import copy

class Category:
    def __init__(self, name, href, subcategories):
        self.name = name
        self.href = href
        self.subcategories = subcategories
        self.products = []

    def addProduct(self, product):
        self.products.append(product)