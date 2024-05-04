from bs4 import BeautifulSoup


def parser(response: str) -> tuple:
    """
    Parse information from given URL.

    Args:
        response (str): the URL address
        from which the information will be taken.

    Returns:
        status_code (int): The HTTP status code of the check.
        title (str): The title parsed from the URL.
        h1 (str): The h1 header from the URL.
        description (str): The meta description from the URL.
    """
    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.text if soup.title else ''
    h1 = soup.h1.text if soup.h1 else ''
    description = soup.find('meta', {'name': 'description'})
    description_content = description['content'] if description else ''
    return status_code, title, h1, description_content
