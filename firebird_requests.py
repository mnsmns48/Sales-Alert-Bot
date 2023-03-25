import fdb
from config import load_config

config = load_config('.env')

con = fdb.connect(dsn=config.db.dsn, user=config.db.user, password=config.db.password)
cursor = con.cursor()


def daily_total(cur, **kwargs):
    cash, noncash = [], []
    cur.execute("SELECT ds.NONCASH, ds.COMMONSUMMA2 FROM DOC_SALE ds \
                WHERE DOC_DATE LIKE '{date}%'".format(**kwargs))
    for pay in cur.fetchall():
        if int(pay[0]) == 1:
            noncash.append(int(pay[1]))
        else:
            cash.append(int(pay[1]))
    date = kwargs.get("date")

    line = f'Дата: {date[8:]}-{date[5:7]}-{date[:4]}\n' \
           f'Наличные: {sum(cash)}\n' \
           f'Безнал: {sum(noncash)}\n' \
           f'Итого: {sum(cash) + sum(noncash)}'
    return line


def sales_one_day(cur, **kwargs):
    cur.execute(
        "SELECT ds.DOC_DATE, dg.NAME, dst.QUANTITY, dst.PRICE2, dst.SUMMA2, ds.NONCASH \
         FROM DOC_SALE ds, DOC_SALE_TABLE dst , DIR_GOODS dg \
         WHERE ds.DOC_DATE LIKE '{date}%' AND ds.CODE = dst.CODE AND dst.GOOD = dg.CODE \
         ORDER BY DOC_DATE".format(**kwargs))
    data_list = []
    for row in cur.fetchall():
        no_cash = '----- Оплата картой\n' if row[5] == 1 else ''
        data_list.append(f"{str(row[0])[11:16]} {row[1]}\n--"
                         f"{int(row[2])}--{int(row[3])}--итого: <{int(row[4])}>\n{no_cash}\n")
    line = ''.join(data_list)
    line = line + daily_total(cursor, **kwargs)
    return line


def goods_list(cur, *args):
    cur.execute(
        f"SELECT SQ.CODE, SQ.NAME, Sum(QUANTITY), SQ.PRICE_ FROM ("
        f"SELECT dg.CODE, dg.NAME, dst.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SESSION_TABLE dst "
        f"WHERE dg.CODE = dst.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -dst2.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_SALE_TABLE dst2 "
        f"WHERE dg.CODE = dst2.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -dbt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_BALANCE_TABLE dbt "
        f"WHERE dg.CODE = dbt.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, +drt.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_RETURN_TABLE drt "
        f"WHERE dg.CODE = drt.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]} "
        f"UNION ALL "
        f"SELECT dg.CODE, dg.NAME, -det.QUANTITY, dg.PRICE_ "
        f"FROM DIR_GOODS dg, DOC_EXPSESSION_TABLE det "
        f"WHERE dg.CODE = det.GOOD AND dg.PARENT BETWEEN {args[0]} AND {args[1]}) SQ "
        f"GROUP BY SQ. CODE, SQ.NAME, SQ.PRICE_ "
        f"HAVING SUM(SQ.QUANTITY) >= 1 "
        f"ORDER BY SQ.PRICE_"

    )

    return cur.fetchall()


def fb_dir_goods_request(cur, **kwargs):
    cur.execute(
        "SELECT {column} FROM DIR_GOODS WHERE CODE = {code}".format(**kwargs)
    )
    return cur.fetchall()
