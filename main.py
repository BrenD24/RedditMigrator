import praw
import webbrowser

# Reddit API credentials for the old and new accounts
old_account_creds = {
    'client_id': 'OLD_CLIENT_ID',
    'client_secret': 'OLD_CLIENT_SECRET',
    'username': 'OLD_USERNAME',
    'password': 'OLD_PASSWORD',
    'user_agent': 'Old Account Script'
}

new_account_creds = {
    'client_id': 'NEW_CLIENT_ID',
    'client_secret': 'NEW_CLIENT_SECRET',
    'username': 'NEW_USERNAME',
    'password': 'NEW_PASSWORD',
    'user_agent': 'New Account Script'
}

# Function to log in to Reddit with PRAW
def login_reddit(credentials):
    reddit = praw.Reddit(
        client_id=credentials['client_id'],
        client_secret=credentials['client_secret'],
        username=credentials['username'],
        password=credentials['password'],
        user_agent=credentials['user_agent']
    )
    return reddit

# Get list of saved posts (submissions and comments) from old account
def get_saved_posts(reddit):
    saved_posts = []
    for item in reddit.user.me().saved(limit=None):
        saved_posts.append(item)
    return saved_posts

# Save posts and comments on the new account
def save_posts_on_new_account(reddit, saved_posts):
    for item in saved_posts:
        if isinstance(item, praw.models.Submission):
            reddit.submission(item.id).save()
            print(f"Saved post: {item.title}")
        elif isinstance(item, praw.models.Comment):
            reddit.comment(item.id).save()
            print(f"Saved comment: {item.body[:30]}...")  # Display a snippet of the comment

# Get list of friends (followed users) from old account
def get_followed_users(reddit):
    followed_users = []
    for friend in reddit.user.friends():
        followed_users.append(friend.name)
    return followed_users

# Follow users on the new account
def follow_users_on_new_account(reddit, users):
    for user in users:
        reddit.redditor(user).friend()
        print(f"Followed {user}")

# Get list of subreddits the user is subscribed to
def get_subscribed_subreddits(reddit):
    subscribed_subreddits = []
    for subreddit in reddit.user.subreddits(limit=None):  # Gets all subreddits
        subscribed_subreddits.append(subreddit.display_name)
    return subscribed_subreddits

# Subscribe to subreddits on the new account
def subscribe_to_subreddits(reddit, subreddits):
    for subreddit in subreddits:
        reddit.subreddit(subreddit).subscribe()
        print(f"Subscribed to {subreddit}")

# Main function to handle migration
def main():
    # Log in to old and new accounts
    print("Logging into the old account...")
    old_reddit = login_reddit(old_account_creds)

    print("Logging into the new account...")
    new_reddit = login_reddit(new_account_creds)

    # Step 1: Transfer saved posts and comments
    print("Fetching saved posts from old account...")
    old_saved_posts = get_saved_posts(old_reddit)
    print(f"Found {len(old_saved_posts)} saved posts/comments.")

    print("Saving posts to new account...")
    save_posts_on_new_account(new_reddit, old_saved_posts)

    # Step 2: Transfer friends (followed users)
    print("Fetching followed users from old account...")
    old_followed_users = get_followed_users(old_reddit)
    print(f"Found {len(old_followed_users)} followed users.")

    print("Following users on new account...")
    follow_users_on_new_account(new_reddit, old_followed_users)

    # Step 3: Transfer subreddit subscriptions
    print("Fetching subscribed subreddits from old account...")
    old_subreddits = get_subscribed_subreddits(old_reddit)
    print(f"Found {len(old_subreddits)} subscribed subreddits.")

    print("Subscribing to subreddits on new account...")
    subscribe_to_subreddits(new_reddit, old_subreddits)

    print("Migration complete!")

if __name__ == "__main__":
    main()
