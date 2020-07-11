import atexit
import sys

def main():
    global sortedItems, cart
    cart = list()
    items = list()
    database = open('database.txt', 'r')

    # populate the list of dictionary with the data of the text file
    for object in database:
        column = object.split(';')
        items.append(
            {
                'id': int(column[0]),
                'name': column[1],
                'price': float(column[2].replace(',', '.')),
                'quantity': int(column[3].strip())
            }
        )

    database.close()
    # sort list of dictionary
    sortedItems = sorted(items, key=lambda i: i['id'])
    menu()


# function that display the menu and call the functions to operate on the dictionary
def menu():
    choice = 0
    while True:
        print('---------------STOCK MANAGER---------------')
        print('1. Insert new item')
        print('2. Update an existing item')
        print('3. Show an existing item')
        print('4. Delete an existing item')
        print('---------------CART MANAGER----------------')
        print('5. Add an existing item in the cart')
        print('6. Remove an item from the cart')
        print('7. Update the quantity of an item in the cart')
        print('8. Checkout')
        print('---SAVE THE CHANGES AND QUIT THE PROGRAM---')
        print('9. Quit')
        choice = int(input('Enter choice: '))

        choices = {
            1: lambda: insert(),
            2: lambda: update(),
            3: lambda: show(),
            4: lambda: delete(),
            5: lambda: addToCart(),
            6: lambda: deleteFromCart(),
            7: lambda: updateFromCart(),
            8: lambda: checkoutFromCart(),
            9: lambda: sys.exit(0)
        }

        caller = choices.get(choice, lambda: print('Unknown command'))
        caller()

#*
#* Stock functons
#*

def insert(id=None, index=None):
    item = {
        'id': id if id else int(input('Insert the numeric id: ')),
        'name': input('Insert item description: '),
        'price': float(input('Insert the price for unit: ').replace(',', '.')),
        'quantity': int(input('Insert the quantity: '))
    }
    # if index is not specified insert without searching it
    if not index:
        success, index = insert_in_stock(item)
        if success:
            print('The item has been added in the stock')
        else:
            print('This item already exist. Do you want to modify it?')
            if askConfirmation():
                update(index)
    else:
        # index is already specified and we assume that item doesn't exists
        success, index = insert_in_stock(item, index)
        print('The item has been added in the stock')
    return

# function that show an existing item
def show():
    id = int(input('Insert id to be find: '))
    success, index = get_from_stock(id)
    if success:
        printItem(sortedItems[index])
    else:
        print('Item not found, would you like to insert it?')
        if askConfirmation():
            insert(id, index)
    return

# function that update an existing item
def update(index = None):
    foundItem = False
    id = -1
    if not index:
        id = int(input('Insert id to be modified: '))
        foundItem, index = get_from_stock(id)

    item = {
        'id': id,
        'name': input('Insert the new description: '),
        'price': float(input('Insert the new price: ').replace(',', '.')),
        'quantity': int(input("Insert the new quantity: "))
    }

    if foundItem or index:
        update_in_stock(item, index)
        print('The item has been updated\n')
        # update cart todo: refactor
        foundCart, indexCart = binarySearch(cart, 0, len(cart) - 1, sortedItems[indexItem]['id'])
        if foundCart:
            updateFromCart(indexCart, indexItem)
    else:
        print('Item not found, would you like to insert it?')
        if askConfirmation():
            success, newIndex = insert_in_stock(item, index if index else None)
            if success:
                print('The item has been added\n')
    return

def delete():
    id = int(input('Insert id to be deleted: '))
    success, index = get_from_stock(id)
    if success:
        delete_from_stock(index)
        deleteFromCart(id)
        print('The item has been deleted\n')
    else:
        print('Item not found\n')
    return

#*
#* Stock core functions
#*

# function that insert a new item in the correct position of the dictionary
# @id is the id to be added
# @index is the index of the list where the new item should be added
def insert_in_stock(item, index=None):
    if not index:
        found, index = binarySearch(sortedItems, 0, len(sortedItems) - 1, item['id'])
        if found:
            return False, index
        sortedItems.insert(index, item)
    else:
        sortedItems.insert(index, item)
    return True, None

def get_from_stock(id):
    found, index = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
    if found:
        return True, index
    return False, index

def update_in_stock(item, index):
    sortedItems[index] = item
    return True, index

def delete_from_stock(index):
    sortedItems.pop(index)
    return

# -------- to be refactored

#*
#* Cart functions
#*

def addToCart():
    id = int(input('Insert the id to be added in the cart: '))
    success, indexCart = get_from_cart(id)
    if success:
        print('This item is already present in the cart')
    else:
        success, indexItem = get_from_stock(id)
        if success:
            added = False
            while not added:
                quantity = int(
                    input('Insert the quantity of ' + sortedItems[indexItem]['name'] + ' to be added to the cart: '))
                added = insert_in_cart(indexItem, quantity)
                if not added:
                    print('The quantity exceed the quantity in stock. The maximum quantity is',
                          sortedItems[indexItem]['quantity'])

            print('The item has been added in the cart\n')
        else:
            print('Item not found, please create it before add in the cart\n')

    return

def deleteFromCart(id = None):
    if not id:
        id = int(input('Insert the id to be deleted from the cart: '))

    succcess, index = delete_from_cart(id)
    if success:
        print('The item has been deleted from the cart\n')
    else:
        print('Item not in the cart\n')
    return

#*
#* Cart core functions
#*

def insert_in_cart(indexItem, quantity):
    if sortedItems[indexItem]['quantity'] < quantity:
        return False

    # add item in the cart
    cartItem = dict(sortedItems[indexItem])
    cartItem['quantity'] = quantity
    cart.append(cartItem)

    # decrease and update quantity in stock
    sortedItems[indexItem].update({'quantity': sortedItems[indexItem]['quantity'] - quantity})

    return True


def get_from_cart(id):
    found, index = binarySearch(cart, 0, len(cart) - 1, id)
    if found:
        return True, index
    return False, index


def delete_from_cart(id):
    success, index = get_from_cart(id)
    if not success:
        return False, index

    success, indexItem = get_from_stock(id)
    sortedItems[indexItem].update({'quantity': sortedItems[indexItem]['quantity'] + cart[index]['quantity']})

    cart.pop(index)
    return True, index

def updateFromCart(indexCart=None, indexItem=None):
    if not indexCart:
        id = int(input('Insert the id to be updated from the cart: '))
        foundCart, indexCart = binarySearch(cart, 0, len(cart) - 1, id)
        foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
        if foundCart:
            print('There are', cart[indexCart]['quantity'], 'product in the cart')
            while True:
                newQuantity = int(input('Update the quantity in the cart: : '))
                if newQuantity > sortedItems[indexItem]['quantity']:
                    print('The new quantity exceed the quantity in stock. The maximum quantity is',
                          sortedItems[indexItem]['quantity'])
                else:
                    break
            difference = cart[indexCart]['quantity'] - newQuantity
            cart[indexCart]['quantity'] = newQuantity
            alterStock(difference, item=sortedItems[indexItem])
            print('The item has been updated\n')
        else:
            print('Item not in the cart\n')
    else:
        cart[indexCart]['name'] = sortedItems[indexItem]['name']
        cart[indexCart]['price'] = sortedItems[indexItem]['price']
        '''
        newQuantity = cart[indexCart]['quantity']
        while True:
            if sortedItems[indexItem]['quantity'] < newQuantity:
                print('The quantity of ' + sortedItems[indexItem][
                    'name'] + ' in the cart is greater then the quantity in the stock.\n'
                              'The maximum quantity is ' + str(sortedItems[indexItem]['quantity']))
                newQuantity = int(input('Please, update the quantity in the cart: '))
            else:
                break
        difference = cart[indexCart]['quantity'] - newQuantity
        cart[indexCart]['quantity'] = newQuantity
        alterStock(difference, item=sortedItems[indexItem])
        '''
        print('The item in the cart has been updated\n')
    return


def checkoutFromCart():
    total = 0
    print('SUMMARY:')
    for item in cart:
        printItem(item)
        total += item['price'] * item['quantity']
    print('TOTAL:', total)
    print('Do you want to continue?')
    if askConfirmation():
        cart.clear()
        print('The changes have been applied')
    else:
        print('The changes have not been applied')

    return


def quit():
    # save all changes stored in memory to database file when application exit
    database = open('database.txt', 'w')
    for item in sortedItems:
        tmp = str(item['id']) + ';' + item['name'] + ';' + str(item['price']) + ';' + str(item['quantity']) + '\n'
        database.write(tmp)
    database.close()
    print('Byebye')


def printItem(item):
    print('id:', item['id'], ' --- description:', item['name'], ' --- price:',
              item['price'], ' --- quantity:', item['quantity'])

def alterStock(quantity, item=None, id=None):
    if not item:
        foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
        item = sortedItems[indexItem]
    item['quantity'] += quantity


def askConfirmation(message = 'Press Y for yes, any other character to back to menu: '):
    choice = input(message).lower()
    if choice == 'y':
        return True
    return False


def binarySearch(list, firstIndex, secondIndex, target):
    if firstIndex <= secondIndex:
        if secondIndex == 1:
            mid = secondIndex
        else:
            mid = (firstIndex + secondIndex) // 2
        if list[mid]['id'] == target:
            return True, mid
        elif list[mid]['id'] < target:
            return binarySearch(list, mid + 1, secondIndex, target)
        else:
            return binarySearch(list, firstIndex, mid - 1, target)
    else:
        return False, firstIndex


# define a callback function when application exit
# using ´atexit´ python standard library
atexit.register(quit)

if __name__ == "__main__":
    main()
