import datetime

# This function is just for converting DD.MM.YYYY. date into datetime format

def convert_date(date):
    list1 = list(date)
    d = list1[0:2]
    m = list1[3:5]
    y = list1[6:10]
    yyyy = "".join(y)
    mm = "".join(m)
    dd = "".join(d)
    return datetime.datetime(int(yyyy), int(mm), int(dd))
