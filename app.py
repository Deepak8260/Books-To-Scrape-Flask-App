from flask import Flask, render_template, request
import requests
import os
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

# List of categories with their corresponding IDs
categories = {
    "Travel": "travel_2",
    "Mystery": "mystery_3",
    "Historical Fiction": "historical-fiction_4",
    "Sequential Art": "sequential-art_5",
    "Classics": "classics_6",
    "Philosophy": "philosophy_7",
    "Romance": "romance_8",
    "Womens Fiction": "womens-fiction_9",
    "Fiction": "fiction_10",
    "Childrens": "childrens_11",
    "Religion": "religion_12",
    "Nonfiction": "nonfiction_13",
    "Music": "music_14",
    "Default": "default_15",
    "Science Fiction": "science-fiction_16",
    "Sports and Games": "sports-and-games_17",
    "Fantasy": "fantasy_18",
    "New Adult": "new-adult_19",
    "Young Adult": "young-adult_20",
    "Science": "science_21",
    "Poetry": "poetry_22",
    "Paranormal": "paranormal_23",
    "Art": "art_24",
    "Psychology": "psychology_25",
    "Autobiography": "autobiography_26",
    "Parenting": "parenting_27",
    "Adult Fiction": "adult-fiction_28",
    "Humor": "humor_29",
    "Horror": "horror_30",
    "History": "history_31",
    "Food and Drink": "food-and-drink_32",
    "Christian Fiction": "christian-fiction_33",
    "Business": "business_34",
    "Biography": "biography_35",
    "Thriller": "thriller_36",
    "Contemporary": "contemporary_37",
    "Spirituality": "spirituality_38",
    "Academic": "academic_39",
    "Self Help": "self-help_40",
    "Historical": "historical_41",
    "Christian": "christian_42",
    "Suspense": "suspense_43",
    "Short Stories": "short-stories_44",
    "Novels": "novels_45",
    "Health": "health_46",
    "Politics": "politics_47",
    "Cultural": "cultural_48",
    "Erotica": "erotica_49",
    "Crime": "crime_50"
}

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_category = request.form.get('category')
    all_books = []

    if selected_category:
        category_url = categories[selected_category]
        url = f'https://books.toscrape.com/catalogue/category/books/{category_url}/index.html'
        print(f"Scraping URL: {url}")  # Debugging statement
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

        print(f"Books found: {len(all_books)}")  # Debugging statement

    return render_template('books.html', books=all_books, categories=categories.keys(), selected_category=selected_category)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)