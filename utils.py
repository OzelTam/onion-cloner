from urllib.parse import urlparse

from bs4 import BeautifulSoup


def extract_internal_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a')
    internal_urls = []
    base_domain = urlparse(base_url).netloc
    for link in links:
        href = link.get('href')
        if href:
            parsed_href = urlparse(href)
            href_domain = parsed_href.netloc
            if href_domain == "" or href_domain == base_domain:
                internal_urls.append(href)
    return internal_urls

def is_valid_link(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ['http', 'https']:
        return False
    if parsed_url.netloc == "":
        return True
    if parsed_url.scheme == 'mailto' or parsed_url.path.startswith('javascript:'):
        return False
    return True
