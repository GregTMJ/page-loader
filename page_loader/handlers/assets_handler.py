import os
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HTML_ATTRS: dict = {
    'link': 'href',
    'script': 'src',
    'img': 'src'
}


def handle_assets(html, url, content_files_path):
    """
    Function to extract all the url content from html, prettify it
    then get all the assets
    :param html: the main html file
    :param url: the url
    :param content_files_path: where the content is stored
    :return: prettify html +
    """
    soup = BeautifulSoup(html, 'html.parser')
    tags = [*soup('link'), *soup('script'), *soup('img')]
    assets = []
    for tag in tags:
        attribute_name: str = HTML_ATTRS.get(tag.name)
        assets_url = tag.get(attribute_name)
        general_assets_url = ''
        if assets_url:
            general_assets_url = urljoin(f'{url}/', assets_url)
        if urlparse(url).netloc == urlparse(general_assets_url).netloc:
            asset_file_name: str = asset_file_naming(general_assets_url)
            assets.append((general_assets_url, asset_file_name))
            tag[attribute_name] = os.path.join(content_files_path,
                                               asset_file_name)
    return soup.prettify(), assets


def asset_file_naming(url: str) -> str:
    """
    helps rename the assets url to local saving
    :param url: the given url of the asset
    :return: new asset name
    """
    url = urlparse(url)
    main_name, extension = os.path.splitext(url.path)
    reformatted_name = re.sub(r"(\.)|(/)", "-", main_name)
    return reformatted_name + extension if extension \
        else reformatted_name + '.html'
