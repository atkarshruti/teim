# youtube sentiment analysis
# group1-marketanalysis.json
# channel id of seva youtube=UCQoXJucsPcgpILS2nmBSqGw
import os
import re
from textblob import TextBlob
from googleapiclient.discovery import build
import matplotlib.pyplot as plt

# Set up the YouTube Data API
api_key = "AIzaSyDTLuCPu1dau9izhnAIItQxSzhL3KfRm60"
youtube = build('youtube', 'v3', developerKey=api_key)


# Function to fetch comments from a YouTube video
def get_video_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        maxResults=100  # You can adjust the number of comments to retrieve
    ).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Continue to the next page of comments
        try:
            results = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                pageToken=results['nextPageToken'],
                maxResults=100
            ).execute()
        except KeyError:
            break

    return comments


# Function to perform sentiment analysis on comments
def analyze_sentiment(comments):
    positive = 0
    negative = 0
    neutral = 0

    for comment in comments:
        analysis = TextBlob(comment)
        sentiment_score = analysis.sentiment.polarity

        if sentiment_score > 0:
            positive += 1
        elif sentiment_score < 0:
            negative += 1
        else:
            neutral += 1

    total_comments = len(comments)

    sentiment_results = {
        "Positive": positive,
        "Negative": negative,
        "Neutral": neutral,
        # "TotalComments": total_comments
    }

    return sentiment_results


# Function to create a simple bar chart for sentiment visualization
def visualize_sentiment(sentiment_results):
    labels = sentiment_results.keys()
    values = sentiment_results.values()

    # plt.bar(labels, values, color=['green', 'red', 'gray'])
    # plt.title('Sentiment Analysis of YouTube Video Comments')
    # plt.xlabel('Sentiment')
    # plt.ylabel('Number of Comments')
    # plt.show()
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red', 'gray'])
    plt.title('Sentiment Analysis of YouTube Video Comments')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

# Main function
def main():
    video_url = "https://www.youtube.com/watch?v=aFbk2tdhJKA"
    video_id = re.search(r"v=([A-Za-z0-9_-]+)", video_url).group(1)

    comments = get_video_comments(video_id)
    sentiment_results = analyze_sentiment(comments)

    print("Sentiment Analysis Results:")
    # print(f"Total Comments: {sentiment_results['TotalComments']}")
    print(f"Positive Comments: {sentiment_results['Positive']}")
    print(f"Negative Comments: {sentiment_results['Negative']}")
    print(f"Neutral Comments: {sentiment_results['Neutral']}")

    # Visualize sentiment distribution
    visualize_sentiment(sentiment_results)

if __name__ == "__main__":
    main()
