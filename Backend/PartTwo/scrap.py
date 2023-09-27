import psycopg2
from decouple import config
from bs4 import BeautifulSoup
import requests
database_URL=config('database_URL')
app_id = config('app_id')

# connecting to database here
connection = psycopg2.connect(database_URL)


cursor = connection.cursor()

# we can also run the loop till 51 for getting 50 pages 
for item in range(1,5):
    scrapp_url = f"http://books.toscrape.com/catalogue/category/books_1/page-{item}.html"
    res = requests.get(scrapp_url)
    print(res)
    # res.content -> gives html in bytes 
    # html.parser used to convert the bytes data into python object
    soup = BeautifulSoup(res.content,'html.parser')

    
    # print(loopingData)
    for book in soup.find_all('article',class_='product_pod'):

        title = book.h3.a['title']

        price = book.select('div p.price_color')[0].get_text()

        availability_elem = book.select('div p.availability')
        availability = availability_elem[0].get_text().strip() if availability_elem else None


        ratings_elem = book.select_one('p.star-rating')['class']
        ratings = ratings_elem[1] if ratings_elem else None 

        # creating the table here
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books(
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                price VARCHAR(50),
                availability VARCHAR(255),
                ratings VARCHAR(10)
            )
        ''')

        cursor.execute('''
            INSERT INTO books(title,price,availability,ratings)
            VALUES(%s,%s,%s,%s)
        ''',(title,price,availability,ratings))

# commit the changes to database
connection.commit()

# close the cursor and database connection

cursor.close()
connection.close()
