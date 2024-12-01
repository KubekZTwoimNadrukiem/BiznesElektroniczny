import time, os, sys

from Scraper import Scraper

def main():
    args = sys.argv
    mainpage = "https://yarnstreet.com/"
    thumbnailPath = os.path.join(os.getcwd(), "images", "thumbnails")
    colorsPath = os.path.join(os.getcwd(), "images")
    logoPath = os.path.join(os.getcwd(), "images", "logos")
    resultPath = os.path.join(os.getcwd(), "results")
    if (len(args) == 6):
        mainpage = args[1]
        thumbnailPath = args[2]
        logoPath = args[3]
        colorsPath = args[4]
        resultPath = args[5]
    if (os.path.exists(thumbnailPath) == False or os.path.exists(colorsPath) == False or os.path.exists(logoPath) == False or os.path.exists(resultPath) == False):
        print("Path is invalid")
        return
    timeSt = time.time()
    scr = Scraper(mainpage, thumbnailPath, colorsPath, logoPath, resultPath)
    scr.scrapFull()
    print(time.time() - timeSt)

if __name__ == "__main__":
    main()