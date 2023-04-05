"""
Calculate index for product.
1. Get product name and price from DB
2. Get kkal from food table
3. Calculate food index
4. Write food and index to db

"""

from asyncio import constants
from cgi import test
import mysql.connector
import configparser
from datetime import datetime
from constants import food_list, dixy_prod_list, food_custom

config = configparser.ConfigParser()
config.sections()
config.read('config.ini')

host = config['MySQL']['host']
user = config['MySQL']['user']
database = config['MySQL']['database']
password = config['MySQL']['password']


def timestamp():
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

mycursor = mydb.cursor(buffered=True)


food_list = food_list  #From constants

def get_calories_striict(food_list):
    sql = "SELECT name, calories, units_name from chefexpert WHERE name = %s"
    val = food_list
    mycursor.execute(sql, (val,))
    answer = mycursor.fetchall()
    
    return(answer)


def get_calories(food_list):
    sql = f"SELECT name, calories, units_name from chefexpert WHERE name\
         like '%{food_list}%'"
    val = food_list
    mycursor.execute(sql)
    answer = mycursor.fetchall()
    
    return(answer)

for el in food_custom:
    # print(el)
    print(get_calories(el))

def get_dixy_price(dixy_prod_list, food_list):
    sql = "SELECT"
    pass