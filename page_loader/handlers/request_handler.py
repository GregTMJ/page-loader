import logging
import requests


def get_html_content(url: str) -> str:
    """
    download content from url
    :param url: the given url
    :return: the request results
    """
    response = requests.get(url, stream=True)
    logging.info(f"downloading from {url}")
    response.raise_for_status()
    return response.text


def get_asset_content(url: str) -> bytes:
    """
    download content from url
    :param url: the given url
    :return: the request results
    """
    response = requests.get(url, stream=True)
    logging.info(f"downloading from {url}")
    response.raise_for_status()
    return response.content
