import os
import pytest
import requests.exceptions
import requests_mock
import tempfile

from page_loader.page_loader import download, renaming_url


URL = 'https://ru.hexlet.io/courses'


def test_download():

    renaming_test_url = renaming_url(URL)
    assert renaming_test_url == "ru-hexlet-io-courses"

    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as mock:
            mock.get(URL)
            new_path = download(URL, tempdir)
            assert new_path == f'{tempdir}\\{renaming_test_url}.html'


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
