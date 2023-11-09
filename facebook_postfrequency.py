import facebook
import matplotlib.pyplot as plt
from datetime import datetime
from collections import Counter

def get_facebook_data(access_token):
    graph = facebook.GraphAPI(access_token)

    # Get user's posts
    posts = graph.get_connections("me", "posts")

    # Extract post dates and count daily posts
    post_dates = [datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S%z').date() for post in posts['data']]
    daily_post_count = Counter(post_dates)

    # Sort the dates
    sorted_dates = sorted(daily_post_count)

    # Format dates as dd/mm/yyyy
    formatted_dates = [date.strftime('%d/%m/%Y') for date in sorted_dates]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(formatted_dates, [daily_post_count[date] for date in sorted_dates], color='skyblue')
    plt.title('Daily Facebook Post Count')
    plt.xlabel('Date')
    plt.ylabel('Number of Posts')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace 'YOUR_ACCESS_TOKEN' with the actual access token
    access_token = 'EAAXduZCvr1F4BO1lOlGAr7jgtXm7vcrMlgRJHhQxFAW6mvQ1cFjVN7C29mFRxah8MtVRkVaeDpZByyAkx1Hqat7VPb6ZC3rimHRR5FxzjBtYc1beuF3XsUxPZAtARYb02zTtdoe99a4bmML3jvW9qscbcaUuSVTbjfGbf02afzrTYxADxqBerKJKosJ1c0Aozz1CdddrGYtof8yiaQZDZD'
    get_facebook_data(access_token)
