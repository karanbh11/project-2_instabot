# Importing requests library to facilitate the access of data in our program from the internet
import requests

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
    req_url = BASE_URL + 'users/' + user_id + '?access_token=' + ACCESS_TOKEN
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


get_user_info('prskntshrma')
