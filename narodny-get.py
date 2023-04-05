import logging
import requests
import difflib
from urllib import response
from wsgiref import headers
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import ssl
import certifi


logging.basicConfig(level=logging.DEBUG, filename='funfood.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

pages_to_parce = 15  # Max pages for parsing.


def get_items_(url, filename, seq):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url, verify=False)
    logger.info(f'Page {url} answered {page.status_code}')

    with open(f'data/{filename}_{seq}', 'w') as f:
        f.write(page.text)
        logger.info(f'File data/{filename}_{seq} writing on disk')

    try:
        seq = int(seq)-1
        seq = str(seq)
        with open(f'data/{filename}_{seq}') as read_f:
            previous_page = read_f.read()
    except FileNotFoundError as err:
        logger.error(f'File  data/{filename}_{seq}  not found erase or not must exist {err}')
        previous_page = ''
        pass

    try:
        current_page = BeautifulSoup(page.text, 'html.parser')
        previous_page = BeautifulSoup(previous_page, 'html.parser')
        diff_page_2 = current_page.find('div', class_='dixyCatalogItem__title')
        diff_page_1 = previous_page.find(
            'div', class_='dixyCatalogItem__title')
    except Exception as err:
        logger.error(err)
        pass
        """
        Skip parsing if pages the same, catalog is over
        """
    return [diff_page_1, diff_page_2]


def download_pages(base_url, number_of_pages, filename):
    for sequence in range(number_of_pages):
        html_diff = get_items_(f'{base_url}?sPAGEN_1={sequence}', f'{filename}', sequence)

        try:
            if html_diff[0] == html_diff[1] and sequence >= 2:
                logger.info('Catalog is over, stop downloading go parse')
                break
        except Exception as err:
            logger.info('Pass, empty page', err)
            pass
    return sequence

# for el in category_list_urls: #For test
#     f_name = get_file_name(el)
#     print(f_name[-2])


def get_catalog(url, filename):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url, verify=False)
    logger.info(f'Page {url} answered {page.status_code}')

    with open(f'data/{filename}', 'w') as f:
        f.write(page.text)
        logger.info(f'File data/{filename} writing on disk')

    return page
def get_url(url):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1,
                    status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    page = s.get(url, verify=False)
    logger.info(f'Page {url} answered {page.status_code}')
    return page

def get_paginator_links(category_url):
    paginator_links_list = []
    page = get_url(category_url)
    # print(page.text)
    paginator_items = BeautifulSoup(page.text, 'html.parser')
    paginator_links = paginator_items.find_all('a', class_='page-numbers', href=True)
    for el in paginator_links:
        paginator_links_list.append(el['href'])
    return paginator_links_list[:-1]

def get_products_pages(paginator_links_list):
    pages_data = []
    for url in paginator_links_list:
        page = get_url(url)
        pages_data.append(page)
    return pages_data

# url ='https://narodniy.spb.ru/'
# filename = 'narodny_catalog.html'
# print(get_catalog(url, filename).text)

category_url = 'https://narodniy.spb.ru/category/1_pticza-myaso/'
# get_paginator_links(category_url)
# paginator_links_list = get_paginator_links(category_url)

# print(len(get_products_pages(paginator_links_list)))

