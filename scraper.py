import random
import requests
from bs4 import BeautifulSoup
from time import sleep


class Scraper:
    """
    Basic scrapper class to fetch data 
    """
    def __init__(self, base_url, proxy=None, retries=3, delay=2):
        self.base_url = base_url
        self.proxy = proxy
        self.retries = retries
        self.delay = delay

    def _fetch_page(self, url):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            session = requests.Session()
            if self.proxy:
                session.proxies = {'http': self.proxy, 'https': self.proxy}
            for _ in range(self.retries):
                try:
                    response = session.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    return response.text
                except requests.RequestException:
                    sleep(self.delay)
            return ""

    def scrape_products(self, num_pages=1):
        products = []

        for page_num in range(1, num_pages + 1):
            url = self.base_url if page_num == 1 else f"{self.base_url}/page/{page_num}/"
            print(f"Scraping... {url}")
            page_content = self._fetch_page(url)
            if page_content:
                products.extend(self._get_product_data_from_html(page_content))
            else:
                print(f"Failed to scrape page {page_num}")
            sleep(random.uniform(1, 3))  # Random sleep between pages

        return products

    def _get_product_data_from_html(self, page_content):
        soup = BeautifulSoup(page_content, 'html.parser')
        master_div = soup.find('div', class_='mf-shop-content')
        product_elements = master_div.find_all('li', class_="product")
        products = []
        for product in product_elements:
            link = product.find('h2', class_='woo-loop-product__title').find('a')['href']
            product_name = link.split('/')[-2]
            title = ' '.join([word.capitalize() for word in product_name.split('-')])
            try:
                price = product.find('span', class_='price').find('ins').get_text(strip=True)
            except AttributeError:
                price = product.find('span', class_='price').find('bdi').get_text(strip=True)
            image_url = product.find('img')['src']
            products.append({
                'product_title': title,
                'product_price': price,
                'path_to_image': image_url,
            })

        return products
