import random 
import string 
import pandas as pd
import os
from datetime import datetime
import glob
import configparser

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

# создаем словарь с категориями, в котором лежат товары и их стоимость
products = { 
    'Бытовая химия': {"Гель для стирки": 15, "Таблетки для посудомоечной машины": 20, "Средство для плит и духовок": 10,
        "Освежитель воздуха": 14, "Средство для кофеварки": 12, "Средство для кухни": 17, "Кондиционер для белья": 22,
        "Ополаскиватель для посудомоечной машины": 18},
    'Посуда': {"Сковорода": 145,"Чайник": 115,"Кастрюля": 100,"Кружка": 105,"Миска для смешивания": 50,"Тарелка обеденная": 55,
       "Набор салатников": 185,"Набор стаканов": 60}, 
    'Текстиль': {"Скатерть квадратная": 92,"Салфетка под тарелку": 54,"Полотенце кухонное": 67,
       "Полотенце махровое": 88, "Набор рукавиц-прихваток": 56,"Обои с узором": 76,
       "Чехол для подушки декоративной": 70,"Подушка-вкладыш": 61}
    }

# функция для генерации рандомного айди чека
def generate_id(length=8):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choices(characters, k=length))
    return random_id

# функция рассчета значения скидки
def calculate_discount(price):
    if price > 100:
        return 0.05 * 100 
    elif price > 50:
        return 0.02 * 100
    else:
        return 0

# функция для генерации рандомных значений в чеке
def random_check():
    cap = random.randint(1, 10)
    doc_id = generate_id()
    selected_items = set()
    check_items = []
    for _ in range(cap):
        category = random.choice(list(products.keys()))
        item, price = random.choice(list(products[category].items()))
        discount = calculate_discount(price)
        if item not in selected_items:
            amount =  random.randint(1, 5)
            selected_items.add(item)
            check_items.append({
            'doc_id': doc_id,
            'category': category,
            'item': item,
            'price': price,
            'amount': amount,
            'discount': discount
    })
    return  check_items

# генерируем рандомное кол-во чеков для рандомного кол-ва магазинов(у каждого из которых 3 кассы)
all_check = []
shop_num = random.randint(1, 10)
for store_id in range(1, shop_num + 1):
    cash_num = 3
    for cash_id in range(1, cash_num + 1):
        check_num = random.randint(1, 5) 
        for num in range(check_num):
            check_ = random_check()
            for r in check_:
                r['store_id'] = store_id     
                r['cash_id'] = cash_id
            all_check.extend(check_)

# создаем папку для хранения файлов и удаляем старые файлы, чтобы они не накладывались на новые
folder =  "data"
if not os.path.exists(folder):
    os.makedirs(folder)
files = glob.glob(os.path.join(folder, '*.csv'))
for f in files:
    os.remove(f)

# делаем из всех словарей единный датафрейм и добавляем проверку по дате
today_weekday = datetime.now().weekday()
if today_weekday == 6:
    print("Сегодня воскресенье — CSV-файлы не выгружаются.")
else:
    united = []
    for receipt in all_check:
        store = receipt['store_id']
        cash_id = receipt['cash_id']
        check_id = receipt['doc_id']
        for items in receipt['doc_id']:
            uni = {'shop_num': store,
            'cash_num': cash_id,
            'doc_id': check_id,
            'category': receipt['category'],
            'item': receipt['item'],
            'price': receipt['price'],
            'amount': receipt['amount'],
            'discount': receipt['discount']}
        united.append(uni)
        df = pd.DataFrame(united)
        grouped = df.groupby(['shop_num', 'cash_num'])
        for (shop_num, cash_num), group in grouped:
            group_to_save = group.drop(columns=['shop_num', 'cash_num'])
            filename = f"{shop_num}_{cash_num}.csv"
            filepath = os.path.join(folder, filename)
            group_to_save.to_csv(os.path.join(dirname, filepath), index=False)

