import os

from progress.bar import IncrementalBar

from page_loader.handlers.request_handler import get_asset_content


def download_content(assets_path: str, assets: list):
    """
    Downloading all the content from assets and storing them inside
    new local files
    :param assets_path: where the assets are stored
    :param assets: the list of assets that were downloaded
    """
    bar_assets_len: int = len(assets)
    with IncrementalBar('Loading...', max=bar_assets_len) as bar:
        bar.suffix = "%(percent)d%%"
        bar.fill = '#'
        for url, asset_name in assets:
            asset_content = get_asset_content(url)
            with open(os.path.join(assets_path, asset_name), 'wb') as as_file:
                as_file.write(asset_content)
                bar.next()
