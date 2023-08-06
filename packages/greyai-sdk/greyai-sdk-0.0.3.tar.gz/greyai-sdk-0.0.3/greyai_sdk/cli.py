import click
from greyai_sdk.package import package_directory
import os


@click.group()
def main():
    """
    grey command line utilities to work with local datasets, packaging and publishing
    """
    pass


@main.command()
def package():
    """
    package your application for publishing to grey marketplace

    if .greyignore file is found in project root, files and folders mentioned in file
    will be excluded from generated package
    """
    package_directory(os.getcwd())


if __name__ == '__main__':
    main()

