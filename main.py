from fastapi import FastAPI, HTTPException, Depends, Header
from scraper import Scraper
from storage import Storage
from config import Settings
# from notification import Notifier
from cache import Cache

app = FastAPI()

settings = Settings()

# In-memory cache
cache = Cache()

# Scraper and storage initialization
scraper = Scraper(base_url="https://dentalstall.com/shop")
storage = Storage(storage_file="products.json")


# print('>>>>>> settings ',settings)
# Dependency for authentication
def verify_token(x_api_key= Header(...)):
    pass
    # if x_api_key != settings.api_token:
    #     raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/scrape/")
async def scrape_products(num_pages=settings.num_pages, proxy=settings.proxy):
    scraper.proxy = proxy

    # First, check cache for existing results
    cached_data = cache.get('scraped_products')
    if cached_data:
        return cached_data

    # Scrape products
    # print('>>>> num_pages :', num_pages)
    products = scraper.scrape_products(num_pages=num_pages)
    # Store in json
    storage.store_products(products)

    # Notify scraping results
    print(f"Scraping completed. {len(products)} products scraped.")

    # Cache results for quick access
    cache.set('scraped_products', products)

    return {"status": "success", "scraped_products_count": len(products)}
