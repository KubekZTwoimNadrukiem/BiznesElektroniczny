import requests as req
from bs4 import BeautifulSoup as bs
import json

from Category import Category
from Product import Product

class Scraper:
    def __init__(self, mainpage):
        self.mainpage = mainpage
        self.listofcategories = []

    def getHTML(self, url):
        if url == None:
            return None
        response = req.get(url)
        return bs(response.content, 'html.parser')
    
    def getHTMLlocal(self, filename):
        with open(filename, "r", encoding = "utf-8") as file:
            content = file.read()
        return bs(content, 'html.parser')
    
    def getCategories(self):
        soup = self.getHTML(self.mainpage)
        if soup == None:
            return None
        categorymenu = soup.select_one("div.sidebar-menu" )
        categories = categorymenu.find_all("a", attrs = { "class": "" })
        for c in categories:
            print(c.text)
            subcategories = c.find_next_sibling("div").select("a.title")
            listofsubcategories = []
            for s in subcategories:
                print("\t" + s.text)
                subcategory = Category(s.text.rstrip().lower(), s["href"][1:], [])
                self.scrapSubcategory(subcategory)
                listofsubcategories.append(subcategory)
            category = Category(c.text.rstrip().lower(), c["href"][1:], listofsubcategories)
            self.scrapCategory(category)
            self.listofcategories.append(category)
    
    def scrapCategory(self, c):
        soup = self.getHTML(self.mainpage + c.href)
        while soup != None:
            products = soup.select_one("div#grid").select("div.featured-info")
            for p in products:
                prod = p.select_one("a")
                product = Product(prod.text, prod["href"])
                c.addProduct(product)
                product.addCategory(c)
            try:
                page = soup.select_one("ul.pagination").select_one("li.active + li").select_one("a")
            except:
                break
            soup = self.getHTML(self.mainpage + page["href"]) # without c.href
            
    def scrapSubcategory(self, s):
        soup = self.getHTML(self.mainpage + s.href)
        while soup != None:
            products = soup.select_one("div#grid").select("div.featured-info")
            for p in products:
                prod = p.select_one("a")
                product = Product(prod.text, prod["href"])
                s.addProduct(product)
                product.addCategory(s)
            try:
                page = soup.select_one("ul.pagination").select_one("li.active + li").select_one("a")
            except:
                break
            soup = self.getHTML(self.mainpage + s.href + page["href"])
            
    def toJSON(self, obj):
        return obj.__dict__
    
    def saveToJSON(self, content, filename):
        if content == None or filename == None:
            return
        with open(filename, "w", encoding = "utf-8") as f:     
            json.dump(content, f, ensure_ascii = False, default = self.toJSON)
            
    def statistics(self):
        for c in self.listofcategories:
            sum = 0
            for s in c.subcategories:
                print("\t" + s.name + " (" + str(len(s.products)) + ")")
                sum = sum + len(s.products)
            print(c.name + " (" + str(len(c.products)) + ") in subcategories (" + str(sum) + ")")