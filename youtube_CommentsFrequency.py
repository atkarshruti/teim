import os
import datetime
from googleapiclient.discovery import build
import matplotlib.pyplot as plt

# Define your YouTube Data API key
api_key = "AIzaSyDTLuCPu1dau9izhnAIItQxSzhL3KfRm60"

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)


def get_video_comments(video_id):
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
    comments = get_video_comments(video_id)

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
    plt.show()

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=gGx5KRirets"  # Replace with your video URL
    video_id = video_url.split("v=")[1]

    comment_frequency = analyze_comment_frequency(video_id)

    # Sort the dictionary by date
    sorted_comment_frequency = dict(sorted(comment_frequency.items()))

    for date, count in sorted_comment_frequency.items():
        print(f"{date}: {count} comments")

    plot_comment_frequency(sorted_comment_frequency)
