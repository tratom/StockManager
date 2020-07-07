import atexit
import sys


def main():
    global sortedItems, cart
    cart = list()
    items = list()
    database = open('database.txt', 'r')

    # popolating the list of dictionary with the data of the text file
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
    # sorting of the list of dictionary
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
            9: lambda: sys.exit(0)  # quit()
        }

        caller = choices.get(choice, lambda: print('Unknown command'))
        caller()



# function that insert a new item in the correct position of the dictionary
# @id is the id to be added
# @index is the index of the list where the new item should be added
def insert(id=None, index=None):
    item = {
        'id': id if id else int(input('Insert the numeric id: ')),
        'name': input('Insert item description: '),
        'price': float(input('Insert the price for unit: ').replace(',', '.')),
        'quantity': int(input('Insert the quantity: '))
    }
    if not index:
        foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, item['id'])
        if foundItem:
            print('This item already exist. Do you want to modify it?')
            choice = input('Press Y for yes, any other character to back to menu: ').lower()
            if choice == 'y':
                update(indexItem)
            else:
                return
    sortedItems.insert(index, item)
    return


# function that update an existing item
def update(indexItem = None):
    foundItem = False
    id = -1
    if not indexItem:
        id = int(input('Insert id to be modified: '))
        foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
    if foundItem or indexItem:
        sortedItems[indexItem]['name'] = input('Insert the new description: ')
        sortedItems[indexItem]['price'] = float(input('Insert the new price: ').replace(',', '.'))
        sortedItems[indexItem]['quantity'] = int(input("Insert the new quantity: "))

        foundCart, indexCart = binarySearch(cart, 0, len(cart) - 1, sortedItems[indexItem]['id'])
        if foundCart:
            updateFromCart(indexCart, indexItem)
        return
    else:
        print('Item not found, would you like to insert it?')
        choice = input('Press Y for yes, any other character to back to menu: ').lower()
        if choice == 'y':
            insert(id)
        else:
            return


# function that show an existing item
def show():
    id = int(input('Insert id to be find: '))
    found, index = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
    if found:
        printItem(sortedItems[index])
        return
    else:
        print('Item not found, would you like to insert it?')
        choice = input('Press Y for yes, any other character to back to menu: ').lower()
        if choice == 'y':
            insert(id, index)
        else:
            return


def delete():
    id = int(input('Insert id to be deleted: '))
    found, index = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
    if found:
        sortedItems.pop(index)
        deleteFromCart(id)
        print('The item has been deleted\n')
    else:
        print('Item not found\n')
    return


def addToCart():
    id = int(input('Insert the id to be added in the cart: '))
    foundCart, indexCart = binarySearch(cart, 0, len(cart) - 1, id)
    foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, id)
    if foundCart:
        print('This item is already present in the cart')
    elif foundItem:
        while True:
            quantity = int(
                input('Insert the quantity of ' + sortedItems[indexItem]['name'] + ' to be added to the cart: '))
            if quantity > sortedItems[indexItem]['quantity']:
                print('The quantity exceed the quantity in stock. The maximum quantity is',
                      sortedItems[indexItem]['quantity'])
            else:
                break
        cartItem = sortedItems[indexItem]
        cartItem['quantity'] = quantity
        cart.append(cartItem)
        print('The item has been added in the cart\n')
    else:
        print('Item not found, please create it before add in the cart\n')
    return


def deleteFromCart(id = None):
    if not id:
        id = int(input('Insert the id to be deleted from the cart: '))
    found, index = binarySearch(cart, 0, len(cart) - 1, id)
    if found:
        cart.pop(index)
        print('The item has been deleted from the cart\n')
    else:
        print('Item not in the cart\n')
    return


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
            cart[indexCart]['quantity'] = newQuantity
            print('The item has been updated\n')
        else:
            print('Item not in the cart\n')
    else:
        cart[indexCart]['name'] = sortedItems[indexItem]['name']
        cart[indexCart]['price'] = sortedItems[indexItem]['price']
        while sortedItems[indexItem]['quantity'] < cart[indexCart]['quantity']:
            print('The quantity of ' + sortedItems[indexItem][
                'name'] + ' in the cart is greater then the quantity in the stock.\n'
                          'The maximum quantity is ' + str(sortedItems[indexItem]['quantity']))
            cart[indexCart]['quantity'] = int(input('Please, update the quantity in the cart: '))
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
    choice = input('Press Y for yes, any other character to back to menu: ').lower()
    if choice == 'y':
        for item in cart:
            foundItem, indexItem = binarySearch(sortedItems, 0, len(sortedItems) - 1, item['id'])
            if foundItem:
                sortedItems[indexItem]['quantity'] -= item['quantity']
        cart.clear()
        print('The changes have been applied')
    else:
        print('The changes have not been applied')

    return


def quit():
    database = open('database.txt', 'w')
    for item in sortedItems:
        tmp = str(item['id']) + ';' + item['name'] + ';' + str(item['price']) + ';' + str(item['quantity']) + '\n'
        database.write(tmp)
        # print(';'.join(str(v) for v in item.values()))
    database.close()
    print('Byebye')


def printItem(item):
    print('id:', item['id'], ' --- description:', item['name'], ' --- price:',
              item['price'], ' --- quantity:', item['quantity'])


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


atexit.register(quit)

main()


# todo aggiornare quantità della merce in stock quando si fanno operazioni sul cart (aggiunta, rimozione, modifica di elementi nel carrello)
