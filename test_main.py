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
        item = {'id': 1, 'name': "product 1", 'price': 1.0, 'quantity': 1}
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
        item = {'id': 20, 'name': "product 1", 'price': 1.0, 'quantity': 1}
        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, False)
        manager.insert_in_stock(item, index)
        self.assertEqual(item, manager.sortedItems[index])


    def test_update_existing_item(self):
        self.__init_stock__()
        item = {'id': 32, 'name': "updated product", 'price': 1.0, 'quantity': 1}

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, True)

        manager.update_in_stock(item, index)

        self.assertEqual(item['name'], manager.sortedItems[index]['name'])

    def test_delete_from_stock(self):
        self.__init_stock__()
        item = {'id': 10, 'name': "updated product", 'price': 1.0, 'quantity': 1}

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, True)

        manager.delete_from_stock(index)

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, False)

    def test_add_item_to_cart(self):
        self.__init_stock__()
        item = {'id': 50, 'name': "product in cart", 'price': 1.0, 'quantity': 25}
        manager.insert_in_stock(item)

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(success, True)

        # add 10 item to the cart
        manager.insert_in_cart(index, 10)

        success, indexCart = manager.get_from_cart(item['id'])
        self.assertEqual(manager.cart[indexCart]['quantity'], 10)
        self.assertEqual(manager.sortedItems[index]['quantity'], 15)

    def test_remove_item_from_cart(self):
        self.__init_stock__()
        item = {'id': 60, 'name': "product in cart that will be deleted", 'price': 1.0, 'quantity': 30}
        # add item in the cart
        manager.insert_in_stock(item)
        success, index = manager.get_from_stock(item['id'])
        manager.insert_in_cart(index, 10)

        # remove item and test updated stock quantity
        success, indexCart = manager.get_from_cart(item['id'])
        self.assertEqual(manager.cart[indexCart]['quantity'], 10)
        self.assertEqual(manager.sortedItems[index]['quantity'], 20)

        success, index = manager.delete_from_cart(item['id'])
        self.assertEqual(success, True)

        success, index = manager.get_from_stock(item['id'])
        self.assertEqual(manager.sortedItems[index]['quantity'], 30)

    def test_remove_non_existing_item_from_cart(self):
        self.__init_stock__()

        success, index = manager.delete_from_cart(20)
        self.assertEqual(success, False)

    def test_item_updated_in_the_cart(self):
        self.__init_stock__()
        item = {'id': 70, 'name': "product that will be updated", 'price': 1.0, 'quantity': 50}

        manager.insert_in_stock(item)
        success, index = manager.get_from_stock(item['id'])
        manager.insert_in_cart(index, 10)

        successCart, indexCart = manager.get_from_cart(item['id'])
        successItem, indexItem = manager.get_from_stock(item['id'])

        self.assertEqual(successCart, True)
        self.assertEqual(successItem, True)

        self.assertEqual(manager.cart[indexCart]['quantity'], 10)
        self.assertEqual(manager.sortedItems[indexItem]['quantity'], 40)

        ok = manager.update_in_cart(indexCart, indexItem, 20)
        self.assertEqual(ok, True)

        self.assertEqual(manager.cart[indexCart]['quantity'], 20)
        self.assertEqual(manager.sortedItems[indexItem]['quantity'], 20)

    def test_item_updated_in_cart_no_enough_quantity(self):
        self.__init_stock__()
        item = {'id': 80, 'name': "only two product", 'price': 1.0, 'quantity': 2}

        manager.insert_in_stock(item)
        success, index = manager.get_from_stock(item['id'])
        manager.insert_in_cart(index, 1)

        successCart, indexCart = manager.get_from_cart(item['id'])
        successItem, indexItem = manager.get_from_stock(item['id'])

        self.assertEqual(successCart, True)
        self.assertEqual(successItem, True)

        ok = manager.update_in_cart(indexCart, indexItem, 2)
        self.assertEqual(ok, False)

    def test_item_back_in_stock_after_quit(self):
        self.__init_stock__()

        success, index = manager.get_from_stock(25)
        manager.insert_in_cart(index, 10)

        successCart, indexCart = manager.get_from_cart(25)
        successItem, indexItem = manager.get_from_stock(25)

        self.assertEqual(successCart, True)
        self.assertEqual(successItem, True)

        self.assertEqual(manager.cart[indexCart]['quantity'], 10)
        self.assertEqual(manager.sortedItems[indexItem]['quantity'], 2)

        manager.quit()

        self.__init_stock__()

        self.assertEqual(manager.sortedItems[indexItem]['quantity'], 12)



if __name__ == '__main__':
    unittest.main()
