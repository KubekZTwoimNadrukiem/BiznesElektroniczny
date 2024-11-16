class Product:
    def __init__(self, name, href):
        self.name = name
        self.href = href
        self.categories = []

    def addCategory(self, category):
        self.categories.append(category)

    def __eq__(self, obj):
        if not isinstance(obj, Product):
            return NotImplemented
        return self.name == obj.name