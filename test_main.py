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


if __name__ == '__main__':
    unittest.main()