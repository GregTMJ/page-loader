import codecs
import os
import pytest
import requests.exceptions
import requests_mock
import tempfile

from urllib.parse import urljoin
from page_loader.downloader import download, renaming_url

URL = 'https://ru.hexlet.io/courses'
FILE_NAMING = ("ru-hexlet-io-courses.html",
               "ru-hexlet-io-courses_files")
ASSET_DIR = 'ru-hexlet-io-courses_files'
HTML_FILE = 'ru-hexlet-io-courses.html'

DOWNLOAD_HTML_FILE = "page-loader.hexlet.repl.co.html"
DOWNLOAD_URL = "https://page-loader.hexlet.repl.co/"
DOWNLOAD_ASSETS_DIR = "page-loader-hexlet-repl-co_files"
ASSETS = [
    {
        'format': 'css',
        'url_path': '/assets/application.css',
        'file_name': 'page-loader-hexlet-repl-co-assets-application.css',
    },
    {
        'format': 'png',
        'url_path': '/assets/professions/nodejs.png',
        'file_name': 'page-loader-hexlet-repl-co-assets-professions'
                     '-nodejs.png',
    },
    {
        'format': 'js',
        'url_path': '/script.js',
        'file_name': 'page-loader-hexlet-repl-co-script.js',
    },
    {
        'format': 'html',
        'url_path': '/courses',
        'file_name': 'page-loader.hexlet.repl.co.html',
    },
]


def get_fixture_path(file_name):
    work_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(work_dir, 'fixtures', file_name)


def get_fixture_data(file_path, mode='r') -> str | bytes:
    full_file_path = get_fixture_path(file_path)
    with codecs.open(full_file_path, mode, 'utf-8') as f:
        result = f.read()
    return result


def test_download():
    new_html_file, html_content_files = renaming_url(URL)
    assert new_html_file, html_content_files == FILE_NAMING

    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL)
            new_path = download(URL, tempdir)
            resulting_path = os.path.join(tempdir, new_html_file)
            assert new_path == resulting_path


def test_connection_error():
    """
    trying to test te download for invalid sites with a > 400 response
    """
    bad_site = 'http://httpbin.org/status/404'
    with tempfile.TemporaryDirectory() as tempdir:
        assert not os.listdir(tempdir)

        with requests_mock.Mocker() as mock:
            mock.get(bad_site, exc=requests.exceptions.ConnectionError)

            with pytest.raises(Exception):
                assert download(bad_site, tempdir)


def test_bad_storage_directory():
    """
    Testing exception if giving not a good directory
    """
    with requests_mock.Mocker() as mock:
        mock.get(URL)
        not_existing_path = '/sys'
        file_path = get_fixture_path("ru-hexlet-io-courses.html")
        with pytest.raises(Exception):
            assert download(URL, not_existing_path)

        with pytest.raises(Exception):
            assert download(URL, file_path)


def test_page_download(requests_mock):
    """
    Testing the page-downloader
    """
    request_content = get_fixture_data(DOWNLOAD_HTML_FILE)
    requests_mock.get(DOWNLOAD_URL, text=request_content)

    for asset in ASSETS:
        url_asset = urljoin(DOWNLOAD_URL, asset['url_path'])
        requests_mock.get(url_asset)

    with tempfile.TemporaryDirectory() as tempdir:
        assert not os.listdir(tempdir)

        output = download(DOWNLOAD_URL, tempdir)
        output_html_path = os.path.join(tempdir, "page-loader-hexlet-repl-co.html")
        assert output == output_html_path
        assert len(os.listdir(tempdir)) == 2
        assert len(os.listdir(os.path.join(tempdir, DOWNLOAD_ASSETS_DIR))) == 4
