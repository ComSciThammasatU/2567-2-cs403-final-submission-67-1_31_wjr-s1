from googleapiclient.discovery import build
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

DetectorFactory.seed = 0

API_KEY = "AIzaSyCZshesxawlDLkmmZy3iRmaEg9MQo39hlc"

def fetch_youtube_comments(query, max_comments=500):
    try:
        youtube = build("youtube", "v3", developerKey=API_KEY)
        search = youtube.search().list(q=query, part="id", maxResults=1, type="video").execute()
        video_id = search['items'][0]['id']['videoId']
        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                textFormat="plainText",
                pageToken=next_page_token
            ).execute()

            for item in response.get("items", []):
                comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
                try:
                    if detect(comment_text) == "en":
                        comments.append(comment_text)
                        if len(comments) >= max_comments:
                            break
                except LangDetectException:
                    continue

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return comments

    except Exception as e:
        print("Error fetching comments:", e)
        return []
