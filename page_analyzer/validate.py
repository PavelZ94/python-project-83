import validators
from urllib.parse import urlparse


def validate(url):
    errors = []
    if url == '':
        errors.append('Url is empty')

    if len(url) > 255 or not validators.url(url):
        errors.append('Not valid url')

    if url is None:
        errors.append('Url not found')

    return errors


def normalize(url):
    normalized_url = urlparse(url)
    return f'{normalized_url.scheme}://{normalized_url.netloc}'
