import fdb
from config import load_config

config = load_config('.env')

con = fdb.connect(dsn=config.db.dsn, user=config.db.user, password=config.db.password)
cur_1 = con.cursor()


def daily_total(cur, date: str, month: str):
    cash, noncash = [], []
    cur.execute(f"SELECT ds.NONCASH, ds.COMMONSUMMA2 FROM DOC_SALE ds "
                f"WHERE DOC_DATE LIKE '2023-{month}-{date}%'")
    for pay in cur.fetchall():
        if int(pay[0]) == 1:
            noncash.append(int(pay[1]))
        else:
            cash.append(int(pay[1]))
    line = f'Дата: {date}-{month}\n' \
           f'Наличные: {sum(cash)}\n' \
           f'Безнал: {sum(noncash)}\n' \
           f'Итого: {sum(cash) + sum(noncash)}'
    return line


def sales(cur, date: str, month: str):
    data_list = []
    cur.execute(
        f"SELECT ds.DOC_DATE, dg.NAME, dst.QUANTITY, dst.PRICE2, dst.SUMMA2, ds.NONCASH "
        f"FROM DOC_SALE ds, DOC_SALE_TABLE dst , DIR_GOODS dg "
        f"WHERE ds.DOC_DATE LIKE '2023-{month}-{date}%' AND ds.CODE = dst.CODE AND dst.GOOD = dg.CODE "
        f"ORDER BY DOC_DATE")
    for row in cur.fetchall():
        no_cash = '----- Оплата картой\n' if row[5] == 1 else ''
        data_list.append(f"{str(row[0])[11:16]} {row[1]}\n--"
                         f"{int(row[2])}--{int(row[3])}--итого: <{int(row[4])}>\n{no_cash}\n")
    line = ''.join(data_list)
    return line


def goods_list(cur, arg1, arg2):
    txt = []
    cur.execute(
        f"SELECT SQ.NAME, Sum(QUANTITY), SQ.PRICE_ FROM ("
        f"SELECT dg.NAME, dst.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SESSION_TABLE dst "
        f"WHERE dg.CODE = dst.GOOD AND dg.PARENT BETWEEN {arg1} AND {arg2} "
        f"UNION ALL "
        f"SELECT dg.NAME, -dst2.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SALE_TABLE dst2 "
        f"WHERE dg.CODE = dst2.GOOD AND dg.PARENT BETWEEN {arg1} AND {arg2} "
        f"UNION ALL "
        f"SELECT dg.NAME, -dbt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_BALANCE_TABLE dbt "
        f"WHERE dg.CODE = dbt.GOOD AND dg.PARENT BETWEEN {arg1} AND {arg2} "
        f"UNION ALL "
        f"SELECT dg.NAME, +drt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_RETURN_TABLE drt "
        f"WHERE dg.CODE = drt.GOOD AND dg.PARENT BETWEEN {arg1} AND {arg2} "
        f"UNION ALL "
        f"SELECT dg.NAME, -det.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_EXPSESSION_TABLE det "
        f"WHERE dg.CODE = det.GOOD AND dg.PARENT BETWEEN {arg1} AND {arg2}) SQ "
        f"GROUP BY SQ.NAME, SQ.PRICE_ "
        f"HAVING SUM(SQ.QUANTITY) >= 1 "
        f"ORDER BY SQ.PRICE_"
    )
    result = cur.fetchall()
    for row in result:
        txt.append(f'{row[0]}\nЦена: {int(row[2])} руб\n\n')
    line = ''.join(txt)
    return line
