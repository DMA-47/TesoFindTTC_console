from selenium.webdriver import Chrome
import time
from datetime import datetime
import winsound
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

time_delay = 5
time_back_min_1 = 0
time_back_min_2 = 0
time_back_min_1_now = 0
time_back_min_2_now = 0

nirn_price1 = 30000
nirn_price2 = 5000
max_price1 = 1900
max_num = 5
max_price2 = 830
sound_sign = False
num_error = 0


def err():
    global num_error
    print('malo time')
    num_error += 1
    if num_error > 20:
        winsound.Beep(1000, 200)
        winsound.Beep(1000, 200)
        winsound.Beep(1000, 200)
        num_error = 0
    time.sleep(1)


def get_time_back(trade_line):
    line = trade_line.find_elements_by_tag_name('td')
    time_back = line[4].text
    if time_back.split()[0] == 'сейчас':
        time_back = 0
    else:
        time_back = int(time_back.split()[0])
        time_back = time_back * 60 if line[4].text.find('ч') >= 0 else time_back
    return time_back
    

def list1():
    global time_back_min_1_now
    list = []
    url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=2677&AmountMin=' + \
          str(max_num) + '&PriceMax=' + str(max_price1) + '&lang=ru-RU'
    driver.get(url)

    while True:
        try:
            trade_list = driver.find_element_by_class_name('trade-list-table').find_elements_by_class_name('cursor-pointer')
            trade_list = trade_list[3:]
            break
        except:
            err()
    
    
    for i in range(len(trade_list)):
        line = trade_list[i].find_elements_by_tag_name('td')

        item_name = line[0].find_elements_by_class_name('item-quality-legendary')[1].text
        location = line[2].text.split('\n')
        if len(location) == 1:
            location.append('None')
        price = line[3].text.replace(' ', '').replace(',', '.').split('\n')
        price_one = float(price[0])
        item_amount = float(price[2])
        price_all = float(price[4])
        time_back = get_time_back(trade_list[i])

        list.append([item_name, location[0], location[1], price_one, item_amount, price_all, time_back])
    
    time_back_min_1_now = list[0][6]
    print(time_back_min_1_now)
    
    return list


def print1(list):
    global sound_sign

    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 10, '-' * 66, '-' * 31, '-' * 6, '-' * 5, '-' * 8, '-' * 6))
    print('| {:<9}| {:<65}| {:<30}| {:<5}| {:<4}| {:<7}| {:<4} |'.
          format('Name', 'Location', 'Guild', 'Price', 'Num', 'All', 'Time'))
    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 10, '-' * 66, '-' * 31, '-' * 6, '-' * 5, '-' * 8, '-' * 6))

    for i in list:
        if i[6] < time_delay + time_back_min_1:
            print('\033[42m| {:<9}| {:<65}| {:<30}| {:<5.0f}| {:<4.0f}| {:<7.0f}| {:<4} |\033[0m'.
                  format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            sound_sign = True
        else:
            print('| {:<9}| {:<65}| {:<30}| {:<5.0f}| {:<4.0f}| {:<7.0f}| {:<4} |'.
                  format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 10, '-' * 66, '-' * 31, '-' * 6, '-' * 5, '-' * 8, '-' * 6))


def list2_default(trade_list, list=[], ind_nirn=0):
    global sound_sign
    for trade_line in trade_list:
        ind_nirn1 = 0
        ind_nirn2 = 0
        line = trade_line.find_elements_by_tag_name('td')

        item_name = line[0].find_element_by_class_name('trade-item-icon').get_attribute("title")
        if item_name.find('лук') >= 0:
            item_name = 'Лук'
            ind_nirn1 = 1
        elif item_name.find('посох') >= 0:
            item_name = 'Посох'
            ind_nirn1 = 1
        else:
            item_name = 'Щит'
            ind_nirn2 = 1
        voucher_amount = int(line[0].text.split()[5])
        location = line[2].text.split('\n')
        if len(location) == 1:
            location.append('None')
        price = line[3].text.replace(' ', '').replace(',', '.').split('\n')
        price_one = float(price[0])
        price_for_voucher = (price_one + 22000 + (
                    nirn_price1 * ind_nirn1 + nirn_price2 * ind_nirn2) * ind_nirn) / voucher_amount
        time_back = get_time_back(trade_line)

        if price_for_voucher < max_price2:
            list.append([item_name, voucher_amount, location[0], location[1], price_one, price_for_voucher, time_back])

    return list


def list2():
    global num_error, time_back_min_2_now
    url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=12749&ItemNamePattern' \
          '=Запечатанный+заказ+для+столяров&ItemQualityID=4&PriceMax=' + str(25000) + '&lang=ru-RU'
    driver.get(url)


    while True:
        try:
            trade_list = driver.find_element_by_class_name('trade-list-table').find_elements_by_class_name(
                'cursor-pointer')
            trade_list = trade_list[3:]
            break
        except:
            err()
            
    
    list = []
    list = list2_default(trade_list, list, 0)
    time_back_min_2_now = list[0][6]
    len_list = len(list)
    print(time_back_min_2_now)


    url = 'https://eu.tamrieltradecentre.com/pc/Trade/SearchResult?ItemID=12749&ItemNamePattern' \
          '=Запечатанный+заказ+для+столяров&ItemQualityID=4&MasterWritVoucherMin=85&PriceMax=' + str(130000) + '&lang=ru-RU'
    driver.get(url)
    while True:
        try:
            trade_list = driver.find_element_by_class_name('trade-list-table').find_elements_by_class_name(
                'cursor-pointer')
            trade_list = trade_list[3:]
            break
        except:
            err()
            
    
    list2_default(trade_list, list, 1)
    
    if len(list) != len_list:
        temp = list[len_list][6]
        if temp < time_back_min_2_now:
            time_back_min_2_now = temp
    print(time_back_min_2_now)
    
    return list


def print2(list):
    global sound_sign

    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 8, '-' * 6, '-' * 65, '-' * 31, '-' * 8, '-' * 8, '-' * 6))
    print('| {:<7}| {:<4} |{:<65}| {:<30}| {:<7}| {:<7}| {:<4} |'.
          format('Name', 'Num', 'Location', 'Guild', 'Price', 'Voucher', 'Time'))
    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 8, '-' * 6, '-' * 65, '-' * 31, '-' * 8, '-' * 8, '-' * 6))

    for i in list:
        if i[6] < time_delay + time_back_min_2:
            print('\033[42m| {:<7}| {:<4} |{:<65}| {:<30}| {:<7.0f}| {:<7.0f}| {:<4} |\033[0m'.
                  format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
            sound_sign = True
        else:
            print('| {:<7}| {:<4} |{:<65}| {:<30}| {:<7.0f}| {:<7.0f}| {:<4} |'.
                  format(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

    print('+{}+{}+{}+{}+{}+{}+{}+'.format('-' * 8, '-' * 6, '-' * 65, '-' * 31, '-' * 8, '-' * 8, '-' * 6))


driver = Chrome(executable_path="./chromedriver.exe")

while True:
    num_error = 0
    list_1 = list1()
    list_2 = list2()
    
    print(datetime.now(), time_back_min_1 + 5, time_back_min_2 + 5)
    print1(list_1)
    print2(list_2)
    time_back_min_2 = time_back_min_2_now
    time_back_min_1 = time_back_min_1_now

    if sound_sign:
        winsound.Beep(800, 300)
        winsound.Beep(800, 300)
        sound_sign = False
    
    time.sleep(time_delay * 60)

