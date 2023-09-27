import requests
import psycopg2
from decouple import config
app_id = '65141aaebac0bd0d974cabe5'
databaseurl = config('database_URL')
users_api_url = 'https://dummyapi.io/data/v1/user'

connection = psycopg2.connect(databaseurl)

cursor = connection.cursor()

response = requests.get(users_api_url,headers={'app-id':app_id})
user_Data = response.json()
# print(user_Data)

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
