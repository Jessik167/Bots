def muestra_item_guardado(item):
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('{} ha sido agregado a la lista!'.format(item))
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


def error_existe_item(item, err):
    print('**************************************************************')
    print('el id {} ya existe en la lista!'.format(item))
    print('{}'.format(err.args[0]))
    print('**************************************************************')
    

def error_no_guardado(item, err):
    print('**************************************************************')
    print('el id {} no existe en la lista, primero inserte!'.format(item))
    print('{}'.format(err.args[0]))
    print('**************************************************************')