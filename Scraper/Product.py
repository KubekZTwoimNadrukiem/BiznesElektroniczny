class Product:
    def __init__(self, name, href, thumbnail):
        self.name = name
        self.href = href
        self.categories = []
        self.thumbnail = thumbnail
        self.share = None
        self.price = None
        self.stock = None
        self.weigths = None
        self.colors = None
        self.colorsThumbnails = None
        self.colorsImages = None
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
        return self.href == obj.href
    
    def __hash__(self):
        return hash(self.href)