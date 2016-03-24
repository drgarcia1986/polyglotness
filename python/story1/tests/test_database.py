from instapolyglot.database import get_or_create
from instapolyglot.models import Picture


class TestGetOrCreateHelper:

    def test_should_return_an_existing_register(
        self, mixer, db_session
    ):
        picture = mixer.blend(Picture)
        args = {
            key: getattr(picture, key)
            for key in picture._sa_class_manager.keys()
        }
        instance, created = get_or_create(db_session, Picture, **args)
        assert not created
        assert instance.id == picture.id

    def test_should_create_new_register(self, db_session):
        instance, created = get_or_create(
            db_session, Picture,
            id='foo', link='http://foo.net',
            low_resolution='foo-low.jpg',
            thumbnail='foo-thumbnail.jpg',
            standard_resolution='foo-standard.jpg'
        )
        assert created
        assert instance.id == 'foo'
