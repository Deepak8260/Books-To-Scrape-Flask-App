from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

# List of categories
categories = {
    "Travel": "travel",
    "Mystery": "mystery",
    "Historical Fiction": "historical-fiction",
    "Sequential Art": "sequential-art",
    "Classics": "classics",
    "Philosophy": "philosophy",
    "Romance": "romance",
    "Womens Fiction": "womens-fiction",
    "Fiction": "fiction",
    "Childrens": "childrens",
    "Religion": "religion",
    "Nonfiction": "nonfiction",
    "Music": "music",
    "Default": "default",
    "Science Fiction": "science-fiction",
    "Sports and Games": "sports-and-games",
    "Fantasy": "fantasy",
    "New Adult": "new-adult",
    "Young Adult": "young-adult",
    "Science": "science",
    "Poetry": "poetry",
    "Paranormal": "paranormal",
    "Art": "art",
    "Psychology": "psychology",
    "Autobiography": "autobiography",
    "Parenting": "parenting",
    "Adult Fiction": "adult-fiction",
    "Humor": "humor",
    "Horror": "horror",
    "History": "history",
    "Food and Drink": "food-and-drink",
    "Christian Fiction": "christian-fiction",
    "Business": "business",
    "Biography": "biography",
    "Thriller": "thriller",
    "Contemporary": "contemporary",
    "Spirituality": "spirituality",
    "Academic": "academic",
    "Self Help": "self-help",
    "Historical": "historical",
    "Christian": "christian",
    "Suspense": "suspense",
    "Short Stories": "short-stories",
    "Novels": "novels",
    "Health": "health",
    "Politics": "politics",
    "Cultural": "cultural",
    "Erotica": "erotica",
    "Crime": "crime"
}

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_category = request.form.get('category')
    all_books = []

    if selected_category:
        category_url = categories[selected_category]
        url = f'https://books.toscrape.com/catalogue/category/books/{category_url}_1/index.html'
        x = requests.get(url)
        soup = bs(x.text, 'html.parser')
        books = soup.find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})

        for i in books:
            # Extract price and convert to INR
            price = i.find_all('p', {'class': 'price_color'})[0].text
            price = price.replace('Â£', '')
            price_inr = round(float(price) * 105.29, 2)

            # Extract title
            title = i.h3.a['title']

            # Extract rating
            num_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating = num_map.get(i.article.p['class'][1])

            # Extract image
            l = i.img['src'].replace('../', '')
            img = 'https://books.toscrape.com/' + l

            all_books.append((title, price_inr, rating, img))

    return render_template('books.html', books=all_books, categories=categories.keys())

if __name__ == '__main__':
    app.run(debug=True)