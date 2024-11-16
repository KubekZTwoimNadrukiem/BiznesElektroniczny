class Product:
    def __init__(self, name, href):
        self.name = name
        self.href = href
        self.categories = []
        self.price = None
        self.stock = None
        self.weigths = None
        self.brand = None
        self.composition = None
        self.weigth = None
        self.length = None
        self.needleSize = None
        self.crochetSize = None
        self.country = None
        self.description = None

    def addCategory(self, category):
        self.categories.append(category)

    def __eq__(self, obj):
        if not isinstance(obj, Product):
            return NotImplemented
        return self.name == obj.name
    
    def __hash__(self):
        return hash(self.name)