from unittest.mock import patch

import pytest

from instapolyglot.database import engine
from instapolyglot.handlers import create_database


class TestCreateDabase:

    @pytest.fixture
    def patch_create_all(self):
        return patch(
            'instapolyglot.handlers.ModelBase.metadata.create_all'
        )

    def test_should_write_a_sucessful_message(self, capsys):
        create_database(None)
        out, err = capsys.readouterr()
        assert 'successfully' in out

    def test_should_call_create_all_sqlalchemy_method(self, patch_create_all):
        with patch_create_all as mock:
            create_database(None)

        assert mock.called
        mock.assert_called_with(engine)
