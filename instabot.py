# Importing requests library to facilitate the access of data in our program from the internet
import requests
# Importing Textblob library to analyze and delete negative comments
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import urllib

# Declaring the access token and the base URL as global variables as the have to be used multiple times
ACCESS_TOKEN = '745963540.3ed3194.7c6b0edac759468fbc4eed4671259161'
BASE_URL = 'https://api.instagram.com/v1/'


# Defining function to get our own information
def self_info():
    req_url = BASE_URL + 'users/self/?access_token=' + ACCESS_TOKEN
    print('The request URL is %s' % req_url)
    user_info = requests.get(req_url).json()

    # To output the recieved data in more user-friendly way
    if user_info['meta']['code'] == 200:
        if len(user_info['data']) > 0:
            print('Username: %s' % (user_info['data']['username']))
            print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
            print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print('No. of posts: %s' % (user_info['data']['counts']['media']))
        else:
            print('User does not exist!')
    else:
        print('Status code other than 200 received!')


# Defining a function to get the user_id of a user by entering his username
def get_user_id(username):
    req_url = BASE_URL + 'users/search?q=' + username + '&access_token=' + ACCESS_TOKEN
    user_info = requests.get(req_url).json()

    # Printing out the user_id in a readable way
    if user_info['meta']['code'] == 200:
        if len(user_info['data']) > 0:
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print('Status code other than 200 received!')
        exit()


# Defining a function to get user info using the username
def get_user_info(username):
    user_id = get_user_id(username)  # Using the previous get_user_id function to get the user_id
    if user_id is None:
        print('The user does not exist')
        exit()
    req_url = BASE_URL + 'users/' + user_id + '/?access_token=' + ACCESS_TOKEN
    print(req_url)
    user_info = requests.get(req_url).json()

    # Printing the user details in a readable way
    if user_info['meta']['code'] == 200:
        if len(user_info['data']) > 0:
            print('Username: %s' % (user_info['data']['username']))
            print('No. of followers: %s' % (user_info['data']['counts']['followed_by']))
            print('No. of people you are following: %s' % (user_info['data']['counts']['follows']))
            print('No. of posts: %s' % (user_info['data']['counts']['media']))
        else:
            print('There is no data for this user!')
    else:
        print('Status code other than 200 received!')


# Defining the function to get our own recent post
def get_own_post():
    req_url = BASE_URL + 'users/self/media/recent/?access_token=' + ACCESS_TOKEN
    media_self = requests.get(req_url).json()

    if media_self['meta']['code'] == 200:
        if len(media_self['data']):
            image_name = media_self['data'][0]['id'] + '.jpeg'
            image_url = media_self['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print('Your image has been downloaded!')
        else:
            print('Post does not exist!')
    else:
        print('Status code other than 200 received!')


# Defining the function to get recent post of a user
def get_user_post(username):
    user_id = get_user_id(username)
    if user_id is None:
        print('The user does not exist')
        exit()
    req_url = BASE_URL + 'users/' + user_id + '/media/recent/?access_token=' + ACCESS_TOKEN
    media_user = requests.get(req_url).json()
    if media_user['meta']['code'] == 200:
        if len(media_user['data']):
            image_name = media_user['data'][0]['id'] + '.jpeg'
            image_url = media_user['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print('Your image has been downloaded!')
        else:
            print('Post does not exist!')
    else:
        print('Status code other than 200 received!')


# Defining a function to get the media_id of the recent post of a user
def get_post_id(username):
    user_id = get_user_id(username)
    if user_id is None:
        print('User does not exist!')
        exit()
    req_url = BASE_URL + 'users/' + user_id + '/media/recent/?access_token=' + ACCESS_TOKEN
    user_media = requests.get(req_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print('There is no recent post of the user!')
            exit()
    else:
        print('Status code other than 200 received!')
        exit()


# Defining the function to like the recent post of a user
def like_post(username):
    media_id = get_post_id(username)
    req_url = BASE_URL + 'media/' + media_id + '/likes'
    payload = {"access_token": ACCESS_TOKEN}
    post_a_like = requests.post(req_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print('Like was successful!')
    else:
        print('Your like was unsuccessful. Try again!')


# Defining a function to post a comment on the recent post of a user
def post_a_comment(username):
    media_id = get_post_id(username)
    comment = input("Your comment: ")
    payload = {"access_token": ACCESS_TOKEN, "text": comment}
    req_url = BASE_URL + 'media/' + media_id + '/comments'

    make_comment = requests.post(req_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print("Successfully added a new comment!")
    else:
        print("Unable to add comment. Try again!")


# Defining a function to delete negative comments from the recent post of a user
def delete_negative_comment(username):
    media_id = get_post_id(username)
    req_url = BASE_URL + 'media/' + media_id + '/comments/?access_token=%s' + ACCESS_TOKEN
    comment_info = requests.get(req_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print('Negative comment : ' + comment_text)
                    delete_url = BASE_URL + 'media/' + media_id + '/comments/' + comment_id + '/?access_token=' + \
                                 ACCESS_TOKEN
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print('Comment successfully deleted!\n')
                    else:
                        print('Unable to delete comment!')
                else:
                    print('Positive comment : ' + comment_text + '\n')
        else:
            print('There are no existing comments on the post!')
    else:
        print('Status code other than 200 received!')


# Defining the menu function of the instabot
def instabot():
    while True:
        print('\n')
        print('Hello and welcome to Instabot!!!!!!!!')
        print('You can perform the following functions....')
        print('1. Get your own details')
        print('2. Get details of another user by username')
        print('3. Get your own recent post')
        print('4. Get the recent post of a user by username')
        print('5. Like the recent post of a user')
        print('6. Comment on the recent post of a user')
        print('7. Delete negative comments from the recent pot of a user')
        print('8. Exit')

        choice = eval(input('Enter your choice : '))
        if choice == 1:
            self_info()

        elif choice == 2:
            name = input('Enter the username : ')
            get_user_info(name)

        elif choice == 3:
            get_own_post()

        elif choice == 4:
            name = input('Enter the username')
            get_user_post(name)

        elif choice == 5:
            name = input('Enter the username')
            like_post(name)

        elif choice == 6:
            name = input('Enter the username')
            post_a_comment(name)

        elif choice == 7:
            name = input('Enter the username')
            delete_negative_comment(name)

        elif choice == 8:
            exit()

        else:
            print('You did not enter a valid choice')


instabot()
