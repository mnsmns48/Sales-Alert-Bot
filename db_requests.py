import fdb

con = fdb.connect(dsn='C:/Users/DrKoffer/PycharmProjects/Sales-Alert-Bot/TASK2.fdb', user='SYSDBA',
                  password='masterkey')
cur_1 = con.cursor()


def sales(cur, date: str, month: str):
    cur.execute(
        f"SELECT ds.DOC_DATE, dg.NAME, dst.QUANTITY, dst.PRICE2, dst.SUMMA2, ds.NONCASH "
        f"FROM DOC_SALE ds, DOC_SALE_TABLE dst , DIR_GOODS dg "
        f"WHERE ds.DOC_DATE LIKE '2023-{month}-{date}%' AND ds.CODE = dst.CODE AND dst.GOOD = dg.CODE "
        f"ORDER BY DOC_DATE")
    return cur.fetchall()
