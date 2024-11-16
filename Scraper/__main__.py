import time

from Product import Product
from Scraper import Scraper

def main():
    mainpage = "https://yarnstreet.com/"
    timeSt = time.time()
    scr = Scraper(mainpage)
    scr.getCategories()
    scr.getProducts()
    print(time.time() - timeSt)
    scr.statistics()

if __name__ == "__main__":
    main()