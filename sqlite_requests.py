import sqlite3

from firebird_requests import fb_dir_goods_request, cursor


def read_product(**kwargs):
    sqlite_connection = sqlite3.connect('products_desc', check_same_thread=False)
    cursor = sqlite_connection.cursor()
    cursor.execute(
        "SELECT {name} FROM MAIN WHERE {code} = {product_code}".format(**kwargs)
    )
    result = cursor.fetchone()
    try:
        return result
    except TypeError:
        return None


def check_sqlite_db(product_code):
    try:
        result = read_product(name='CODE', code='CODE', product_code=product_code)
        return result
    except TypeError:
        return None


def write_photo_db(code, name):
    sqlite_connection = sqlite3.connect('products_desc', check_same_thread=False)
    cursor = sqlite_connection.cursor()
    cursor.execute('INSERT INTO MAIN (CODE, NAME) VALUES (?, ?)',
                   (code, name))
    sqlite_connection.commit()


def take_caption(product_code):
    result = check_sqlite_db(product_code)
    price = fb_dir_goods_request(cur=cursor, column='PRICE_', code=product_code)
    if result:
        line = read_product(name='NAME, DESCRIPT', code='CODE', product_code=product_code)
        descr = '' if line[1] is None else line[1]
        caption = f"Цена {int(price[0][0])} руб.\n{line[0]}\n\n{descr}"
        return caption
    else:
        line = fb_dir_goods_request(cur=cursor, column='NAME, PRICE_', code=product_code)
        caption = f"{int(line[0][1])} руб.\n{line[0][0]}"
        write_photo_db(product_code, line[0][0])
        return caption

