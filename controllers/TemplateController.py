from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates/"),
    autoescape=select_autoescape()
)

template = env.get_template("index.jinja2")


def get_thing(resource: str):
    return env.get_template(resource)
