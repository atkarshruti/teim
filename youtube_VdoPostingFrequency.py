import os
import datetime
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

# Define your YouTube Data API key
api_key = "AIzaSyDTLuCPu1dau9izhnAIItQxSzhL3KfRm60"

# Initialize the YouTube API client
youtube = build("youtube", "v3", developerKey=api_key)


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
    plt.show()


if __name__ == "__main__":
    channel_id = "UCQoXJucsPcgpILS2nmBSqGw"  # Replace with the channel ID you want to analyze

    video_frequency = analyze_video_frequency(channel_id)
    sorted_video_frequency = dict(sorted(video_frequency.items()))

    for date, count in sorted_video_frequency.items():
        print(f"{date}: {count} videos")

    # Plot the video posting frequency
    plot_video_frequency(sorted_video_frequency)
