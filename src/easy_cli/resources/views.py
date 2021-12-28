import os
import pathlib
import click
from jinja2 import Template
from .utils import convert_to_camelcase, add_to_init


def create_view(app, name):
    """
    This function creates a view with the name specified.
    This view is created in the rootdir/views
    directory and its auto imported in the __init__.py file

    """
    name = name.lower()
    file_dir = os.path.join(app.root_path, "views")
    root_dir_name = os.path.basename(app.root_path)
    if not os.path.exists(file_dir):
        pathlib.Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_name = f"{name}.py"
    class_name = convert_to_camelcase(name)
    repository_file_name = f"{name}_repository"
    repository_class_name = f"{class_name}"

    template_details = {
        "repository_file_name": repository_file_name,
        "repository_class_name": repository_class_name,
        "root_dir_name": root_dir_name,
        "class_name": class_name,
    }
    template_string = """from core.views import EasyView


class {{class_name}}(EasyView):
    def index(self):
        pass

    def create(self, data):
        pass

    def show(self, item_id):
        pass

    def update(self, item_id, data):
        pass

    def delete(self, item_id):
        pass

"""

    template = Template(template_string)
    data = template.render(**template_details)
    file = os.path.join(file_dir, file_name)
    if not os.path.exists(file):
        with open(file, "w") as w:
            w.write(data)
        click.echo(f"{name} generated successfully")
        add_to_init(file_dir, name, class_name)
