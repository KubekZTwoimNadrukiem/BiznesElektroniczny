import sys

from wrapper import Wrapper

def main(key, api_url):
    w = Wrapper(key, api_url)
    w.load_data("../Scraper/")

    #print(api.does_supplier_exist("test"))
    #print(api.get_category_id("test"))
    #api.add_category("test")
    #api.add_supplier("test", "test")
    # api.add_product("test", 12.50,
    #                 api.get_manufacturer_id("test"),
    #                 api.get_category_id("test"),
    #                 api.get_supplier_id("test"))
    #api.add_image("/home/ahrithmia/Downloads/ryan-gosling---wi13-01----resize.jpg", "categories", 3)
    #api.add_manufacturer("test")
    

if __name__ == "__main__":
    key = "YZ245ZJY86UAPI46LN431JCQ9CMWNWH8"
    api_url = "http://localhost:8089/api/"
    if len(sys.argv) == 3:
        key = sys.argv[1]
        api_url = sys.argv[2]
    else:
        print("You may provide your own key and API url as arguments.")
        print("Usage: python -m rest <key> <api_url>")
        print("Using default key and API url.")

    main(key, api_url)
