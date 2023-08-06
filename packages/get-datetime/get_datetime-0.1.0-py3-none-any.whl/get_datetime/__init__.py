import datetime

def get_date_year():
    current_time = datetime.datetime.now()
    return current_time.year

def get_date_month():
    current_time = datetime.datetime.now()
    return current_time.month

def get_date_day():
    current_time = datetime.datetime.now()
    return current_time.day

def get_date_DM(character):
    current_time = datetime.datetime.now()
    str(current_time.day) + character + str(current_time.month)

def get_date_MD(character):
    current_time = datetime.datetime.now()
    str(current_time.month) + character + str(current_time.day)

def get_date_DMY(character):
    current_time = datetime.datetime.now()
    return str(current_time.day) + character + str(current_time.month) + character + str(current_time.year)

def get_date_MDY(character):
    current_time = datetime.datetime.now()
    return str(current_time.month) + character + str(current_time.day) + character + str(current_time.year)

def get_time_hour():
    current_time = datetime.datetime.now()
    return current_time.hour

def get_time_minute():
    current_time = datetime.datetime.now()
    return current_time.minute

def get_time_second():
    current_time = datetime.datetime.now()
    return current_time.second

def get_time_HM(character):
    current_time = datetime.datetime.now()
    return str(current_time.hour) + character + str(current_time.minute)

def get_time_HMS(character):
    current_time = datetime.datetime.now()
    return str(current_time.hour) + character + str(current_time.minute) + character + str(current_time.second)