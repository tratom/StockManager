import unittest
import manager

class TestStockManager(unittest.TestCase):

    def __init_stock__(self):
        manager.cart = list()
        manager.items = list()
        database = open('database.txt', 'r')

        # populate the list of dictionary with the data of the text file
        for object in database:
            column = object.split(';')
            manager.items.append(
                {
                    'id': int(column[0]),
                    'name': column[1],
                    'price': float(column[2].replace(',', '.')),
                    'quantity': int(column[3].strip())
                }
            )

        database.close()
        # sort list of dictionary
        manager.sortedItems = sorted(manager.items, key=lambda i: i['id'])

    def test_insert_in_stock(self):
        self.__init_stock__()
        item = {'id': 1, 'name': "product 1", 'price': 1, 'quantity': 1}
        # insert item in stock
        manager.insert_in_stock(item)
        # get item from stock
        success, index = manager.get_from_stock(item['id'])
        # assert that item has been added
        self.assertEqual(success, True)
        # assert that item is equals
        self.assertEqual(item, manager.sortedItems[index])

    def test_search_and_insert_non_existing_item(self):
        self.__init_stock__()
        item = {'id': 20, 'name': "product 1", 'price': 1, 'quantity': 1}
        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, False)
        manager.insert_in_stock(item, index)
        self.assertEqual(item, manager.sortedItems[index])


    def test_update_existing_item(self):
        self.__init_stock__()
        item = {'id': 32, 'name': "updated product", 'price': 1, 'quantity': 1}

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, True)

        manager.update_in_stock(item, index)

        self.assertEqual(item['name'], manager.sortedItems[index]['name'])

    def test_delete_from_stock(self):
        self.__init_stock__()
        item = {'id': 10, 'name': "updated product", 'price': 1, 'quantity': 1}

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, True)

        manager.delete_from_stock(index)

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, False)


if __name__ == '__main__':
    unittest.main()
