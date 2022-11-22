import requests


def get_content(url: str) -> str:
    """
    download content from url
    :param url: the given url
    :return: the request results
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
