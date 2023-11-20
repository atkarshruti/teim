import os
from textblob import TextBlob
from googleapiclient.discovery import build
import matplotlib.pyplot as plt

# Set up the YouTube Data API
api_key =  "AIzaSyAIxzii_3Bv5i5df2CcwZT0vsFwMUDAD4U"
youtube = build("youtube", "v3", developerKey=api_key)

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
        
    }

    return sentiment_results

# Function to create a simple bar chart for sentiment visualization
def visualize_sentiment(sentiment_results):
    labels = sentiment_results.keys()
    values = sentiment_results.values()

    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red', 'gray'])
    plt.title('Sentiment Analysis of YouTube Video Comments')
    
    image_path = 'static/image/youtube_sentiment_pie.png'
    if os.path.exists(image_path):
        os.remove(image_path)  # Remove the existing file

    plt.savefig(image_path, format="png")
    plt.close()

import os
import datetime
import matplotlib.pyplot as plt
from googleapiclient.discovery import build



def get_channel_videos(channel_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,  # You can adjust this value as needed
            order="date",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            if item["id"]["kind"] == "youtube#video":
                video = item["snippet"]
                videos.append({
                    "title": video["title"],
                    "published_at": video["publishedAt"]
                })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return videos


def analyze_video_frequency(channel_id):
    videos = get_channel_videos(channel_id)

    video_dates = [datetime.datetime.fromisoformat(video["published_at"].replace("Z", "+00:00")) for video in videos]
    video_counts = {}

    for date in video_dates:
        date_str = date.strftime("%Y-%m-%d")
        video_counts[date_str] = video_counts.get(date_str, 0) + 1

    return video_counts


def plot_video_frequency(video_frequency):
    dates = list(video_frequency.keys())
    video_counts = list(video_frequency.values())

    plt.figure(figsize=(12, 6))
    plt.plot(dates, video_counts, marker='o', linestyle='-')
    plt.title('Video Posting Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Videos')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    image_path = 'static/image/youtube_videoposting_frequency.png'
    plt.savefig(image_path, format="png")
    plt.close()
    return image_path


import os
import datetime
from googleapiclient.discovery import build
import matplotlib.pyplot as plt



def get_video_comments1(video_id):
    comments = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # You can adjust this value as needed
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "published_at": comment["publishedAt"]
            })

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments


def analyze_comment_frequency(video_id):
    comments = get_video_comments1(video_id)

    # Extract the publication dates of comments and count their frequency
    comment_dates = [datetime.datetime.fromisoformat(comment["published_at"].replace("Z", "+00:00")) for comment in
                     comments]
    comment_counts = {}

    for date in comment_dates:
        date_str = date.strftime("%Y-%m-%d")
        comment_counts[date_str] = comment_counts.get(date_str, 0) + 1

    return comment_counts

def plot_comment_frequency(comment_frequency):
    dates = list(comment_frequency.keys())
    comment_counts = list(comment_frequency.values())

    plt.figure(figsize=(12, 6))
    plt.plot(dates, comment_counts, marker='o', linestyle='-')
    plt.title('Comment Frequency Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Comments')
    plt.xticks(rotation=45)
    plt.grid(True)

    plt.tight_layout()
    
    image_path = 'static/image/youtube_comment_frequency.png'
    plt.savefig(image_path, format="png")
    plt.close()
    return image_path

def get_channel_statistics(channel_id):
    request = youtube.channels().list(
        part='statistics',
        id=channel_id
    )
    response = request.execute()

    if 'items' in response:
        channel_data = response['items'][0]['statistics']
        return channel_data
    else:
        return None

def get_channel_videos(channel_id):
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,  # You can adjust this value as needed
            order='date',
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                videos.append({
                    'title': item['snippet']['title'],
                    'published_at': item['snippet']['publishedAt']
                })

        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break

    return videos





if __name__ == "__main__":
    channel_id = "UCQoXJucsPcgpILS2nmBSqGw"  # Replace with the channel ID you want to analyze

    video_frequency = analyze_video_frequency(channel_id)
    sorted_video_frequency = dict(sorted(video_frequency.items()))

    # Plot the video posting frequency
    plot_video_frequency(sorted_video_frequency)


    video_url = "https://www.youtube.com/watch?v=gGx5KRirets"  # Replace with the YouTube video URL or ID
    video_id = video_url.split("v=")[1]

    comments = get_video_comments(video_id)
    sentiment_results = analyze_sentiment(comments)

    # Visualize sentiment distribution
    visualize_sentiment(sentiment_results)

    
    comment_frequency = analyze_comment_frequency(video_id)

    # Sort the dictionary by date
    sorted_comment_frequency = dict(sorted(comment_frequency.items()))

    plot_comment_frequency(sorted_comment_frequency)

    channel_statistics = get_channel_statistics(channel_id)

    if channel_statistics:
        total_subscribers = channel_statistics.get('subscriberCount', 'N/A')
        print(f'Total Subscribers: {total_subscribers}')

    # Get channel videos
    channel_videos = get_channel_videos(channel_id)
    total_videos = len(channel_videos)
    print(f'Total Videos: {total_videos}')