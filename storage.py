import json
import os


class Storage:
    """
    Storage class to store scraped products data in json format
    and update products data if price changes
    """

    def __init__(self, storage_file: str):
        self.storage_file = storage_file

    def _load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                return json.load(file)
        return []

    def _save_data(self, data):
        with open(self.storage_file, 'w') as file:
            json.dump(data, file, indent=4)

    def store_products(self, products):
        print('????? len of products :', len(products))
        existing_data = self._load_data()
        existing_data_dict = {product['product_title']: product for product in existing_data}

        for new_product in products:
            if new_product['product_title'] in existing_data_dict:
                print(">>>> if condtiing workimg ???????")
                existing_product = existing_data_dict[new_product['product_title']]
                if existing_product['product_price'] != new_product['product_price']:
                    existing_product['product_price'] = new_product['product_price']
                    existing_product['path_to_image'] = new_product['path_to_image']  # Update image if necessary
            else:
                print(">>>> else workimg ???????")

                existing_data_dict[new_product['product_title']] = new_product
        
        updated_data = list(existing_data_dict.values())
        print('>>>>> len of update products :', len(updated_data))


        self._save_data(updated_data)
