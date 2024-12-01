import time, os, sys

from Scraper import Scraper

def main():
    args = sys.argv
    mainpage = "https://yarnstreet.com/"
    thumbnailPath = os.path.join(os.getcwd(), "images", "thumbnails")
    colorsPath = os.path.join(os.getcwd(), "images")
    productsPath = os.path.join(os.getcwd(), "results", "products.json")
    if (len(args) == 4):
        mainpage = args[1]
        thumbnailPath = args[2]
        colorsPath = args[3]
        productsPath = args[4]
    productsDir = os.path.split(productsPath)
    if (os.path.exists(thumbnailPath) == False or os.path.exists(colorsPath) == False or os.path.exists(productsDir[0]) == False):
        print("Path is invalid")
        return
    timeSt = time.time()
    scr = Scraper(mainpage, thumbnailPath, colorsPath, productsPath)
    scr.scrapFull()
    print(time.time() - timeSt)

if __name__ == "__main__":
    main()