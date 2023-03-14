from datetime import date, timedelta

date_t = date.today()
date_y = date_t - timedelta(days=1)

date_today = str(date_t)[-2:]
month_today = str(date_t)[-5:-3]

date_yesterday = str(date_y)[-2:]
month_yesterday = str(date_y)[-5:-3]
