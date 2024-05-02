from bs4 import BeautifulSoup


def parser(response):
    status_code = response.status_code
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.text if soup.title else ''
    h1 = soup.h1.text if soup.h1 else ''
    description = soup.find('meta', {'name': 'description'})
    description_content = description['content'] if description else ''
    return status_code, title, h1, description_content
