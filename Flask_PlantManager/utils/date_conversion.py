

def convert_date(date):
    #ova funkcija pretvara datum iz DD-MM-YYYY u YYYY-MM-DD format
    #to je potrebno budući da baza podataka prima takav format datuma

    list1 = list(date)
    d = list1[0:2]
    m = list1[3:5]
    y = list1[6:10]
    yyyy = "".join(y)
    mm = "".join(m)
    dd = "".join(d)
    converted_date = yyyy + "-" + mm + "-" + dd
    return converted_date
