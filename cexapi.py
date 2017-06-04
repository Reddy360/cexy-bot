from urllib.parse import quote
from urllib.request import urlopen
import json

class CexApi:

    def __init__(self):
        self.CEX_SEARCH_URL = 'https://{}.webuy.com/search/index.php?stext={}&section='
        self.CEX_PRODUCT_PAGE = 'https://{}.webuy.com/product.php?sku={}'
        self.CEX_UNIVERSIAL_VARIABLE = 'window.universal_variable = '
        self.CEX_BASE = 'https://{}.webuy.com/{}'

    def cexScrape(self, url):
        urlHandle = urlopen(url)
        for line in urlHandle:
            line = line.decode('utf-8').strip()[:-1]
            if line.startswith(self.CEX_UNIVERSIAL_VARIABLE):
                line = line.replace(self.CEX_UNIVERSIAL_VARIABLE, '')
                array = json.loads(line)
                return array

    def search(self, search, region='UK'):
        # Invokes a search on the CeX website and returns the full list
        searchUrl = self.CEX_SEARCH_URL.format(region, quote(search))
        array = self.cexScrape(searchUrl)
        if len(array['listing']) == 0:
            return []
        return array['listing']['items']


    def searchFirst(self, search):
        # Invokes a search on the CeX website and returns the first item
        return self.search(search)[0]

    def searchWithStock(self, search, region='UK'):
        # Invokes a search on the CeX website and returns the full list with stock
        instock = []

        for product in self.search(search, region=region):
            stock = int(product['stock'])
            if stock > 0:
                instock.append(product)
        return instock

    def searchFirstWithStock(self, search, region='UK'):
        # Invokes a search on the CeX website and returns the first item with stock
        products = self.searchWithStock(search, region=region)
        if len(products) == 0:
            return []
        return products[0]

    def lookupProductPage(self, sku, region='UK'):
        # Invokes a lookup on the CeX page using the sku
        productUrl = self.CEX_PRODUCT_PAGE.format(region, quote(sku))
        array = self.cexScrape(productUrl)
        return array['product']