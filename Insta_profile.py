import instaloader

# Initialize an Instaloader instance
L = instaloader.Instaloader()

# Enter the Instagram username of the account you want to fetch info for
username = 'b.techproject_2024'

try:
    # Fetch the profile of the Instagram account
    profile = instaloader.Profile.from_username(L.context, username)
    total_igtv_videos = 1
    for post in profile.get_posts():
        if post.typename == 'GraphVideo':
            total_igtv_videos += 1

    print(f"Total IGTV Videos: {total_igtv_videos}")
    # Print the account information
    print(f"Username: {profile.username}")
    print(f"Full Name: {profile.full_name}")
    print(f"Followers: {profile.followers}")
    print(f"Following: {profile.followees}")
    print(f"Total Posts: {profile.mediacount}")
    print(f"Bio: {profile.biography}")
    print(f"Profile Pic URL: {profile.get_profile_pic_url()}")
except instaloader.exceptions.ProfileNotExistsException:
    print(f"The Instagram account '{username}' does not exist.")



# Close the Instaloader instance
L.context.log("Done.")
