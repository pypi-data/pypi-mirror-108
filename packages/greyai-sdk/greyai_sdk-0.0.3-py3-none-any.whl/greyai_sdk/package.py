import os
import click
import sys
import zipfile
import glob


def zipdir(path, ziph, ignores, zip_root=None):
    if zip_root is None:
        zip_root = path
    # ziph is zipfile handle

    for root, dirs, files in os.walk(path):
        for file in files:
            f = os.path.join(root, file)
            if f in ignores:
                continue
            click.echo(f'adding {f}')
            ziph.write(f, os.path.relpath(os.path.join(root, file), zip_root))
        for dir_name in dirs:
            dir_abs = os.path.join(root, dir_name)
            if f'{dir_abs}/' in ignores:
                continue
            zipdir(dir_abs, ziph, ignores, zip_root)
        break


def package_directory(directory):
    if not os.path.exists(os.path.join(directory, 'requirements.txt')):
        click.echo(click.style('requirements.txt file not found in the root', fg='red'))
        sys.exit(1)

    ignores = []
    ignore_file = os.path.join(directory, '.greyignore')
    if os.path.exists(ignore_file):
        click.echo('.greyignore file found, files and folders mentioned will be ignored')
        with open(ignore_file) as f:
            globs = f.read().split('\n')
            for g in globs:
                abs_g = [os.path.join(directory, pth) for pth in glob.glob(g)]
                ignores = ignores + abs_g
    _, name = os.path.split(directory)
    build_dir = os.path.join(directory, 'build')
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)
    elif os.path.isfile(build_dir):
        click.echo('tried creating build directory, it already exists and is a file. Expected a directory')
        sys.exit(1)

    pkg_zip = os.path.join(build_dir, f'{name}.zip')
    if os.path.exists(pkg_zip):
        os.remove(pkg_zip)

    zipf = zipfile.ZipFile(pkg_zip, 'w', zipfile.ZIP_DEFLATED)
    zipdir(directory, zipf, ignores)
    zipf.close()



