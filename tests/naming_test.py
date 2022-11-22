from page_loader.handlers.assets_handler import asset_file_naming


IMAGE_URL = 'ru.hexlet.io/assets/professions/nodejs.png'
SCRIPT_URL = 'ru.hexlet.io/packs/js/runtime.js'
HTML_URL = 'ru.hexlet.io/courses'


def test_naming():
    """
    checking if all the names going to come good after
    getting reformed
    """
    assert asset_file_naming(IMAGE_URL) == "ru-hexlet-io-assets-professions-nodejs.png"
    assert asset_file_naming(SCRIPT_URL) == "ru-hexlet-io-packs-js-runtime.js"
    assert asset_file_naming(HTML_URL) == "ru-hexlet-io-courses.html"
