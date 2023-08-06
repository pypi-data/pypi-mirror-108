from setuptools import setup, find_packages

setup(
    name="elephant-game-tables",
    version="1.0.2",

    author="Fish",
    author_email="jnufish@gmail.com",

    install_requires=[
        "click",
        "click-aliases",
        "Jinja2",
        "openpyxl",
        "regex",
        "six",
    ],

    entry_points={
        "console_scripts": [
            "emt-tables-cli=command:cli"
        ]
    }
)
