from flask import Flask
import os
import pandas as pd
from google_play_scraper import Sort, reviews_all, search

app = Flask(__name__)

@app.route("/")
def home():
    return "Google Play Scraper is running!"

@app.route("/scrape")
def scrape():
    if not os.path.exists('data'):
        os.makedirs('data')

    category_keyword = "lifestyle"
    apps = search(category_keyword, lang="en", country="us", n_hits=5)

    all_reviews = []

    for app_data in apps:
        app_id = app_data['appId']
        try:
            result = reviews_all(
                app_id,
                sleep_milliseconds=1000,
                lang='en',
                country='us',
                sort=Sort.NEWEST
            )
            for r in result:
                r['appId'] = app_id

            all_reviews.extend(result)

        except Exception as e:
            print(e)

    if all_reviews:
        df = pd.DataFrame(all_reviews)
        df.to_csv('data/category_reviews.csv', index=False)

    return f"Scraping complete. Total reviews: {len(all_reviews)}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)