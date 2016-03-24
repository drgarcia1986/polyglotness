from concurrent.futures import ThreadPoolExecutor, wait
import os

import requests

from .database import (
    engine,
    get_or_create,
    ModelBase,
    session_builder,
)
from .models import Picture


API_URL_BASE = 'https://api.myjson.com/bins/2e3xw'
IMAGES_DIR = 'images'


def create_database(args):
    try:
        ModelBase.metadata.create_all(engine)
    except Exception as e:
        print('Error on create database:\n{}'.format(e))
    else:
        print('The database was created successfully')


def _show_picture_info(picture):
    print('ID: {}'.format(picture.id))
    print('Link: {}'.format(picture.link))
    print('Low Resolution: {}'.format(picture.low_resolution))
    print('Thumbnail: {}'.format(picture.thumbnail))
    print('Standard: {}'.format(picture.standard_resolution))
    print('-' * 30)


def show_infos(args):
    session = session_builder()
    pictures = session.query(Picture).limit(args.count)

    print('=' * 24)
    print('= Pictures in database =')
    print('=' * 24)

    for picture in pictures:
        _show_picture_info(picture)


def _download_picture(url, image_path):
    try:
        response = requests.get(url, stream=True)
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    except Exception as e:
        print('Error to download picture {}: {}'.format(url, e))


def _generate_imagem_patch(pic_id, pic_type):
    return os.path.join(IMAGES_DIR, '{}-{}.jpg'.format(pic_id, pic_type))


def download(args):
    try:
        response = requests.get(API_URL_BASE).json()
    except Exception as e:
        print('Error on get and parse API response: {}'.format(e))
        return

    print('=' * 24)
    print('= Pictures to database =')
    print('=' * 24)

    session = session_builder()
    for picture in response['data'][:args.count]:
        images = {
            key: _generate_imagem_patch(picture['id'], key)
            for key in picture['images'].keys()
        }
        values = {'id': picture['id'], 'link': picture['link']}
        values.update(images)
        try:
            instance, created = get_or_create(
                session,
                Picture,
                defaults=values,
                id=values['id']
            )
        except Exception as e:
            print('Error to get or create picture {}: {}'.format(
                values['id'], e
            ))
            return

        if created:
            pictures = (
                (picture['images'][key]['url'], value)
                for key, value in images.items()
            )
            with ThreadPoolExecutor(max_workers=3) as executor:
                downloads = [
                    executor.submit(
                        _download_picture, url, image_path
                    )
                    for url, image_path in pictures
                ]
                wait(downloads)

        if args.show_infos:
            _show_picture_info(instance)

    session.commit()
    print('Done :D')
