import concurrent.futures as con
import requests as req
from bs4 import BeautifulSoup as bs
import json

from Category import Category
from Product import Product
from InfoEnums import InfoEnum, InfoEnumYarn

class Scraper:
    def __init__(self, mainpage):
        self.mainpage = mainpage
        self.listofcategories = []

    def getHTML(self, url):
        if url == None: return None
        response = req.get(url)
        return bs(response.content, 'html.parser')
    
    def getHTMLlocal(self, filename):
        with open(filename, "r", encoding = "utf-8") as file:
            content = file.read()
        return bs(content, 'html.parser')
    
    def formatString(self,name):
        return name.rstrip().lower()

    def scrapCategory(self, c, isSubcategory):
        soup = self.getHTML(self.mainpage + c.href)
        categoryURL = self.mainpage + (c.href if isSubcategory == True else "")
        while soup != None:
            products = soup.select_one("div#grid").select("div.featured-info")
            for p in products:
                prod = p.select_one("a")
                product = Product(prod.text, prod["href"][1:])
                c.addProduct(product)
                product.addCategory(c)
            try:
                page = soup.select_one("ul.pagination").select_one("li.active + li").select_one("a")
            except:
                break
            soup = self.getHTML(categoryURL + page["href"])

    def threadSubcategory(self, params):
        print("\t" + params[0].text)
        subcategory = Category(self.formatString(params[0].text), params[0]["href"][1:], [])
        self.scrapCategory(subcategory, True)
        params[1].append(subcategory)

    def threadCategory(self, c):
        print(c.text)
        subcategories = c.find_next_sibling("div").select("a.title")
        listofsubcategories = []
        params = [(s, listofsubcategories) for s in subcategories]
        with con.ThreadPoolExecutor(max_workers = len(subcategories)) as executor:
            executor.map(self.threadSubcategory, params)
        category = Category(self.formatString(c.text), c["href"][1:], listofsubcategories)
        self.scrapCategory(category, False)
        self.listofcategories.append(category)

    def getCategories(self):
        soup = self.getHTML(self.mainpage)
        if soup == None: return None
        categorymenu = soup.select_one("div.sidebar-menu" )
        categories = categorymenu.find_all("a", attrs = { "class": "" })
        with con.ThreadPoolExecutor(max_workers = len(categories)) as executor:
            executor.map(self.threadCategory, categories)
        for c in self.listofcategories:
            for s in c.subcategories:
                c.products = list(set(c.products) - set(s.products))

    def scrapProduct(self, params):
        p = params[0]
        soup = self.getHTML(self.mainpage + p.href)
        if soup == None: return
        product = soup.select_one("div.single-products")
        #productImage = product.select_one()
        productDetails = product.select_one("div.single-product-details")
        productInfo = product.select_one("div#content-product-review").select_one("div#my-tab-content")
        info1 = productInfo.select_one("div#info1 > table > tbody").select("tr")
        info2 = productInfo.select_one("div#info2 > p")
        p.price = productDetails.select_one("h2 > span").text
        p.stock = productDetails.select_one("p.sin-item > span").text
        if params[1] == False:
            p.brand = info1[InfoEnum.BRAND.value].select("td")[1].text
            p.weigth = info1[InfoEnum.WEIGTH.value].select("td")[1].text
            p.length = info1[InfoEnum.LENGTH.value].select("td")[1].text
            p.country = info1[InfoEnum.COUNTRY.value].select("td")[1].text
        else:
            p.brand = info1[InfoEnumYarn.BRAND.value].select("td")[1].text
            p.composition = info1[InfoEnumYarn.COMPOSITION.value].select("td")[1].text
            p.weigth = info1[InfoEnumYarn.WEIGTH.value].select("td")[1].text
            p.length = info1[InfoEnumYarn.LENGTH.value].select("td")[1].text
            if len(info1) == len(InfoEnumYarn):
                p.needleSize = info1[InfoEnumYarn.NEEDLE_SIZE_OR_COUNTRY.value].select("td")[1].text
                p.crochetSize = info1[InfoEnumYarn.CROCHET_SIZE.value].select("td")[1].text
                p.country = info1[InfoEnumYarn.COUNTRY.value].select("td")[1].text
            else:
                weigths = productDetails.select_one("select#productWeight").select("option")
                weigths = weigths[1:]
                p.weigths = [w.text for w in weigths]
                p.country = info1[InfoEnumYarn.NEEDLE_SIZE_OR_COUNTRY.value].select("td")[1].text
        p.description = info2.text
        # TODO: colors and pictures

    def threadProduct(self, params):
        for p in params[0].products:
            self.scrapProduct(p, params[1])

    def getProducts(self):
        for c in self.listofcategories:
            isYarn = False
            if c.name == "yarns": isYarn = True
            '''
            for p in c.products:
                self.scrapProduct(p, isYarn)
            params = [(s, isYarn) for s in c.subcategories]
            with con.ThreadPoolExecutor(max_workers = len(c.subcategories)) as executor:
                executor.map(self.threadProduct, params)
            '''
            params = [(p, isYarn) for p in c.products]
            if len(c.products) > 0:
                with con.ThreadPoolExecutor(max_workers = len(c.products)) as executor:
                    executor.map(self.scrapProduct, params)
            for s in c.subcategories:
                params = [(p, isYarn) for p in s.products]
                with con.ThreadPoolExecutor(max_workers = len(s.products)) as executor:
                    executor.map(self.scrapProduct, params)
            
    def toJSON(self, obj):
        return obj.__dict__
    
    def saveToJSON(self, content, filename):
        if content == None or filename == None: return
        with open(filename, "w", encoding = "utf-8") as f:     
            json.dump(content, f, ensure_ascii = False, default = self.toJSON)
            
    def statistics(self):
        for c in self.listofcategories:
            sum = 0
            for s in c.subcategories:
                print("\t" + s.name + " (" + str(len(s.products)) + ")")
                sum = sum + len(s.products)
            print(c.name + " (" + str(len(c.products)) + ") in subcategories (" + str(sum) + ")")