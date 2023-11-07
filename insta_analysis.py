import instaloader
import pandas as pd
import matplotlib.pyplot as plt

# Define the Instagram username you want to analyze
username = 'b.techproject_2024'

# Create an Instaloader instance
L = instaloader.Instaloader()

# Load the profile of the specified username
profile = instaloader.Profile.from_username(L.context, username)

# Create an empty list to store the data
data = []

# Fetch and store the data for each post
for post in profile.get_posts():
    data.append({
        'Date': post.date_utc.date(),  # Extract the date (without time)
        'Likes': post.likes,
        'Comments': post.comments,
        'Caption': post.caption,
    })

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Data Analysis
# Calculate total likes and comments
total_likes = df['Likes'].sum()
total_comments = df['Comments'].sum()

# Calculate average likes and comments per post
average_likes_per_post = total_likes / len(df)
average_comments_per_post = total_comments / len(df)

# Count daily posts
daily_post_counts = df['Date'].value_counts().sort_index()

# Data Visualization
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.bar(['Likes', 'Comments'], [total_likes, total_comments])
plt.title('Total Likes and Comments')

plt.subplot(1, 2, 2)
plt.bar(['Likes per Post', 'Comments per Post'], [average_likes_per_post, average_comments_per_post])
plt.title('Average Likes and Comments per Post')

plt.show()

# Present the results
print(f"Instagram Account Analysis for {username}:")
print(f"Total Likes: {total_likes}")
print(f"Total Comments: {total_comments}")
print(f"Average Likes per Post: {average_likes_per_post:.2f}")
print(f"Average Comments per Post: {average_comments_per_post:.2f}")
print("Most Liked Posts:")
for post in sorted(data, key=lambda x: x['Likes'], reverse=True)[:5]:
    print(f"  - Likes: {post['Likes']}")
    print(f"  - Caption: {post['Caption']}")
print("Most Commented Posts:")
for post in sorted(data, key=lambda x: x['Comments'], reverse=True)[:5]:
    print(f"  - Comments: {post['Comments']}")
    print(f"  - Caption: {post['Caption']}")

print("\nDaily Post Analysis:")
print(daily_post_counts)

# Plot daily post counts
plt.figure(figsize=(12, 6))
daily_post_counts.plot(kind='bar')
plt.title('Daily Post Counts')
plt.xlabel('Date')
plt.ylabel('Number of Posts')
plt.show()
