from decouple import config
import psycopg2
import requests
import json
databaseurl = config('database_URL')
connection = psycopg2.connect(databaseurl)
# intacting with database with cursor
cursor = connection.cursor()

app_id = config('app_id')

cursor.execute('SELECT id FROM users')
user_id = cursor.fetchall()
# print(user_id)
for u_id in user_id:
    u_id = u_id[0]
    res = requests.get(
        f"https://dummyapi.io/data/v1/user/{u_id}/post", headers={'app-id': app_id})
    posts_Data = res.json()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts(
            id VARCHAR(255) PRIMARY KEY,
            image VARCHAR(400),
            likes INT,
            owner JSONB,
            publishDate TIMESTAMP,
            tags TEXT[],
            text TEXT
        )
    ''')

    for post in posts_Data['data']:
        owner_json = json.dumps(post['owner'])
        cursor.execute('''
        INSERT INTO posts (id,image,likes,owner,publishDate,tags,text)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''', (post['id'], post['image'], post['likes'], owner_json, post['publishDate'], post['tags'], post['text']))

# saving the changes to the database
connection.commit()
# close database cursor
cursor.close()
# connection close of database 
connection.close()
