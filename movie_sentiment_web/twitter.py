import requests

BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAOmLxQEAAAAAGDVGF%2FzcuVsilpqPAWUTXJNMSuo%3D9dd4zWWJmzwTrWOcKZLAvFCLKNDBBQzerB0hC87YUowFZKYip7"  # แนะนำให้ใช้ os.getenv("TWITTER_BEARER_TOKEN") แทน

def fetch_twitter_comments(hashtag, max_results=50):
    if not BEARER_TOKEN:
        raise ValueError("TWITTER_BEARER_TOKEN is missing.")

    query = f"#{hashtag} lang:en -is:retweet"
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "query": query,
        "tweet.fields": "lang,text",
        "max_results": min(max_results, 100)
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")  # ✅ เพิ่มบรรทัดนี้
        return []

    tweets = response.json().get("data", [])
    return [tweet["text"] for tweet in tweets if tweet["lang"] == "en"]
