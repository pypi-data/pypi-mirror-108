from dataclasses import dataclass
from typing import Literal, Optional, Tuple, List
import psycopg2.extras;
from subsql.parser import parser, util, ParserSnippet, ParserError, ParserOption

return_types = ["one", "many", "column", "scalar", "void", "rowcount", "lastrowid"]
supported_options = ["name", "template", "execute", "all", "doc"] + return_types

@dataclass
class PgCommand:
    name: str
    query: str
    returns: Literal["one", "many", "column", "scalar", "void", "rowcount", "lastrowid"]
    all: bool
    execute: Optional[Literal["batch", "values"]]
    template: Optional[str]
    modifier: Optional[str]

def parse(path: str) -> Tuple[List[ParserError], List[PgCommand]]:

    ### Setup global state we'll be using throughout this function ###

    errors = [] # list of errors to display to user
    command_snippets = {} # command snippets keyed by name
    template_snippets = {} # template snippets keyed by name
    command_objects = [] # command objects

    ### Parse file into snippets ###

    snippets: List[ParserSnippet] = parser.parse_file(path)

    if not snippets:
        errors.append(ParserError(message="No SQL snippets found", file=path, lineno=1))
        return [], []


    ### Sort snippets into command/template buckets keyed by snippet name ###

    for snippet in snippets:
        if name_option := util.get_option(snippet, "name"):
            if name_option.value in command_snippets:
                errors.append(ParserError(
                    message=f"Command {name_option.value} already exists",
                    file=snippet.file,
                    lineno=snippet.lineno
                ))
            else:
                command_snippets[name_option.value] = snippet
        elif template_option := util.get_option(snippet, "template"):
            if template_option.value in template_snippets:
                errors.append(ParserError(
                    message=f"Template {template_option.value} already exists",
                    file=snippet.file,
                    lineno=snippet.lineno
                ))
            else:
                template_snippets[template_option.value] = snippet
        else:
                errors.append(ParserError(message="Snippet doesn't have a name", file=snippet.file, lineno=snippet.lineno))

    ### Add template option to corresponding command snippets ###

    for template_name in template_snippets:
        if template_name in command_snippets:
            template = template_snippets[template_name]
            command = command_snippets[template_name]
            execute_option = util.get_option(command, "execute") 

            if execute_option and execute_option.value == "values":
                command.options.append(
                    ParserOption(
                        name="template",
                        value=template.sql,
                        file=template.file,
                        lineno=template.lineno,
                        modifier=None
                    )
                )
            else:
                errors.append(ParserError(
                    message=f"Function for template {template_name} must have ':execute values' specified",
                    file=template.file,
                    lineno=template.lineno
                ))

                del command_snippets[template_name]
        else:
            errors.append(ParserError(
                message=f"Cannot find matching function for template {template_name}",
                file=template.file,
                lineno=template.lineno
            ))

    ### Process command snippets and convert them to objects ###

    for command_name in command_snippets:
        snippet = command_snippets[command_name]

        if unsupported_options := [s for s in snippet.options if s.name not in supported_options]:
            for unsupported in unsupported_options:
                errors.append(ParserError(
                    message=f"Unsupported option {unsupported.name}",
                    file=unsupported.file,
                    lineno=unsupported.lineno
                ))
            continue

        if duplicate_options := util.get_duplicate_options(snippet):
            errors.append(ParserError(
                message="Found duplicate option " + ', '.join(duplicate_options),
                file=snippet.file,
                lineno=snippet.lineno
            ))
            continue

        if not snippet.sql:
            errors.append(ParserError(message=f"No query found for command {command_name}", file=snippet.file, lineno=snippet.lineno))
            continue
        
        # we'll start collect arugments to PgCommand here
        args = {"name": command_name, "query": snippet.sql}

        # since we don't allow duplicate option names let's convert options list to a dict
        options = util.get_options_dict(snippet.options)

        returns = [o for o in options if o in return_types]

        if len(returns) == 0:
            args["returns"] = "void"
        elif len(returns) == 1:
            args["returns"] = returns[0]
        else:
            errors.append(ParserError(
                message="Multiple returns types (" + ', '.join(returns) + f") specified for command {command_name}",
                file=snippet.file,
                lineno=snippet.lineno
            ))
            continue

        if "execute" in options:
            execute_option = options["execute"]
            execute_value = execute_option.value
            if execute_value in ["batch", "values"]:
                args["execute"] = execute_value
            else:
                errors.append(ParserError(
                    message=f"Parameter to :execute must be 'batch' or 'values', not '{execute_value}'",
                    file=execute_option.file,
                    lineno=execute_option.lineno
                ))
                continue
        else:
            args["execute"] = None

        args["template"] = options["template"].value if "template" in options else None
        args["all"] = True if "all" in options else False
        args["modifier"] = None

        command_objects.append(PgCommand(**args))

    return errors, command_objects

# "insert into {} values (%s, %s)"
# sqlist.save_posts([10, 20], format=lambda s: s.format(sql.Identifier('my_table')))

def execute(self, command, args=None, cursor=None, format=None, modifier=None, size=None):
    cursor = cursor if cursor else self.conn.cursor()
    query = format(command.query) if format else command.query
    modifier = modifier if modifier else command.modifier

    if not modifier:
        modify = lambda r: r
    elif modifier in self.modifiers:
        modify = self.modifiers[modifier]
    else:
        raise f"Unknown modifier {modifier}"

    if command.execute == "batch":
        psycopg2.extras.execute_batch(cursor, query, args, page_size=size)
    elif command.execute == "values":
        psycopg2.extras.execute_values(cursor, query, args, template=command.template, page_size=size)
    else:
        cursor.execute(query, args)

    ### one ###
    if command.returns == "one":
        result = modify(cursor.fetchone())
    ### many ###
    elif command.returns == "many":
        if command.all:
            result = [modify(r) for r in cursor.fetchall()]
        else:
            result = iterator(cursor, modify, size=size)
    ### column ###
    elif command.returns == "column":
        if command.all:
            result = [r[0] for r in cursor.fetchall()]
        else:
            result = iterator(cursor, modify, size=size if size else 0, column=True)
    ### scalar ###
    elif command.returns == "scalar":
        result = cursor.fetchone()[0]
    ### void ###
    elif command.returns == "void":
        result = None
    ### rowcount ###
    elif command.returns == "rowcount":
        result = cursor.rowcount
    ### lastrowid ###
    elif command.returns == "lastrowid":
        result = cursor.lastrowid
    else:
        raise f"Unknown return type {command.returns}"

    return result

def iterator(cursor, modify, size=0, column=False):
    if size > 1:
        while results := cursor.fetchmany(size=size):
            if column:
                yield [r[0] for r in results]
            else:
                yield [modify(r) for r in results]
    else:
        while result := cursor.fetchone():
            if column:
                yield result[0]
            else:
                yield modify(result)
