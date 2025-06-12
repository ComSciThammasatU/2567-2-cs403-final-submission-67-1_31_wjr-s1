from flask import Flask, request, render_template
import pickle
import numpy as np
from utils import clean_texts
from youtube import fetch_youtube_comments
from twitter import fetch_twitter_comments
from imdb import get_movie_details
from datetime import datetime

import requests


RAPIDAPI_KEY = "04c9b82df1msh7c8ca7156ac5193p1fa850jsnebfff546a6f1"

app = Flask(__name__)

with open("model_logreg.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    platform = request.form["platform"]
    query = request.form["query"]

    if platform == "youtube":
        comments = fetch_youtube_comments(query)
    elif platform == "twitter":
        comments = fetch_twitter_comments(query)
    else:
        comments = []

    if not comments:
        return render_template("result.html", movie_title=query, error="No valid comments found.")

   
    cleaned = clean_texts(comments)

   
    X = vectorizer.transform(cleaned)
    predictions = model.predict(X)

    pos = int(np.sum(predictions == 1))
    neg = int(np.sum(predictions == -1))

    results = [
        {"text": comment, "label": int(label)}
        for comment, label in zip(comments, predictions)
    ]

    sentiment_comments = {
        "positive": [r["text"] for r in results if r["label"] == 1],
        "negative": [r["text"] for r in results if r["label"] == -1],
    }

   
    cleaned_sentiment_comments = {
        "positive": [cleaned[i] for i, label in enumerate(predictions) if label == 1],
        "negative": [cleaned[i] for i, label in enumerate(predictions) if label == -1],
    }

    movie_title = request.form['query']
    movie_info = get_movie_details(movie_title, RAPIDAPI_KEY)

    search_date = datetime.now().strftime("%d %B %Y %H:%M")

    return render_template(
        "result.html",
        movie_title=query,
        positive=pos,
        negative=neg,
        comments=sentiment_comments,
        cleaned_comments=cleaned_sentiment_comments,
        poster=movie_info['poster'],
        plot=movie_info['plot'],
        title=movie_info['title'],
        search_date=search_date,
        
        )

if __name__ == "__main__":
    app.run(debug=True)
