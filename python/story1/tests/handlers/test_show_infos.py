from collections import namedtuple

from instapolyglot.handlers import show_infos
from instapolyglot.models import Picture


ShowInfosArgs = namedtuple('ShowInfosArgs', 'count')


class TestShowInfos:

    def test_should_show_information_about_one_picture(self, mixer, capsys):
        picture = mixer.blend(Picture)
        show_infos(ShowInfosArgs(1))
        out, err = capsys.readouterr()
        assert 'ID: {}'.format(picture.id) in out
        assert 'Link: {}'.format(picture.link) in out

    def test_should_show_information_about_lot_picture(self, mixer, capsys):
        pictures = mixer.cycle(5).blend(Picture)
        assert len(pictures) == 5

        show_infos(ShowInfosArgs(5))
        out, err = capsys.readouterr()
        for picture in pictures:
            assert 'ID: {}'.format(picture.id) in out
            assert 'Link: {}'.format(picture.link) in out

    def test_should_show_information_about_limited_number_of_picture(
        self, mixer, capsys
    ):
        pictures = mixer.cycle(5).blend(Picture)

        show_infos(ShowInfosArgs(2))
        out, err = capsys.readouterr()
        for picture in pictures[:2]:
            assert 'ID: {}'.format(picture.id) in out
            assert 'Link: {}'.format(picture.link) in out
