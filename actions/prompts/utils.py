from pathlib import Path
from jinja2 import FileSystemLoader, Environment


def load_prompt_template(filename: str, templates_path: Path):
    """
    Loads jinja template from given path
    :param templates_path:
    :param filename:
    :return:
    """
    file_loader = FileSystemLoader(templates_path)
    env = Environment(loader=file_loader)
    template = env.get_template(filename)
    return template
