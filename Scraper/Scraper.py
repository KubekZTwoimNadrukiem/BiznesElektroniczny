import concurrent.futures as con
import requests as req
from bs4 import BeautifulSoup as bs
import json, os

from Category import Category
from Product import Product
from Brand import Brand
from InfoEnums import InfoEnum, InfoEnumYarn

class Scraper:
    def __init__(self, mainpage, thumbnailsPath, colorsPath, logoPath, resultPath):
        self.mainpage = mainpage
        self.thumbnailPath = thumbnailsPath
        self.colorsPath = colorsPath
        self.logoPath = logoPath
        self.resultPath = resultPath
        self.listofcategories = []
        self.listofproducts = list()
        self.listofbrands = []

    def getHTML(self, url):
        if url == None: return None
        response = req.get(url)
        return bs(response.content, 'html.parser')
    
    def getHTMLlocal(self, filename):
        with open(filename, "r", encoding = "utf-8") as file:
            content = file.read()
        return bs(content, 'html.parser')
    
    def toJSON(self, obj):
        return obj.__dict__
    
    def formatString(self,name):
        return name.rstrip().lower()
    
    def removeDuplicate(self, p):
        if p in self.listofproducts:
            for l in self.listofproducts:
                if l == p:
                    l.categories += p.categories
                    break
        else:
            self.listofproducts.append(p)

    def onlyCategories(self):
        list = []
        for c in self.listofcategories:
            subc = []
            for s in c.subcategories:
                subc.append(s.name)
            list.append([c.name, subc])
        return list

    def scrapCategory(self, c, isSubcategory):
        soup = self.getHTML(self.mainpage + c.href)
        categoryURL = self.mainpage + (c.href if isSubcategory == True else "")
        while soup != None:
            products = soup.select_one("div#grid").select("div.featured-inner")
            for p in products:
                prod = p.select_one("div.featured-info").select_one("a")
                img = p.select_one("div.featured-image").select_one("img")
                product = Product(prod.text, prod["href"][1:], img["src"])
                c.addProduct(product)
                product.addCategory(c.name)
            try:
                page = soup.select_one("ul.pagination").select_one("li.active + li").select_one("a")
            except:
                break
            soup = self.getHTML(categoryURL + page["href"])

    def threadSubcategory(self, s):
        subcategory = Category(self.formatString(s.text), s["href"][1:], [])
        self.scrapCategory(subcategory, True)
        return subcategory

    def threadCategory(self, c):
        subcategories = c.find_next_sibling("div").select("a.title")
        listofsubcategories = []
        with con.ThreadPoolExecutor() as executor: #max_workers = len(subcategories)
            for f in executor.map(self.threadSubcategory, subcategories):
                listofsubcategories.append(f)
        category = Category(self.formatString(c.text), c["href"][1:], listofsubcategories)
        self.scrapCategory(category, False)
        self.listofcategories.append(category)

    def getCategories(self):
        soup = self.getHTML(self.mainpage)
        if soup == None: return None
        categorymenu = soup.select_one("div.sidebar-menu" )
        categories = categorymenu.find_all("a", attrs = { "class": "" })
        with con.ThreadPoolExecutor() as executor: #max_workers = len(categories)
            executor.map(self.threadCategory, categories)
        for c in self.listofcategories:
            for s in c.subcategories:
                c.products = list(set(c.products) - set(s.products))

    def scrapProduct(self, params):
        p = params[0]
        soup = self.getHTML(self.mainpage + p.href)
        if soup == None: return
        product = soup.select_one("div.single-products")
        productDetails = product.select_one("div.single-product-details")
        productShare = product.select_one("div.sin-social").select("a")
        productColorsImages = product.select_one("div.single-product-image").select_one("div#my-tab-content").select("a")
        productInfo = product.select_one("div#content-product-review").select_one("div#my-tab-content")
        info1 = productInfo.select_one("div#info1 > table > tbody").select("tr")
        info2 = productInfo.select_one("div#info2 > p")
        try:
            p.stock = productDetails.select_one("p.sin-item > span").text
            productColors = product.select_one("select#selectProductSort1").select("option")
            productColors = productColors[1:]
            p.colors = [c.text for c in productColors]
            p.colorsImages = [i["href"][1:] for i in productColorsImages]
        except:
            p.stock = 0
            p.colorsImages = [[i["title"], i.select_one("img")["src"][len(self.mainpage):]] for i in productColorsImages]
        p.price = productDetails.select_one("h2 > span").text
        p.share = [l["href"] for l in productShare]
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
            elif len(info1) == len(InfoEnumYarn) - 1:
                p.needleSize = info1[InfoEnumYarn.NEEDLE_SIZE_OR_COUNTRY.value].select("td")[1].text
                p.country = info1[InfoEnumYarn.CROCHET_SIZE.value].select("td")[1].text
            elif len(info1) == len(InfoEnumYarn) - 2:
                p.country = info1[InfoEnumYarn.NEEDLE_SIZE_OR_COUNTRY.value].select("td")[1].text
            else:
                if (p.stock != 0):
                    weigths = productDetails.select_one("select#productWeight").select("option")
                    weigths = weigths[1:]
                    p.weigths = [w.text for w in weigths]
                p.country = info1[InfoEnumYarn.NEEDLE_SIZE_OR_COUNTRY.value].select("td")[1].text
        p.description = info2.text

    def threadProduct(self, params):
        for p in params[0].products:
            self.scrapProduct(p, params[1])

    def getProducts(self):
        for c in self.listofcategories:
            isYarn = False
            if c.name == "yarns": isYarn = True
            params = [(p, isYarn) for p in c.products]
            if len(c.products) > 0:
                with con.ThreadPoolExecutor() as executor: #max_workers = len(c.products)
                    executor.map(self.scrapProduct, params)
            for s in c.subcategories:
                params = [(p, isYarn) for p in s.products]
                with con.ThreadPoolExecutor() as executor: #max_workers = len(s.products)
                    executor.map(self.scrapProduct, params)
        for c in self.listofcategories:
            for p in c.products:
                self.removeDuplicate(p)
            for s in c.subcategories:
                for p in s.products:
                    self.removeDuplicate(p)
                    p.categories.append(c.name)

    def threadBrand(self, b):
        href = b["href"][1:]
        soup = self.getHTML(self.mainpage + href)
        if soup == None: return
        br = soup.select_one("div.categori-content")
        logo = None
        try:
            logo = br.select_one("div.brand-banner > img")["src"]
        except:
            pass
        brand = Brand(br.select_one("h1").text.strip(), href, logo)
        self.listofbrands.append(brand)

    def getBrands(self):
        soup = self.getHTML(self.mainpage)
        if soup == None: return
        brands = soup.select_one("div.brand-and-client").select_one("div.brand-logo").select("div.clients")
        brands = [b.select_one("a") for b in brands]
        with con.ThreadPoolExecutor() as executor: #max_workers = len(brands)
            executor.map(self.threadBrand, brands)

    def threadImage(self, p):
        img = req.get(p.thumbnail)
        thumbnailPath = os.path.join(self.thumbnailPath, p.href.split("/")[-1] + "." + p.thumbnail.split(".")[-1])
        with open(thumbnailPath, "wb") as f:
            f.write(img.content)
        colorsPath = os.path.join(self.colorsPath, p.href.split("/")[-1])
        if (os.path.exists(colorsPath) == False):
            os.mkdir(colorsPath)
        i = 0
        for c in p.colorsImages:
            img2 = req.get(self.mainpage + c)
            with open(os.path.join(colorsPath, p.colors[i].replace("/", "-") + "." + c.split(".")[-1]), "wb") as f:
                f.write(img2.content)
            i = i + 1

    def threadLogo(self, b):
        img = req.get(b.image)
        logoPath = os.path.join(self.logoPath, b.image.split("/")[-1])
        with open(logoPath, "wb") as f:
            f.write(img.content)

    def saveToJSON(self, content, filename):
        with open(os.path.join(self.resultPath, filename), "w", encoding = "utf-8") as f:     
            json.dump(content, f, ensure_ascii = False, default = self.toJSON)

    def downloadImages(self, function, content):
        with con.ThreadPoolExecutor() as executor: #max_workers = len(self.listofproducts)
            executor.map(function, content)
    
    def scrapFull(self):
        self.getCategories()
        self.saveToJSON(self.onlyCategories(), "categories.json")
        self.getBrands()
        self.saveToJSON(self.listofbrands, "brands.json")
        self.downloadImages(self.threadLogo, self.listofbrands)
        self.getProducts()
        self.saveToJSON(self.listofproducts, "products.json")
        self.downloadImages(self.threadImage, self.listofproducts)
            
    def statistics(self):
        for c in self.listofcategories:
            sum = 0
            for s in c.subcategories:
                print("\t" + s.name + " (" + str(len(s.products)) + ")")
                sum = sum + len(s.products)
            print(c.name + " (" + str(len(c.products)) + ") in subcategories (" + str(sum) + ")")
        print("Total products without duplicates (" + str(len(self.listofproducts)) + ")")