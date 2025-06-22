from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

env: Environment = Environment(
    loader=FileSystemLoader(["templates"]),
    autoescape=select_autoescape(["html", "xml"]),
)


def add_template_folder(*template_folders: str):
    global env
    env.loader = FileSystemLoader(list(template_folders))


def template_global(name: str):
    def wrapper(func):
        env.globals[name] = func
        return func

    return wrapper


def template_filter(name: str = None):
    def wrapper(func):
        env.filters[name or func.__name__] = func
        return func

    return wrapper


def render(template_name: str, context: Any = None):
    if context is None:
        context = {}
    template = env.get_template(template_name)
    return template.render(context)