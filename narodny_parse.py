from cmath import pi
from bs4 import BeautifulSoup
import datetime
from write_to_db import write_db
from dixy_get import download_pages
from os.path import exists
import logging

logging.basicConfig(level=logging.DEBUG, filename='funfood.log',
                    format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

number_of_pages = 15
dixy_products_data_all = []
seq = 0
url_base = f'https://dixy.ru/catalog/molochnaya-gastronomiya/?sections=molochnaya-gastronomiya%2F&PAGEN_1='
file_name_base = 'dixy_molochnaya-gastronomiya.txt'
counter = 0

filename_catalog = 'data/narodny_catalog.html'

def read_catalog(filename):
    with open(filename) as file:
        catalog_page = file.read()
    return catalog_page


def parse_catalog(catalog_page):
    categories_url_list = []
    soup = BeautifulSoup(catalog_page, 'html.parser')
    categies_items = soup.find_all('li', class_='product-category')
    for el in categies_items:
        category_url = el.find('a', href=True)
        categories_url_list.append(category_url['href'])
    return categories_url_list


def parce_products(products_page):
    pass


def get_file_name(category_url):
    filename_base = category_url.split('/')
    return filename_base


# for category_url in category_list_urls:
#     index = counter
#     file_name_base_list = get_file_name(category_url)
#     file_name_base = file_name_base_list[-2]
#     base_url = category_list_urls[index]
#     counter += 1

#     logger.info(f'URL for category {base_url}')
#     logger.info(f'Base file name for write {base_url}')

#     seq = download_pages(base_url, number_of_pages, file_name_base)

#     if exists(f'data/{file_name_base}_{seq}'):
#         with open(f'data/{file_name_base}_{seq}') as file:
#             logger.info(f'Read file data/{file_name_base}_{seq}')
#             source = file.read()
#             soup = BeautifulSoup(source, 'html.parser')
#             raw_data = soup.find('div', class_='items products')
#             cards_item = raw_data.find_all('div', class_='dixyCatalogItem')
#             for el in cards_item:
#                 dixy_products_data = []
#                 price_rur_tag = el.find(
#                     'div', class_='dixyCatalogItemPrice__new')
#                 price_kop_tag = el.find(
#                     'div', class_='dixyCatalogItemPrice__kopeck')
#                 print(price_rur_tag)
#                 try:
#                     price_rur = price_rur_tag.text.replace(" ", "").strip()
#                 except AttributeError as err:
#                     price_rur = str(0)
#                     logger.debug(f'{err} None RUR in prise')
#                 try:
#                     price_kop = price_kop_tag.text.replace(" ", "").lstrip()
#                 except AttributeError as err:
#                     price_kop = str(0)
#                     logger.debug(f'{err} None KOP in prise')
#                 price_end = float(price_rur + '.' + price_kop)
                

#                 title_qty = el.find('div', class_='dixyModal__title').text
#                 title_qty_list = title_qty.split(',')
#                 if len(title_qty_list) == 1:
#                     title_qty_list = title_qty.split(' ')
#                     title = title_qty_list[0] + ' ' + title_qty_list[1]
#                     qty = title_qty_list[-1].split('\xa0')
#                     try:
#                         mesure = qty[1].rstrip()
#                     except Exception as err:
#                         logger.debug(f'no mesure set null {err}')
#                         mesure = 'уп'
#                     now = datetime.datetime(2022, 1, 1, 00, 00, 00)
#                     str_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                     dixy_products_data.append(title)
#                     dixy_products_data.append(price_end)
#                     dixy_products_data.append(qty[0])
#                     dixy_products_data.append(mesure)
#                     dixy_products_data.append(str_now)
#                     dixy_products_data_all.append(dixy_products_data)
#                 else:
#                     title = title_qty_list[0]
#                     try:
#                         qty = title_qty_list[1].split('\xa0')
#                     except IndexError as err:
#                         qty = 'None'
#                     try:
#                         mesure = qty[1].rstrip()
#                     except Exception as er:
#                         print('no mesure set null')
#                         mesure = 'уп'
#                     now = datetime.datetime(2022, 1, 1, 00, 00, 00)
#                     str_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#                     dixy_products_data.append(title)
#                     dixy_products_data.append(price_end)
#                     dixy_products_data.append(qty[0])
#                     dixy_products_data.append(mesure)
#                     dixy_products_data.append(str_now)
#                     dixy_products_data_all.append(dixy_products_data)

#             else:
#                 pass


catalog_page = read_catalog(filename=filename_catalog)
print(parse_catalog(catalog_page))
# write_db(dixy_products_data_all)
