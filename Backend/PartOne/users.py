# http library
import requests

#connection to postgresSQL
import psycopg2

# for enviroment variables
from decouple import config

app_id = config('app_id')

databaseurl = config('database_URL')

users_api_url = 'https://dummyapi.io/data/v1/user'

connection = psycopg2.connect(databaseurl)

# for intraction with database
cursor = connection.cursor()

# making the request for data
response = requests.get(users_api_url,headers={'app-id':app_id})

#converting from json to simple data for manipulation of data
user_Data = response.json()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        firstName VARCHAR(255),
        lastName VARCHAR(255),
        picture VARCHAR(400)
       
    )
''')
for user in user_Data['data']:
    cursor.execute('''
        INSERT INTO users (id, title, firstName,lastName,picture)
        VALUES (%s, %s,%s,%s,%s)
    ''', (user['id'], user['title'],user['firstName'],user['lastName'],user['picture']))


connection.commit()
cursor.close()
connection.close()
