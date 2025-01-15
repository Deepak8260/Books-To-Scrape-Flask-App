from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route('/')
def home():
    # Scrape the data
    x = requests.get('https://books.toscrape.com/catalogue/category/books/music_14/index.html')
    soup = bs(x.text, 'html.parser')
    books = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

    # Extract prices and convert to INR
    prices = []
    conversion_rate = 105.29  # Example conversion rate from GBP to INR
    for i in books:
        price = i.find_all('p', {'class': 'price_color'})[0].text
        price = price.replace('Â£', '')
        prices.append(round(float(price) * conversion_rate, 2))

    # Extract titles
    titles = [i.h3.a['title'] for i in books]

    # Extract ratings
    num_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    ratings = [num_map.get(i.article.p['class'][1]) for i in books]

    # Extract images
    imgs = []
    for i in books:
        l = i.img['src'].replace('../', '')
        img = 'https://books.toscrape.com/' + l
        imgs.append(img)

    # Render the template with data and pass zip function
    return render_template('books.html', titles=titles, prices=prices, ratings=ratings, imgs=imgs, zip=zip)

if __name__ == '__main__':
    app.run(debug=True)