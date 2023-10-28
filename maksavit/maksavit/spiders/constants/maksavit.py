XPATH_TITLE = '//h1[contains(@class, "product-top")]/text()'
XPATH_LASTPAGE_NUMBER = '(//a[contains(@class, "ui-pagination__item")])[last()]/@href'
XPATH_URLS_PRODUCTS = '(//a[contains(@class, "product-card-block__title")])/@href'
XPATH_CURRENT_PRICE = '//div[contains(@class, "price-info__price")]/span/text()'
XPATH_ORIGINAL_PRICE = '//div[@class="price-box__old-price"]/text()'
XPATH_DESCRIPTION = '//div[contains(@class, "ph23")]/p/text()'
XPATH_IMAGE = '//div[contains(@class, "product-picture")]/img/@src'
XPATH_BRAND = '(//a[@class="product-info__brand-value"]|//div[@class="product-info__brand-value"]|//span[@class="product-info__brand-value"])/text()'
XPATH_RPC = '//div/@data-product-id'
XPATH_SECTION = '//a[@class="breadcrumbs__link"]/span[@itemprop="name"]/text()'
XPATH_MARKETING_TAG = '//div[contains(@class, "product-picture")]/div/text()'
XPATH_STOCK = '//div[contains(@class, "another-city__city")]/span/text()'
XPATH_COUNTRY = '//a[contains(@class, "product-info__brand-value")]/text()'
