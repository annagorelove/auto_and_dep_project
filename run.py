import configparser
import os
import pandas as pd
import glob 
import inspect
from pg import Database

module_file = inspect.getfile(Database)
absolute_path = os.path.abspath(module_file)

dirname = os.path.dirname(__file__)

config = configparser.ConfigParser()
config.read(os.path.join(dirname, 'config.ini'))

PATH = config["Files"]["PATH"]
DATABASE_ = config["Database"]
all_csv = glob.glob(PATH)
full_path = os.path.join(dirname, PATH)

dataframes = []

# объединяем все CSV-файлы в один 
for file in all_csv:
    df = pd.read_csv(file)  
    df['source_file'] = os.path.abspath(full_path)
    dataframes.append(df)
    os.remove(file)
if dataframes:
    full_df = pd.concat(dataframes, ignore_index=True)
    print(full_df)
else:
    full_df = pd.DataFrame()

database = Database(
    host = DATABASE_["HOST"],
    port = DATABASE_["PORT"],
    database = DATABASE_["DATABASE"],
    user = DATABASE_["USER"],
    password = DATABASE_["PASSWORD"]
)

# удаляем старые данные и вставляем новые для таблицы товары 
delete_query = "delete from products"
database.post(delete_query)
values = ', '.join([f"('{row['category']}', '{row['item']}', {row['price']})" for _, row in full_df.iterrows()])
if values:
    query = f"""
    INSERT INTO products (category, item, price)
    VALUES {values}
    ON CONFLICT (category, item, price) DO NOTHING;
    """
    database.post(query)
else:
    next


# удаляем старые данные и вставляем новые для таблицы скидка 
delete_query = "delete from discount"
database.post(delete_query)
values = ', '.join([f"({row['price']}, {row['discount']})" for _, row in full_df.iterrows()])
if values:
    query = f"""
    INSERT INTO discount (price, discount)
    VALUES {values}
    ON CONFLICT (price, discount) DO NOTHING;
    """
    database.post(query)
else:
    next


# удаляем старые данные и вставляем новые для таблицы чек магазина
delete_query = "delete from store_receipt"
database.post(delete_query)
for i, row in full_df.iterrows():
    query = f"INSERT INTO store_receipt VALUES ('{row['doc_id']}', '{row['item']}', {row['amount']}, '{row['category']}', {row['price']}, {row['discount']})"
    database.post(query)
