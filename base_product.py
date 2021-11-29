import json

from variables import *


class Catalog:

    def __init__(self):
        self.goods_list = Catalog.load_from_file()
        self.auto_id = 0

    def __repr__(self):
        return f'Это весь лист {self.goods_list}'

    def make_product(self, list_):
        # list_contrast = [ID, NAME, DIRECTION, STATUS, PRICE]
        list_contrast = [ID, NAME, DIRECTION, STATUS, PRICE]
        if not self.check_params(list_):
            print('Элемент с таким именем уже есть')
            return
        self.auto_id += 1
        list_work = [self.auto_id]
        list_work.extend(list_)

        work_dict = {k: v for (k, v) in zip(list_contrast, list_work)}
        print('Это make_product', work_dict)
        return work_dict

    def get_list(self):
        print('Это весь лист', self.goods_list)
        return self.goods_list

    def check_params(self, products_list):
        all_products = self.load_from_file()
        if len(all_products) > 0:
            for i in all_products:
                if i[NAME] == products_list[0]:
                    return False
        self.auto_id = all_products[-1][ID]
        return True

    # Приходит словарь вида
    # {ID: 2, NAME: 'first', DIRECTION: 'west', STATUS: 'yes', PRICE: 100}
    def add_product(self, product):
        if product:
            self.goods_list.append(product)
            with open("data_file.json", 'r') as r_f:
                json_list = json.load(r_f)
                json_list.append(product)

            with open("data_file.json", 'w') as w_f:
                # json.dump(json_list, w_f, indent=4, ensure_ascii=False)
                json.dump(json_list, w_f, ensure_ascii=False)

    def delete_to_list(self, product):
        for i in self.goods_list:
            if i[ID] == product[ID]:
                self.goods_list.remove(product)
                return
        print('Такого товара нет в каталоге')

    def clear_all(self):
        self.goods_list = []
        # self.save_to_file()

    @staticmethod
    def load_from_file():
        # goods_list = []
        with open("data_file.json", 'r') as r_f:
            goods_list = json.load(r_f)
        return goods_list

    def save_to_file(self):
        with open("data_file.json", 'w') as w_f:
            json.dump(self.goods_list, w_f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    catalog = Catalog()
    # print(catalog.goods_list)

    first = catalog.make_product(['first', 'west', 'yes', 100])
    second = catalog.make_product(['два', 'ветер', 'yes', 150])

    catalog.add_product(first)
    catalog.add_product(second)
    # print(catalog.goods_list)

    # catalog.clear_all()
    # catalog.get_list()

    print(catalog)
