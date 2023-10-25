import re
import time

import scrapy

from spiders.constants.maksavit import *


class MaksavitRuSpider(scrapy.Spider):
    name = 'maksavit'
    allowed_domains = ['maksavit.ru']
    start_urls = [
        'https://maksavit.ru/catalog/gematologiya/'
    ]

    cookies = {  # для города Архангельск
        'location_code': '0000110423',
        'location_selected': 'Y'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, cookies=self.cookies, callback=self.parse_pages)

    def parse_pages(self, response):
        page_prefix = "?page="
        last_page = response.xpath(XPATH_LASTPAGE_NUMBER).get()
        last_page = int(last_page.split('=')[1])
        url = response.url
        for page_count in range(last_page + 1):
            url_page = f'{url}{page_prefix}{page_count}'
            yield scrapy.Request(url=url_page, cookies=self.cookies, callback=self.parse_category_page)

    def parse_category_page(self, response):
        urls = response.xpath(XPATH_URLS_GOODS).getall()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)

    def get_price_data(self, response):
        current_price = response.xpath(XPATH_PRICE).get()
        original_price = response.xpath(XPATH_ORIGINAL_PRICE).get()
        if current_price:
            current_price = int(''.join(re.findall(r'\d+', current_price)))
            if original_price:
                original_price = int(''.join(re.findall(r'\d+', original_price)))
                sales = ((original_price - current_price) / original_price) * 100
                sales = round(sales, 1)
            else:
                original_price = ''
                sales = 0
        else:
            current_price = ''
            original_price = ''
            sales = 0
        sales_tag = f"Скидка {sales}%" if sales > 0 else ''
        price_data = {"current": current_price, "original": original_price, "sale_tag": sales_tag}
        return price_data

    def get_stock(self, response):
        not_stock = response.xpath(XPATH_STOCK).getall()
        # у товаров, которые отсутствуют в продаже, на странице появляется элемент с текстом "Нет в наличии в вашем городе"
        # у товаров в наличии ничего подобного нет
        if not_stock:
            stock = False
        else:
            stock = True
        count = 1 if stock else 0
        stock = {"in_stock": stock, "count": count}
        return stock

    def get_metadata(self, response):
        description = ','.join(response.xpath(XPATH_DESCRIPTION).getall()) or ''
        country = response.xpath(XPATH_COUNTRY).get()
        country = country.split()[-1] if country else ''

        metadata = {
            '__description': description,
            'СТРАНА ПРОИЗВОДИТЕЛЬ': country
        }
        return metadata

    def parse(self, response):
        main_image = response.urljoin(response.xpath(XPATH_IMAGE).get())
        brand = response.xpath(XPATH_BRAND).get()
        brand = brand.strip().split(',')[0] if brand else ''
        title = response.xpath(XPATH_TITLE).get()
        rpc = response.xpath(XPATH_RPC).get()
        sections = ','.join(response.xpath(XPATH_SECTION).getall()[2:])
        marketing_tag = response.xpath(XPATH_MARKETING_TAG).get("").strip()

        item = {
            "timestamp": int(time.time()),  # Текущее время в формате timestamp
            "RPC": rpc,  # {str} Уникальный код товара
            "url": response.url,  # {str} Ссылка на страницу товара
            "title": title,  # {str} Заголовок/название товара (если в карточке товара указан цвет или объем, необходимо добавить их в title в формате: "{название}, {цвет}")
            "marketing_tags": [marketing_tag],  # {list of str} Список тегов, например: ['Популярный', 'Акция', 'Подарок'], если тэг представлен в виде изображения собирать его ненужно
            "brand": brand,  # {str} Бренд товара
            "section": sections,  # {list of str} Иерархия разделов, например: ['Игрушки', 'Развивающие и интерактивные игрушки', 'Интерактивные игрушки']
            "price_data": self.get_price_data(response),
            "stock": self.get_stock(response),
            "assets": {
                "main_image": main_image,  # {str} Ссылка на основное изображение товара
                "set_images": [main_image],  # {list of str} Список больших изображений товара
                "view360": [],  # {list of str}
                "video": []  # {list of str}
            },
            "metadata": self.get_metadata(response),
            "variants": 0,  # {int} Кол-во вариантов у товара в карточке
                            # (За вариант считать только цвет или объем/масса. Размер у одежды или обуви вариантами не считаются)
        }
        yield item
