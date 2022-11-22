from page_loader.cli import parse_args


def test_args_parser(capsys) -> None:
    """
    testing the args tester given from the user
    :return: asserts
    """
    output: tuple = parse_args(['https://site.com',
                                "--output", '/home/asu'])
    assert output.url == 'https://site.com'
    assert output.output == '/home/asu'
