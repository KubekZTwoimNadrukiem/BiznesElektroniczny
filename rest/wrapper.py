from api import API
from utils import encode_key, get_endpoints
import json

class Wrapper:
    def __init__(self, key, api_url):
        encoded_key = encode_key(username = key)
        headers = {"Authorization": f"Basic {encoded_key}"}
        self.euro_conversion = 4.29
        self.api_url = api_url
        self.api = API(headers)
        self.api.init(self.api_url)

    
    def add_product_option(self, name):
        if not self.api.does_product_option_exist(name):
            print(f"Adding product option {name}.")
            return self.api.add_product_option(name)
        else:
            print(f"Product option {name} already exists.")
            return self.api.get_product_option_id(name)

    
    def add_tax(self, rate):
        if not self.api.does_tax_exist(23):
            print("Adding tax 23%.")
            return self.api.add_tax(23)
        else:
            print("Tax 23% already exists.")
            return self.api.get_tax_id(23)


    def add_product_option_value(self, name, option_id):
        if not self.api.does_product_option_value_exist(name, option_id):
            print(f"Adding product option value {name}.")
            return self.api.add_product_option_value(name, option_id)
        else:
            print(f"Product option value {name} already exists.")
            return self.api.get_product_option_value_id(name, option_id)


    def add_product_feature(self, name):
        if not self.api.does_product_feature_exist(name):
            print(f"Adding product feature {name}.")
            return self.api.add_product_feature(name)
        else:
            print(f"Product feature {name} already exists.")
            return self.api.get_product_feature_id(name)

    
    def add_product_feature_value(self, name, feature_id):
        if not self.api.does_product_feature_value_exist(name, feature_id):
            print(f"Adding product feature value {name}.")
            return self.api.add_product_feature_value(name, feature_id)
        else:
            print(f"Product feature value {name} already exists.")
            return self.api.get_product_feature_value_id(name, feature_id)


    def load_brands(self, path, image_path):
        with open(path) as f:
            brands = json.load(f)
            for brand in brands:
                name = brand["name"]
                link = brand["href"].replace("brands/", "")
                tmp_name = brand["image"]
                if tmp_name == None:
                    filename = ""
                else:
                    filename = tmp_name.split("/")[-1]
                if self.api.does_manufacturer_exist(name):
                    print(f"Manufacturer {name} already exists.")
                    id = self.api.get_manufacturer_id(name)
                    if filename != "":
                        print(f"Image available for {name}, adding.")
                        self.api.add_image(image_path + filename, "manufacturers", id)
                    continue
                else:
                    id = self.api.add_manufacturer(name)
                    if filename != "":
                        self.api.add_image(image_path + filename, "manufacturers", id)
            #for brand in brands:
            #    self.api.add_manufacturer(brand)


    def load_products(self, path):
        color_id = self.add_product_option("Color")
        tax_id = self.add_tax(23)
        composition_id = self.add_product_feature("Composition")
        length_id = self.add_product_feature("Length")
        needle_id = self.add_product_feature("Needle Size (mm)")
        crochet_id = self.add_product_feature("Crochet Size (mm)")
        country_id = self.add_product_feature("Country")
        
        print(self.add_product_option_value("Black", color_id))
        with open(path) as f:
            products = json.load(f)
            #print(products)
            #print(products[1])
            for product in products[:1]:
                name = product["name"].title()
                #print(name)
                price = round(float(product["price"].replace("€", "")) * self.euro_conversion, 2)
                manufacturer = product["brand"]
                manufacturer_id = self.api.get_manufacturer_id(manufacturer)
                categories = product["categories"]
                category_ids = []
                for category in categories:
                    category_ids.append(self.api.get_category_id(category.title()))
                colors = product["colors"]
                color_stock = []
                if colors != None:
                    for color in colors:
                        separate = color.split(" ")
                        stock = int(separate[-2])
                        color_stock.append(stock)
                composition = product["composition"]
                country = product["country"]
                description = product["description"].replace(
                    r"\r\n", "\n"
                )
                weight = product["weigth"]
                length = product["length"]
                needleSize = product["needleSize"]
                crochetSize = product["crochetSize"]
                if weight != None:
                    #print(weight, name)
                    if weight.strip() == "PLASTIC 100%" or weight.strip() == "POLYESTER 100%" or weight.strip() == "ACRYLIC 100%" or weight.strip() == "POLYAMIDE 100%" or weight.strip() == "POLYAMIDE 20% POLYESTER 80%":
                        weight_value = float(product["length"].split(" ")[0])
                        composition = product["weigth"]
                        length = product["country"]
                        country = None
                    else:
                        weight_value = float(weight.split(" ")[0])
                else:
                    weight_value = None
                #weigths = product["weigths"]
                colorsImages = product["colorsImages"]
                if (type(colorsImages[0]) == list):
                    continue
                if composition != None:
                    composition_value_id = self.add_product_feature_value(composition, composition_id)
                else:
                    composition_value_id = None
                if length != None:
                    length_value_id = self.add_product_feature_value(length, length_id)
                else:
                    length_value_id = None
                if needleSize != None:
                    needleSize_value_id = self.add_product_feature_value(needleSize, needle_id)
                else:
                    needleSize_value_id = None
                if crochetSize != None:
                    crochetSize_value_id = self.add_product_feature_value(crochetSize, crochet_id)
                else:
                    crochetSize_value_id = None
                if country != None:
                    country_value_id = self.add_product_feature_value(country, country_id)
                else:
                    country_value_id = None
                product_id = self.api.add_product(name, price, manufacturer_id, category_ids, tax_id, description, weight=weight_value, composition_id = composition_id, length_id = length_id, needle_id = needle_id, crochet_id = crochet_id, country_id = country_id, composition_value_id = composition_value_id, length_value_id = length_value_id, needle_value_id = needleSize_value_id, crochet_value_id = crochetSize_value_id,country_value_id=country_value_id)
                for i in range(len(colors)):
                    color_option_id = self.add_product_option_value(colors[i], color_id)
                    combination_id = self.api.add_combination(product_id, price, color_option_id)
                    self.api.update_combination_stock(combination_id, color_stock[i])
                    #self.api.add_image(colorsImages[i], "products", product_id)
                print(product_id)

                
            


    def load_categories(self, path):
        with open(path) as f:
            categories = json.load(f)
            #print(categories)
            for category in categories:
                name = category[0].title()
                subcategories = category[1]
                if self.api.does_category_exist(name, 1):
                    print(f"Category {name} already exists.")
                    id = self.api.get_category_id(name)
                else:
                    print(f"Adding category {name}.")
                    id = self.api.add_category(name)

                for subcategory in subcategories:
                    sub_name = subcategory.title()
                    if self.api.does_category_exist(sub_name, 2):
                        print(f"Category {sub_name} already exists.")
                    else:
                        print(f"Adding category {sub_name}.")
                        sub_id = self.api.add_category(sub_name, id)


    def load_data(self, path):
        #self.load_brands(path + "results/brands.json", path + "images/logos/")
        self.load_categories(path + "results/categories.json")
        self.load_products(path + "results/products.json")
        pass