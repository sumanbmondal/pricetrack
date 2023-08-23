import requests
from bs4 import BeautifulSoup
from pony import orm
from datetime import datetime

db = orm.Database()
db.bind(provider='sqlite', filename='products.db', create_db = True)

class Products(db.Entity):
    name = orm.Required(str)
    price = orm.Required(float)
    created_at = orm.Required(datetime)

db.generate_mapping(create_tables=True)

def amazon(session):
    url = "https://www.amazon.in/Lenovo-Ideapad-39-62cm-Keyboard-82K201UEIN/dp/B0B6GJH5Q7/"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "amazon",
        float(soup.select_one("span.a-price-whole").text.replace(",",""))
    )

    return data

def flipkart(session):
    url = "https://dl.flipkart.com/s/SjVgLYuuuN"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    data = (
        "flipkart",
        float((soup.select_one("div._30jeq3._16Jk6d").text.replace("₹","")).replace(",",""))
    )

    return data

def main():
    session = requests.Session()
    session.headers.update({
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    })

    data = [
        amazon(session),
        flipkart(session)
    ]
    
    with orm.db_session:
        for item in data:
            Products(name=item[0], price=item[1], created_at = datetime.now())

if __name__ == '__main__':
    main()


