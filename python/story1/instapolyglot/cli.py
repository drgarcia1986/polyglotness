import argparse

from .handlers import (
    create_database,
    download,
    show_infos
)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


create_db_parser = subparsers.add_parser(
    'create_database',
    help='Create SQLite database'
)
create_db_parser.set_defaults(handler=create_database)


download_parser = subparsers.add_parser(
    'download',
    help='Download and store pictures'
)
download_parser.set_defaults(handler=download)
download_parser.add_argument(
    'count',
    type=int,
    help='number of pictures to download'
)
download_parser.add_argument(
    '--show-infos',
    action='store_true',
    help='show informations about pictures'
)


show_infos_parser = subparsers.add_parser(
    'show_infos',
    help='Show infos about salved pictures'
)
show_infos_parser.set_defaults(handler=show_infos)
show_infos_parser.add_argument(
    'count',
    type=int,
    help='number of pictures to show informations'
)
