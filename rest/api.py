import requests
from bs4 import BeautifulSoup, CData
from utils import get_endpoints

class API:
    def __init__(self, auth_header):
        self.endpoints = {}
        self.auth_header = auth_header


    def init(self, api_url):
        endpoints = get_endpoints(api_url, self.auth_header)
        for name, endpoint in endpoints.items():
            print(f"Adding endpoint: {name}")
            self.add_endpoint(endpoint)


    def add_endpoint(self, endpoint):
        self.endpoints[endpoint.name] = endpoint


    def get_shops(self):
        return requests.get(self.endpoints['shops'].path, headers=self.auth_header)


    def get_product_feature_id(self, name):
        product_features = requests.get(self.endpoints['product_features'].path, headers=self.auth_header)
        bs_product_features = BeautifulSoup(product_features.text, "xml")
        for product_feature in bs_product_features.find_all("product_feature"):
            product_feature_data = requests.get(product_feature.attrs["xlink:href"], headers=self.auth_header)
            bs_product_feature_data = BeautifulSoup(product_feature_data.text, "xml")
            id_t = bs_product_feature_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_product_feature_data.find("name")
            for language in name_t.find_all("language"):
                if language.get_text().strip() == name.strip():
                    return id_value
        
        return -1
    

    def does_product_feature_exist(self, name):
        return self.get_product_feature_id(name) != -1


    def add_product_feature(self, name):
        blank = requests.get(self.endpoints['product_features'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        name_t = bs_blank.find("name")
        name_languages = name_t.find_all("language")
        for language in name_languages:
            language.string = CData(name)
        position = bs_blank.find("position")
        position.extract()
        status = requests.post(self.endpoints['product_features'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add product feature {name}")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        feature_id = bs_status.find("id")
        added_id = int(feature_id.get_text())
        return added_id
    

    def get_product_feature_value_id(self, name, feature_id):
        product_feature_values = requests.get(self.endpoints['product_feature_values'].path, headers=self.auth_header)
        bs_product_feature_values = BeautifulSoup(product_feature_values.text, "xml")
        for product_feature_value in bs_product_feature_values.find_all("product_feature_value"):
            product_feature_value_data = requests.get(product_feature_value.attrs["xlink:href"], headers=self.auth_header)
            bs_product_feature_value_data = BeautifulSoup(product_feature_value_data.text, "xml")
            id_t = bs_product_feature_value_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_product_feature_value_data.find("value")
            for language in name_t.find_all("language"):
                if language.get_text().strip() == name.strip():
                    id_feature = bs_product_feature_value_data.find("id_feature")
                    if int(id_feature.get_text()) == feature_id:
                        return id_value
        
        return -1
    

    def does_product_feature_value_exist(self, name, feature_id):
        return self.get_product_feature_value_id(name, feature_id) != -1

    
    def add_product_feature_value(self, name, feature_id):
        blank = requests.get(self.endpoints['product_feature_values'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        id_feature_t = bs_blank.find("id_feature")
        id_feature_t.string = str(feature_id)
        custom = bs_blank.find("custom")
        custom.string = "0"
        value = bs_blank.find("value")
        value_languages = value.find_all("language")
        for language in value_languages:
            language.string = CData(name)
        status = requests.post(self.endpoints['product_feature_values'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add product feature value {name}")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        value_id = bs_status.find("id")
        added_id = int(value_id.get_text())
        return added_id


    def get_category_id(self, category, level_depth = None):
        categories = requests.get(self.endpoints['categories'].path, headers=self.auth_header)
        bs_categories = BeautifulSoup(categories.text, "xml")
        for category_t in bs_categories.find_all("category"):
            category_data = requests.get(category_t.attrs["xlink:href"], headers=self.auth_header)
            bs_category_data = BeautifulSoup(category_data.text, "xml")
            id_t = bs_category_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_category_data.find("name")
            for language in name_t.find_all("language"):
                #print(language.get_text())
                if language.get_text().strip() == category.strip():
                    level_depth_t = bs_category_data.find("level_depth")
                    if level_depth == None:
                        return id_value
                    if int(level_depth_t.get_text()) == level_depth:
                        return id_value
        return -1


    def does_category_exist(self, category, level_depth = None):
        return self.get_category_id(category, level_depth) != -1


    def add_category(self, category, parent_id = 0):
        blank = requests.get(self.endpoints['categories'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        for t in ["level_depth", "nb_products_recursive", "position", "date_add", "date_upd",
                  "meta_keywords", "meta_description"]:
            for s in bs_blank.select(t):
                s.extract()
        name = bs_blank.find("name")
        name_languages = name.find_all("language")
        for language in name_languages:
            language.string = CData(category)
        is_root_category = bs_blank.find("is_root_category")
        if parent_id == 0:
            is_root_category.string = "1"
        else:
            is_root_category.string = "0"
        id_shop_default = bs_blank.find("id_shop_default")
        id_shop_default.string = "1"
        parent = bs_blank.find("id_parent")
        parent.string = str(parent_id)
        active = bs_blank.find("active")
        active.string = "1"
        link_rewrite = bs_blank.find("link_rewrite")
        link_rewrite_languages = link_rewrite.find_all("language")
        for language in link_rewrite_languages:
            language.string = CData(category.lower().replace(" ", "-"))
        status = requests.post(self.endpoints['categories'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print("Failed to add category.")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        category_id = bs_status.find("id")
        added_id = int(category_id.get_text())
        return added_id


    def get_tax_id(self, rate, country = "PL"):
        blank = requests.get(self.endpoints['taxes'].path, headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        taxes = bs_blank.find_all("tax")
        for tax in taxes:
            tax_data = requests.get(tax.attrs["xlink:href"], headers=self.auth_header)
            bs_tax_data = BeautifulSoup(tax_data.text, "xml")
            id_t = bs_tax_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_tax_data.find("name")
            for language in name_t.find_all("language"):
                if country in language.get_text().strip():
                    rate_t = bs_tax_data.find("rate")
                    if float(rate_t.get_text()) == float(rate):
                        return id_value
        
        return -1


    def does_tax_exist(self, rate, country = "PL"):
        return self.get_tax_id(rate, country) != -1


    def add_tax(self, rate, country = "PL"):
        blank = requests.get(self.endpoints['taxes'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        print(bs_blank.prettify())
        name = bs_blank.find("name")
        name_languages = name.find_all("language")
        for language in name_languages:
            language.string = CData(f"PTU {rate}% {country}")
        rate_t = bs_blank.find("rate")
        rate_t.string = str(float(rate))
        active = bs_blank.find("active")
        active.string = "1"
        status = requests.post(self.endpoints['taxes'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print("Failed to add tax.")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        tax_id = bs_status.find("id")
        added_id = int(tax_id.get_text())
        return added_id

    def get_manufacturer_id(self, manufacturer):
        manufacturers = requests.get(self.endpoints['manufacturers'].path, headers=self.auth_header)
        bs_manufacturers = BeautifulSoup(manufacturers.text, "xml")
        for manufacturer_t in bs_manufacturers.find_all("manufacturer"):
            manufacturer_data = requests.get(manufacturer_t.attrs["xlink:href"], headers=self.auth_header)
            bs_manufacturer_data = BeautifulSoup(manufacturer_data.text, "xml")
            id_t = bs_manufacturer_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_manufacturer_data.find("name")
            if name_t.get_text().strip() == manufacturer.strip():
                return id_value
        
        return -1


    def does_manufacturer_exist(self, manufacturer):
        return self.get_manufacturer_id(manufacturer) != -1


    def add_manufacturer(self, name):
        blank = requests.get(self.endpoints['manufacturers'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        to_remove = ["date_add", "date_upd", "meta_title", "meta_description", "meta_keywords", "description",
                  "associations", "short_description", "link_rewrite"]
        for t in to_remove:
            for s in bs_blank.select(t):
                s.extract()
        name_t = bs_blank.find("name")
        name_t.string = CData(name)
        active = bs_blank.find("active")
        active.string = "1"
        #print(bs_blank.prettify())
        status = requests.post(self.endpoints['manufacturers'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add manufacturer {name}")
            return -1
        
        bs_status = BeautifulSoup(status.text, "xml")
        manufacturer_id = bs_status.find("id")
        added_id = int(manufacturer_id.get_text())
        return added_id


    def get_supplier_id(self, name):
        suppliers = requests.get(self.endpoints['suppliers'].path, headers=self.auth_header)
        bs_suppliers = BeautifulSoup(suppliers.text, "xml")
        for supplier in bs_suppliers.find_all("supplier"):
            supplier_data = requests.get(supplier.attrs["xlink:href"], headers=self.auth_header)
            bs_supplier_data = BeautifulSoup(supplier_data.text, "xml")
            id_t = bs_supplier_data.findChild("id")
            id_value = int(id_t.get_text())
            if bs_supplier_data.find("name").string == name:
                return id_value
            
        return -1
    

    def does_supplier_exist(self, name):
        return self.get_supplier_id(name) != -1


    def add_supplier(self, name, description):
        blank = requests.get(self.endpoints['suppliers'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        for t in ["date_add", "date_upd", "meta_title", "meta_description", "meta_keywords"]:
            for s in bs_blank.select(t):
                s.extract()
        link_rewrite = bs_blank.find("link_rewrite")
        link_rewrite.string = CData(name.lower())
        name_t = bs_blank.find("name")
        name_t.string = CData(name)
        active = bs_blank.find("active")
        active.string = "1"
        description_t = bs_blank.find("description")
        description_languages = description_t.find_all("language")
        for language in description_languages:
            language.string = CData(description)
        status = requests.post(self.endpoints['suppliers'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add category ({name}) - status code:", status.status_code)
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        supplier_id = bs_status.find("id")
        print(supplier_id)

    def add_combination(self, product_id, price, product_option_value_id):
        print(f"Adding combination {product_option_value_id} to {product_id}")
        blank = requests.get(self.endpoints['combinations'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        to_remove = ["location", "ean13", "upc", "isbn", "mpn", "reference", "supplier_reference", "wholesale price", "ecotax", "weight",
                     "unit_price_impact", "low_stock_threshold", "low_stock_alert", "available_date", "images", "wholesale_price", "quantity"]
        for t in to_remove:
            for s in bs_blank.select(t):
                s.extract()
        id_product = bs_blank.find("id_product")
        id_product.string = str(product_id)
        price_t = bs_blank.find("price")
        price_t.string = str(price)
        minimal_quantity = bs_blank.find("minimal_quantity")
        minimal_quantity.string = "1"
        default_on = bs_blank.find("default_on")
        default_on.string = "0"
        product_option_value = bs_blank.find("product_option_value")
        option_id = bs_blank.new_tag("id")
        option_id.string = str(product_option_value_id)
        product_option_value.append(option_id)
        #print(bs_blank.prettify())
        status = requests.post(self.endpoints['combinations'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add combination {product_option_value_id} - status code:", status.status_code)
            print(status.text)
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        combination_id = bs_status.find("id")
        added_id = int(combination_id.get_text())
        return added_id


    def add_image(self, image_path, category, id):
        blank = requests.get(self.endpoints['images'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        tag = bs_blank.find(category)
        address = f"{tag.attrs['xlink:href']}/{id}"
        try:
            file = open(image_path, "rb")
        except FileNotFoundError:
            print(f"File not found: {image_path}")
            return
        except Exception as e:
            print(f"Error opening file: {e}")
            return
        mime_type = "image/jpeg"
        filename = image_path.split("/")[-1]
        files = {"image": (filename, file, mime_type)}
        response = requests.post(address, headers=self.auth_header, files=files)
        print(response.status_code)
        #print(response.text)
    

    def get_product_option_id(self, name):
        product_options = requests.get(self.endpoints['product_options'].path, headers=self.auth_header)
        bs_product_options = BeautifulSoup(product_options.text, "xml")
        for product_option in bs_product_options.find_all("product_option"):
            product_option_data = requests.get(product_option.attrs["xlink:href"], headers=self.auth_header)
            bs_product_option_data = BeautifulSoup(product_option_data.text, "xml")
            id_t = bs_product_option_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_product_option_data.find("name")
            for language in name_t.find_all("language"):
                if language.get_text().strip() == name.strip():
                    return id_value
        
        return -1

    
    def does_product_option_exist(self, name):
        return self.get_product_option_id(name) != -1

    
    def add_product_option(self, name):
        #print(f"Adding product option {name}")
        blank = requests.get(self.endpoints['product_options'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        name_t = bs_blank.find("name")
        for language in name_t.find_all("language"):
            language.string = CData(name)
        group_type = bs_blank.find("group_type")
        group_type.string = CData("select")
        public_name = bs_blank.find("public_name")
        for language in public_name.find_all("language"):
            language.string = CData(name)
        is_color_group = bs_blank.find("is_color_group")
        is_color_group.string = "0"
        associations = bs_blank.find("associations")
        associations.extract()
        position = bs_blank.find("position")
        position.extract()
        status = requests.post(self.endpoints['product_options'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add product option {name}")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        option_id = bs_status.find("id")
        added_id = int(option_id.get_text())
        return added_id

    
    def get_product_option_value_id(self, name, option_id):
        product_option_values = requests.get(self.endpoints['product_option_values'].path, headers=self.auth_header)
        bs_product_option_values = BeautifulSoup(product_option_values.text, "xml")
        for product_option_value in bs_product_option_values.find_all("product_option_value"):
            product_option_value_data = requests.get(product_option_value.attrs["xlink:href"], headers=self.auth_header)
            bs_product_option_value_data = BeautifulSoup(product_option_value_data.text, "xml")
            id_t = bs_product_option_value_data.findChild("id")
            id_value = int(id_t.get_text())
            name_t = bs_product_option_value_data.find("name")
            for language in name_t.find_all("language"):
                if language.get_text().strip() == name.strip():
                    id_attribute_group = bs_product_option_value_data.find("id_attribute_group")
                    if int(id_attribute_group.get_text()) == option_id:
                        return id_value
        
        return -1

    
    def does_product_option_value_exist(self, name, option_id):
        return self.get_product_option_value_id(name, option_id) != -1

    
    def add_product_option_value(self, name, option_id):
        print(f"Adding product option value {name}")
        blank = requests.get(self.endpoints['product_option_values'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        id_attribute_group = bs_blank.find("id_attribute_group")
        id_attribute_group.string = str(option_id)
        color = bs_blank.find("color")
        color.extract()
        position = bs_blank.find("position")
        position.extract()
        name_t = bs_blank.find("name")
        for language in name_t.find_all("language"):
            language.string = CData(name)
        status = requests.post(self.endpoints['product_option_values'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add product option value {name}")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        value_id = bs_status.find("id")
        added_id = int(value_id.get_text())
        return added_id


    def update_combination_stock(self, combination_id, quantity):
        blank = requests.get(self.endpoints['stock_availables'].path + f"?filter[id_product_attribute]={combination_id}&display=full", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        to_remove = ["id_shop", "id_shop_group", "location"]
        for t in to_remove:
            for s in bs_blank.select(t):
                s.extract()
        quantity_t = bs_blank.find("quantity")
        quantity_t.string = str(quantity)
        stock_id = bs_blank.find("id").get_text()
        stock_available = bs_blank.find("stock_available")
        stock_availables = bs_blank.find("stock_availables")
        prestashop = bs_blank.find("prestashop")
        prestashop.append(stock_available)
        stock_availables.extract()
        print(bs_blank.prettify())
        status = requests.put(self.endpoints['stock_availables'].path + f"/{stock_id}", headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 200:
            print(f"Failed to update stock for combination {combination_id}")
            print(status.text)
            return -1
        print(status.status_code)
        return 0


    def add_product(self, product_name, price, manufacturer_id, category_ids, tax_id, description = "", supplier_id = 1, width = None, height = None, depth = None, weight = None, needle_value_id = None, crochet_value_id = None, composition_value_id = None, length_value_id = None, country_value_id = None, needle_id = None, crochet_id = None, composition_id = None, length_id = None, country_id = None):
        blank = requests.get(self.endpoints['products'].path + "?schema=synopsis", headers=self.auth_header)
        bs_blank = BeautifulSoup(blank.text, "xml")
        to_remove = ["cache_default_attribute", "id_default_image", "id_default_combination",
                     "position_in_category", "manufacturer_name", "quantity","id_shop_default",
                     "reference", "supplier_reference", "location", "quantity_discount", "ean13", "upc",
                     "isbn", "mpn", "cache_is_pack", "cache_has_attachments", "is_virtual",
                     "additional_delivery_times", "delivery_in_stock", "delivery_out_stock", "on_sale",
                     "online_only", "ecotax", "minimal_quantity", "low_stock_alert", "low_stock_threshold",
                     "wholesale_price", "unity", "unit_price_ratio", "additional_shipping_cost",
                     "customizable", "text_fields", "uploadable_files", "redirect_type", 
                     "is_type_redirected", "available_date", "show_condition", "condition",
                     "advanced_stock_management", "date_add", "date_upd", "pack_stock_type", "meta_description",
                     "meta_keywords", "meta_title", "images", "description_short", "available_now",
                     "available_later", "combinations", "product_option_values",
                     "tags", "stock_availables", "attachments", "accessories", "product_bundle",
                     "id_type_redirected"]
        for t in to_remove:
            for s in bs_blank.select(t):
                s.extract()
        id_manufacturer_t = bs_blank.find("id_manufacturer")
        id_manufacturer_t.string = str(manufacturer_id)
        id_supplier_t = bs_blank.find("id_supplier")
        id_supplier_t.string = str(supplier_id)
        id_category_t = bs_blank.find("id_category_default")
        id_category_t.string = str(category_ids[-1])
        active = bs_blank.find("active")
        active.string = "1"
        state = bs_blank.find("state")
        state.string = "1"
        new = bs_blank.find("new")
        new.string = "1"
        product_type = bs_blank.find("product_type")
        product_type.string = CData("combinations")
        type = bs_blank.find("type")
        type.string = "1"
        available_for_order = bs_blank.find("available_for_order")
        available_for_order.string = "1"
        show_price = bs_blank.find("show_price")
        show_price.string = "1"
        indexed = bs_blank.find("indexed")
        indexed.string = "1"
        visibility = bs_blank.find("visibility")
        visibility.string = CData("both")
        link_rewrite = bs_blank.find("link_rewrite")
        link_rewrite_languages = link_rewrite.find_all("language")
        for language in link_rewrite_languages:
            language.string = CData(product_name.lower().replace(" ", "-"))
        name = bs_blank.find("name")
        name_languages = name.find_all("language")
        for language in name_languages:
            language.string = CData(product_name)
        description_t = bs_blank.find("description")
        description_languages = description_t.find_all("language")
        for language in description_languages:
            language.string = CData(description)
        id_tax_rules_group = bs_blank.find("id_tax_rules_group")
        id_tax_rules_group.string = str(tax_id)
        categories = bs_blank.find("categories")
        category_tags = categories.find_all("category")
        for category_tag in category_tags:
            category_tag.extract()
        for category_id in category_ids:
            category = bs_blank.new_tag("category")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(category_id)
            category.append(id_t)
            categories.append(category)
        product_features = bs_blank.find("product_features")
        product_feature_tags = product_features.find_all("product_feature")
        for product_feature_tag in product_feature_tags:
            product_feature_tag.extract()
        if needle_value_id != None and needle_id != None:
            product_feature = bs_blank.new_tag("product_feature")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(needle_id)
            product_feature.append(id_t)
            id_feature_value = bs_blank.new_tag("id_feature_value")
            id_feature_value.string = str(needle_value_id)
            product_feature.append(id_feature_value)
            product_features.append(product_feature)
        if crochet_value_id != None and crochet_id != None:
            product_feature = bs_blank.new_tag("product_feature")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(crochet_id)
            product_feature.append(id_t)
            id_feature_value = bs_blank.new_tag("id_feature_value")
            id_feature_value.string = str(crochet_value_id)
            product_feature.append(id_feature_value)
            product_features.append(product_feature)
        if composition_value_id != None and composition_id != None:
            product_feature = bs_blank.new_tag("product_feature")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(composition_id)
            product_feature.append(id_t)
            id_feature_value = bs_blank.new_tag("id_feature_value")
            id_feature_value.string = str(composition_value_id)
            product_feature.append(id_feature_value)
            product_features.append(product_feature)
        if length_value_id != None and length_id != None:
            product_feature = bs_blank.new_tag("product_feature")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(length_id)
            product_feature.append(id_t)
            id_feature_value = bs_blank.new_tag("id_feature_value")
            id_feature_value.string = str(length_value_id)
            product_feature.append(id_feature_value)
            product_features.append(product_feature)
        if country_value_id != None and country_id != None:
            product_feature = bs_blank.new_tag("product_feature")
            id_t = bs_blank.new_tag("id")
            id_t.string = str(country_id)
            product_feature.append(id_t)
            id_feature_value = bs_blank.new_tag("id_feature_value")
            id_feature_value.string = str(country_value_id)
            product_feature.append(id_feature_value)
            product_features.append(product_feature)
        # if no features are added, remove the tag
        if len(product_features.find_all("product_feature")) == 0:
            product_features.extract()
        price_t = bs_blank.find("price")
        price_t.string = str(price)
        width_t = bs_blank.find("width")
        if width != None:
            width_t.string = str(width)
        else:
            width_t.extract()
        height_t = bs_blank.find("height")
        if height != None:
            height_t.string = str(height)
        else:
            height_t.extract()
        depth_t = bs_blank.find("depth")
        if depth != None:
            depth_t.string = str(depth)
        else:
            depth_t.extract()
        weight_t = bs_blank.find("weight")
        if weight != None:
            weight_t.string = str(weight)
        else:
            weight_t.extract()
        #print(bs_blank.prettify())
        status = requests.post(self.endpoints['products'].path, headers=self.auth_header, data=bs_blank.encode())
        if status.status_code != 201:
            print(f"Failed to add product {product_name}")
            return -1
        bs_status = BeautifulSoup(status.text, "xml")
        product_id = bs_status.find("id")
        added_id = int(product_id.get_text())

        return added_id

