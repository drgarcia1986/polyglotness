import pytest

from instapolyglot.cli import parser
from instapolyglot.handlers import (
    create_database,
    download,
    show_infos,
)


class TestParser:

    @pytest.mark.parametrize(
        'command, handler, extra_arg',
        [
            ('show_infos', show_infos, '2'),
            ('download', download, '2'),
            ('create_database', create_database, ''),
        ]
    )
    def test_parser_should_get_right_handler(
        self, command, handler, extra_arg
    ):
        cli_args = parser.parse_args(
            '{} {}'.format(command, extra_arg).split()
        )
        assert cli_args.handler is handler
        assert str(getattr(cli_args, 'count', '')) == extra_arg
