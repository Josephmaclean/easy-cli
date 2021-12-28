from setuptools import setup, find_packages

setup(
    name="Flask-Easy-Cli",
    find_packages=find_packages(),
    install_requires=[
        "Flask-Easy>=0.0.1",
        "cookiecutter>=1.7.3",
        "click>=7.1.2",
        "jinja2>=3.0.3",
        "GitPython>=3.1.24",
    ],
    entry_points={
        'console_scripts': [
            "easy-cli=easy_cli.scripts.easy_scripts:cli"
        ]
    }
)
