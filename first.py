import requests
from bs4 import BeautifulSoup
import psycopg2

def create_database():
    connection = psycopg2.connect(
        host='localhost',
        user='sreelakshmi',
        password='',
        database='sreelakshmi'
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ChildrensBooks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            author TEXT,
            genre TEXT
        )
    ''')

    connection.commit()
    connection.close()

def scrape_and_insert_data():
    url = 'https://www.goodreads.com/shelf/show/childrens'

    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        books = soup.find_all('div', class_='elementList')

        connection = psycopg2.connect(
            host='localhost',
            user='sreelakshmi',
            password='',
            database='sreelakshmi'
        )
        cursor = connection.cursor()

    
        for book in books:
            title_element = book.find('a', class_='bookTitle')
            title = title_element.text.strip() if title_element else 'N/A'

            author_element = book.find('a', class_='authorName')
            author = author_element.find('span', itemprop='name').text.strip() if author_element else 'N/A'

            genre_element = book.find('div', class_='elementList')
            genre = genre_element.text.strip() if genre_element else 'N/A'

           
            cursor.execute('''
                INSERT INTO ChildrensBooks (title, author, genre)
                VALUES (%s, %s, %s)
            ''', (title, author, genre))

            print(f"Inserted: Title: {title}, Author: {author}, Genre: {genre}")

        connection.commit()
        connection.close()
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

def retrieve_and_display_data():
    connection = psycopg2.connect(
        host='localhost',
        user='sreelakshmi',
        password='',
        database='sreelakshmi'
    )
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM BookInfo')
    data = cursor.fetchall()

    for row in data:
        print(row)

    connection.close()

if __name__ == '__main__':
    create_database()
    scrape_and_insert_data()
    retrieve_and_display_data()
