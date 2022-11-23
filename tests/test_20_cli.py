# Тесты консольной части приложения сделаны для системы
# автоматической проверки тестов.
# Пользователям их реализовывать не требуется.

import os
import pytest
import re
import subprocess
import tempfile
import threading
from urllib.parse import urljoin
from flask import Flask, abort, send_file

INVALID_BASE_URL = 'http://badsite'
BASE_URL = 'http://localhost'
PAGE_PATH = '/blog/about'
PAGE_URL = urljoin(BASE_URL, PAGE_PATH)
HTML_FILE_NAME = 'localhost-blog-about.html'
ASSETS_DIR_NAME = 'localhost-blog-about_files'
ASSETS = {
    'css': {
        'url_path': '/blog/about/assets/styles.css',
        'file_name': 'localhost-blog-about-assets-styles.css',
    },
    'svg': {
        'url_path': '/photos/me.jpg',
        'file_name': 'localhost-photos-me.jpg',
    },
    'js': {
        'url_path': '/assets/scripts.js',
        'file_name': 'localhost-assets-scripts.js',
    },
    'html': {
        'url_path': '/blog/about',
        'file_name': 'localhost-blog-about.html',
    },
}


def run_app(url, output_path=None):
    args = ['poetry', 'run', 'page-loader']
    if output_path is not None:
        args.extend(['-o', output_path])
    args.extend([url])
    return subprocess.run(args, capture_output=True, text=True)


def get_fixture_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'fixtures', file_name)


def read(file_path, mode='r'):
    with open(file_path, mode) as f:
        result = f.read()
    return result


def get_fixture_data(file_name):
    return read(get_fixture_path(file_name))


@pytest.fixture(scope='module', autouse=True)
def prepare_assets():
    for format in ASSETS:
        asset = ASSETS[format]
        file_path = get_fixture_path(
            os.path.join('expected', ASSETS_DIR_NAME, asset['file_name'])
        )
        asset['file_path'] = file_path
        asset['expected_content'] = read(file_path, 'rb')


@pytest.fixture(scope='module', autouse=True)
def run_server():  # noqa: C901
    app = Flask(__name__)

    @app.route('/notfound')
    def not_found():
        abort(404)

    @app.route('/internalerror')
    def internal_error():
        abort(500)

    @app.route(PAGE_PATH)
    def get_html():
        return send_file(get_fixture_path(HTML_FILE_NAME))

    @app.route(ASSETS['css']['url_path'])
    def get_css():
        return send_file(ASSETS['css']['file_path'])

    @app.route(ASSETS['js']['url_path'])
    def get_js():
        return send_file(ASSETS['js']['file_path'])

    @app.route(ASSETS['svg']['url_path'])
    def get_svg():
        return send_file(ASSETS['svg']['file_path'])

    thread = threading.Thread(
        target=app.run,
        args=('localhost', 80),
        daemon=True
    )
    thread.start()


# проверка ошибок сети
def test_connection_error():
    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)

        process = run_app(INVALID_BASE_URL, tmpdirname)
        assert process.returncode != 0

        assert not os.listdir(tmpdirname)


# проверка ошибок с сайта
@pytest.mark.parametrize(
    'path,code',
    [('/notfound', 404), ('/internalerror', 500)]
)
def test_response_with_error(path, code):
    url = urljoin(BASE_URL, path)

    with tempfile.TemporaryDirectory() as tmpdirname:
        process = run_app(url, tmpdirname)
        assert process.returncode != 0


# проверка ошибок файловой системы
def test_storage_errors():
    root_dir_path = '/sys'
    process = run_app(PAGE_URL, root_dir_path)
    assert process.returncode != 0

    file_path = get_fixture_path(HTML_FILE_NAME)
    process = run_app(PAGE_URL, file_path)
    assert process.returncode != 0

    not_exists_path = get_fixture_path('notExistsPath')
    process = run_app(PAGE_URL, not_exists_path)
    assert process.returncode != 0


def test_page_load():
    expected_html_file_path = get_fixture_path(
        os.path.join('expected', HTML_FILE_NAME),
    )
    expected_html_content = read(expected_html_file_path)

    with tempfile.TemporaryDirectory() as tmpdirname:
        assert not os.listdir(tmpdirname)

        # NOTE:
        # It's hard to debug internal errors without any logging.
        # We must be sure that students are able to read their logs from either stdout or stderr.
        process = run_app(PAGE_URL, tmpdirname)
        stdout = process.stdout
        stderr = process.stderr
        returncode = process.returncode
        assert returncode == 0, 'exit code 0 expected, got {}. stdout: {}, stderr: {}'.format(
            returncode, stdout, stderr
        )

        assert len(os.listdir(tmpdirname)) == 2
        assert len(os.listdir(os.path.join(tmpdirname, ASSETS_DIR_NAME))) == 4

        html_file_path = os.path.join(tmpdirname, HTML_FILE_NAME)

        html_content = read(html_file_path)
        assert html_content == expected_html_content

        for format in ASSETS:
            asset = ASSETS[format]
            asset_path = os.path.join(
                tmpdirname,
                ASSETS_DIR_NAME,
                asset['file_name'],
            )
            asset_content = read(asset_path, 'rb')
            expected_asset_content = asset['expected_content']
            assert asset_content == expected_asset_content
