import codecs
import logging
import os
import re

from page_loader.content_downloader import download_content
from page_loader.handlers.assets_handler import handle_assets
from page_loader.handlers.request_handler import get_html_content


def download(url, file_path=''):
    """
    download content from a web page and store it locally
    :param url: the web page
    :param file_path: the directory where the content will be downloaded
    :return: directory name
    """
    full_file_path = os.path.join(os.getcwd(), file_path)
    html_file_name, html_content_file_path = renaming_url(url)
    content_file_path = os.path.join(full_file_path, html_content_file_path)
    html_file_path: str = os.path.join(full_file_path, html_file_name)
    html_content = get_html_content(url)
    prettify_html_content, assets = handle_assets(html_content, url,
                                                  html_content_file_path)
    with codecs.open(html_file_path, 'w', 'utf-8') as file:
        logging.info("writing into new local html file: "
                     f"{html_file_path}")
        file.write(prettify_html_content)
    if assets:
        if not os.path.exists(content_file_path):
            logging.info("Creating new directory for assets: "
                         f"{content_file_path}")
            os.mkdir(content_file_path)
        download_content(content_file_path, assets)
    return html_file_path


def renaming_url(url: str) -> tuple:
    """
    helps rename files
    :param url: the web request
    :return: main html file name + directory name for assets
    """
    if 'https://' in url:
        url = re.sub(r"https://", '', url)
    common_name: str = re.sub(r"(\.)|(/)", "-", url)
    if common_name[-1] == '-':
        return common_name[:-1] + '.html', common_name[:-1] + '_files'
    return common_name + '.html', common_name + '_files'
