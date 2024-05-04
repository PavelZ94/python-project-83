import validators
from urllib.parse import urlparse


def validate(url: str) -> list:
    """
    Validate that the given address meets the specified requirements:
    - availability of the address;
    - length;
    - validity;

    Args:
        url (str): The name of the URL to validate.

    Returns:
        errors (list): a list of errors,
        if they were identified during the validation process.
    """
    errors = []
    if url == '':
        errors.append('Url is empty')

    if len(url) > 255 or not validators.url(url):
        errors.append('Not valid url')

    if url is None:
        errors.append('Url not found')

    return errors


def normalize(url: str) -> str:
    """
    Returns the url to its normal appearance.

    Args:
        url (str): The name of the URL to normalize.
        At this stage, the address that has passed validation is transmitted.

    Returns:
        url (str): the normalized url looks like: scheme://netloc.
    """
    normalized_url = urlparse(url)
    return f'{normalized_url.scheme}://{normalized_url.netloc}'
