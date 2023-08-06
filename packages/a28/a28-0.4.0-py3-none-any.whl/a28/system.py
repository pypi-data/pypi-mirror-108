# vim: encoding=utf-8 ts=4 et sts=4 sw=4 tw=79 fileformat=unix nu wm=2
import os
import shutil
from . import utils


def options(mainparser):
    """Argparse options added to the cli."""
    parser = mainparser.add_parser(
        'system',
        aliases=['sys'],
        help='system actions'
    )
    subparser = parser.add_subparsers(
        dest='system',
        required=True,
        help='system',
    )
    parser_exist = subparser.add_parser(
        'exists',
        help='check if the system configuration exists.',
    )
    parser_exist.set_defaults(func=exists)
    parser_clean = subparser.add_parser(
        'clean',
        help='clean (delete) the configuration permanently.',
    )
    parser_clean.set_defaults(func=clean)
    parser_clean.add_argument(
        '-f',
        '--force',
        action='store_true',
        help='force the configuration to be removed bypassing confirmation',
    )


def clean(args):
    """Using the shutil utilities, delete all the files provided in the STORAGE
    directory. If an error occurs, catch the exception and print it out to the
    STDOUT.
    """
    message = f"Delete ALL configuration data from '{utils.STORAGE}'? y/n?"
    if not os.path.isdir(utils.STORAGE):
        utils.message('No configuration to clean.')
        return

    elif not args.force and not utils.confirm(message):
        utils.message(f'Not deleting {utils.STORAGE}')
        return

    try:
        shutil.rmtree(utils.STORAGE)
        utils.message(f'Deleted all files and directories in {utils.STORAGE}')
    except OSError as e:
        utils.message(f'Error: {utils.STORAGE} : {e.strerror}')


def exists(_):
    """Check if the configuration directory exists."""
    if os.path.isdir(utils.STORAGE):
        utils.message(f"Configuration exists at '{utils.STORAGE}'.")
    else:
        utils.message(f"No configuration exists at '{utils.STORAGE}'.")
