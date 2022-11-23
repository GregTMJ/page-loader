import codecs
import os

from page_loader.handlers.assets_handler import handle_assets

HTML_FILE = 'ru-hexlet-io-courses.html'
URL = 'https://ru.hexlet.io/courses'
PATH = 'ru-hexlet-io-courses_files'
ASSETS = [
    ('https://ru.hexlet.io/packs/js/runtime.js',
     'ru-hexlet-io-packs-js-runtime.js'),
    ('https://ru.hexlet.io/assets/application.css',
     'ru-hexlet-io-assets-application.css'),
    ('https://ru.hexlet.io/courses',
     'ru-hexlet-io-courses.html'),
    ('https://ru.hexlet.io/assets/professions/nodejs.png',
     'ru-hexlet-io-assets-professions-nodejs.png')
]


def get_fixture_path(file_name):
    work_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(work_dir, 'fixtures', file_name)


def read(file_path):
    html_file = get_fixture_path(file_path)
    with codecs.open(html_file, 'r', 'utf-8') as f:
        result = f.read()
    return result


def test_assets_handler():
    """
    Checking if the function is working correctly
    """
    html_content = read(HTML_FILE)
    _, assets = handle_assets(html_content, URL, PATH)
    assert assets == ASSETS
