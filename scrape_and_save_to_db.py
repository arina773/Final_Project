from bs4 import BeautifulSoup
import requests
import sqlite3


class Author:
    def __init__(self, name: str):
        self.name = name


def add_book(title: str, author: Author, rating, customers_rated, prize):
    global conn
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT
                id
            FROM
                authors
            WHERE
                name LIKE :fname
            LIMIT 1;""",
            {
                'fname': author.name,
            }
        )

        found_author = cursor.fetchone()
        author_id = found_author[0] if found_author else add_author(author)

        cursor.execute(
            """SELECT
                id
            FROM
                books
            WHERE
                title LIKE :title
                AND rating LIKE :rating
                AND customers_rated LIKE :customers_rated
                AND prize LIKE :prize 
            LIMIT 1;""",
            {
                'title': title,
                'rating': rating,
                'customers_rated': customers_rated,
                'prize': prize,
            }
        )
        found_book = cursor.fetchone()
        if found_book:
            book_id = found_book[0]
        else:
            cursor.execute("INSERT INTO books(title, rating, customers_rated, prize) VALUES (?, ?, ?, ?)", (title, rating, customers_rated, prize))
            book_id = cursor.lastrowid

            cursor.execute(
                "INSERT INTO book_authors(book_id, author_id) VALUES (?, ?)",
                (book_id, author_id)
            )
        conn.commit()
    except sqlite3.DatabaseError as dbex:
        conn.rollback()
        print('[ERROR]', str(dbex))
    finally:
        cursor.close()


def add_author(author: Author) -> int:
    global conn
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO authors(name) VALUES (?);",
            (author.name,)
        )
        return cursor.lastrowid
    finally:
        cursor.close()


no_pages = 3


def get_data(pageNo):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    r = requests.get('https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_pg_'+str(pageNo)+'?ie=UTF8&pg='+str(pageNo), headers=headers)
    content = r.content
    soup = BeautifulSoup(content)
    alls = []
    for d in soup.findAll('div', attrs={'class':'a-section a-spacing-none aok-relative'}):
        name = d.find('span', attrs={'class':'zg-text-center-align'})
        n = name.find_all('img', alt=True)
        author = d.find('a', attrs={'class':'a-size-small a-link-child'})
        rating = d.find('span', attrs={'class':'a-icon-alt'})
        users_rated = d.find('a', attrs={'class':'a-size-small a-link-normal'})
        price = d.find('span', attrs={'class':'p13n-sc-price'})
        all1=[]
        if name is not None:
            all1.append(n[0]['alt'])
        else:
            all1.append("unknown-book")
        if author is not None:
            all1.append(author.text)
        elif author is None:
            author = d.find('span', attrs={'class':'a-size-small a-color-base'})
            if author is not None:
                all1.append(author.text)
            else:
                all1.append('0')
        if rating is not None:
            all1.append(rating.text)
        else:
            all1.append('-1')
        if users_rated is not None:
            all1.append(users_rated.text)
        else:
            all1.append('0')
        if price is not None:
            all1.append(price.text)
        else:
            all1.append('0')
        add_book(all1[0], Author(all1[1]), all1[2], all1[3], all1[4])
    return alls
results = []
for i in range(1, no_pages+1):
    conn = sqlite3.connect('library.db')
    try:
        get_data(i)
    finally:
        conn.close()
