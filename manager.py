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
    while choice != 9:
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

        if choice == 1:
            insert()
        elif choice == 2:
            update()
        elif choice == 3:
            show()
        elif choice == 4:
            delete()
        elif choice == 5:
            addToCart()
        elif choice == 6:
            deleteFromCart()
        elif choice == 7:
            updateFromCart()
        elif choice == 8:
            checkoutFromCart()
        elif choice == 9:
            quit()
        else:
            print('Unknown command')


# function to add a new item in the stock list
def insert(id=None, index=None):
    item = {
        'id': id if id else int(input('Insert the numeric id: ')),  # if the id comes from another function then fill it
        'name': input('Insert item description: '),
        'price': float(input('Insert the price for unit: ').replace(',', '.')),
        'quantity': int(input('Insert the quantity: '))
    }
    # if index is specified, insert it without searching
    if not index:
        success, index = insert_in_stock(item)  # check if the item already exists and find the position
        if success:
            print('The item has been added in the stock')
        else:
            print('This item already exist. Do you want to modify it?')
            if askConfirmation():
                update(sortedItems[index]['id'], index)
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
def update(id = None, index = None):
    foundItem = True
    if not index or not id:
        id = int(input('Insert id to be modified: '))
        foundItem, index = get_from_stock(id)

    item = {
        'id': id,
        'name': input('Insert the new description: '),
        'price': float(input('Insert the new price: ').replace(',', '.')),
        'quantity': int(input("Insert the new quantity: "))
    }

    if foundItem:
        update_in_stock(item, index)
        print('The item has been updated\n')
        foundCart, indexCart = get_from_cart(sortedItems[index]['id'])
        if foundCart:
            updateFromCart(indexCart, index)
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
        deleteFromCart(id)
        delete_from_stock(index)
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

    success, index = delete_from_cart(id)
    if success:
        print('The item has been deleted from the cart\n')
    else:
        print('Item not in the cart\n')
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


def updateFromCart(indexCart=None, indexItem=None):
    if indexCart == None:
        id = int(input('Insert the id to be updated from the cart: '))
        foundCart, indexCart = get_from_cart(id)
        foundItem, indexItem = get_from_stock(id)

        if foundCart:
            print('There are', cart[indexCart]['quantity'], 'product in the cart')
            updated = False
            while not updated:
                quantity = int(input('Update the quantity in the cart: '))
                updated = update_in_cart(indexCart, indexItem, quantity)
                if not updated:
                    print('The new quantity exceed the quantity in stock. The maximum quantity is',
                          sortedItems[indexItem]['quantity'])
        else:
            print('Item not in the cart\n')
            return
    else:
        cart[indexCart]['name'] = sortedItems[indexItem]['name']
        cart[indexCart]['price'] = sortedItems[indexItem]['price']
        quantity = cart[indexCart]['quantity']
        updated = False
        while not updated:
            updated = update_in_cart(indexCart, indexItem, quantity)

            if not updated:
                print('The quantity of ' + sortedItems[indexItem][
                    'name'] + ' in the cart is greater then the quantity in the stock.\n'
                              'The maximum quantity is ' + str(sortedItems[indexItem]['quantity']))
                quantity = int(input('Please, update the quantity in the cart: '))

    print('The item in the cart has been updated\n')
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
    sortedItems[indexItem]['quantity'] = sortedItems[indexItem]['quantity'] - quantity

    return True


def get_from_cart(id):
    found, index = binarySearch(cart, 0, len(cart) - 1, id)
    if found:
        return True, index
    return False, index


def update_in_cart(indexCart, indexItem, quantity):
    if quantity > sortedItems[indexItem]['quantity']:
        return False

    difference = sortedItems[indexItem]['quantity'] - (quantity - cart[indexCart]['quantity'])
    cart[indexCart]['quantity'] = quantity

    sortedItems[indexItem]['quantity'] = difference
    return True


def delete_from_cart(id):
    success, index = get_from_cart(id)
    if not success:
        return False, index

    success, indexItem = get_from_stock(id)
    sortedItems[indexItem]['quantity'] = sortedItems[indexItem]['quantity'] + cart[index]['quantity']

    cart.pop(index)
    return True, index


#*
#* Utils functions
#*

def quit():
    # clear cart and update quantity in stock
    for c in cart:
        delete_from_cart(c['id'])

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


main()
