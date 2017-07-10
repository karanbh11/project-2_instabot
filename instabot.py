# Importing requests library to facilitate the access of data in our program from the internet
import requests
# Importing Textblob library to analyze and delete negative comments
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# Importing urllib3 library for downloading posts in python 3 program
import urllib3
# Importing tkinter and PIL to display image or post
import tkinter as tk
from PIL import ImageTk, Image
# Importing matplotlib library for plotting hash-tag(#) trends in form of pie-charts
import matplotlib.pyplot as plt

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


# Function to display image
def display(path):
    # This creates the main window of an application
    window = tk.Tk()
    window.title("Join")
    window.geometry("500x500")
    window.configure(background='grey')

    # Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
    img = ImageTk.PhotoImage(Image.open(path))

    # The Label widget is a standard Tkinter widget used to display a text or image on the screen.
    panel = tk.Label(window, image=img)

    # The Pack geometry manager packs widgets in rows or columns.
    panel.pack(side="bottom", fill="both", expand="yes")

    # Start the GUI
    window.mainloop()


# Defining the function to get our own recent post
def get_own_post():
    req_url = BASE_URL + 'users/self/media/recent/?access_token=' + ACCESS_TOKEN
    media_self = requests.get(req_url).json()

    if media_self['meta']['code'] == 200:
        if len(media_self['data']):
            rec_img = media_self['data'][0]['images']['standard_resolution']['url']
            urllib3.disable_warnings()
            conn = urllib3.PoolManager()
            response = conn.request('GET', rec_img)
            f = open('own_post.jpg', 'wb')
            f.write(response.data)
            f.close()
            print('Your post was downloaded')
            dis = input("Do you want to display the image.. Enter \'y\' for yes and \'n\' for no : ")
            if dis == 'y':
                print("do click the image window below to see after pressing y ")
                display('own_post.jpg')
            else:
                pass
            print('Media Id is : ', media_self['data'][0]['id'])
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
            rec_img = media_user['data'][0]['images']['standard_resolution']['url']
            urllib3.disable_warnings()
            conn = urllib3.PoolManager()
            response = conn.request('GET', rec_img)
            f = open('user_post.jpg', 'wb')
            f.write(response.data)
            f.close()
            print('Your post was downloaded')
            dis = input("Do you want to display the image.. Enter \'y\' for yes and \'n\' for no : ")
            if dis == 'y':
                print("do click the image window below to see after pressing y ")
                display('user_post.jpg')
            else:
                pass
            print('Media ID is : ', media_user['data'][0]['id'])
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


# Defining a function to get the list of comments on the recent post
def comment_list(username):
    post_id = get_post_id(username)
    req_url = BASE_URL + 'media/' + post_id + '/comments?access_token=' + ACCESS_TOKEN
    comments_here = requests.get(req_url).json()
    print('The comments on this post are : \n')
    if comments_here['meta']['code'] == 200:
        for i in range(len(comments_here['data'])):
            print(comments_here['data'][i]['from']['username'], end=' : ')
            print(comments_here['data'][i]['text'])
            print()
    else:
        print('Status code other than 200!!!')


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
    req_url = BASE_URL + 'media/' + media_id + '/comments/?access_token=' + ACCESS_TOKEN
    print(req_url)
    comment_info = requests.get(req_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            for i in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][i]['id']
                comment_text = comment_info['data'][i]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if blob.sentiment.p_neg > blob.sentiment.p_pos:
                    print('Negative comment : ' + comment_text)
                    delete_url = BASE_URL + 'media/' + media_id + '/comments/' + comment_id + '?access_token=' + \
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


count = [0, 0, 0, 0, 0]
name = ['', '', '', '', '']


# Defining a function to count tags by name and plot them
def tag_count_plot():
    tag_analysis()
    plot()


def tag_analysis():
    i = 0
    print('Maximum of five tags allowed...!!!')
    while True:
        tag = input('Enter the tag to be evaluated : ')
        name[i] = tag
        req_url = BASE_URL + 'tags/' + tag + '?access_token=' + ACCESS_TOKEN
        tag_info = requests.get(req_url).json()
        count[i] = tag_info['data']['media_count']
        print('Do you want to evaluate another tag')
        ans = input()
        i = i + 1
        if ans == 'n':
            break
        elif ans == 'y':
            continue
        else:
            exit(code='Can\'t you enter correct answer !! Now restart the application ')

        print(count)


def plot():
    labels = name
    sizes = count
    explode = (0.1, 0.1, 0.1, 0.1, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


# Defining the menu function of the instabot
def instabot():
    while True:
        print('\n')
        print('Hello and welcome to Instabot!!!!!!!!')
        print('Only self and users in the sandbox can be accessed...')
        print('Sandbox test user \n[eviledmpredator]')
        print('Whom do you want to use the application for ??? \nEnter \'self\'(For own) or username(For another '
              'user) or \'exit\' to exit : ')
        user = input()
        if user == 'self':
            while True:
                print('You can perform the following functions....')
                print('1. Get your own details')
                print('2. Get your own recent post')
                print('3. Get to the previous menu')
                choice = eval(input('Enter your choice : '))
                if choice == 1:
                    self_info()

                elif choice == 2:
                    get_own_post()

                elif choice == 3:
                    break

                else:
                    print('You did not enter a valid choice!')

        elif user == 'exit':
            exit(code='You closed the application')

        else:
            while True:
                print('User ID is : ', get_user_id(user))
                print('You can perform the following functions....')
                print('1. Get the details of the user')
                print('2. Get the recent post of the user')
                print('3. Like the recent post of a user')
                print('4. Get the list of comments on the recent post of the user')
                print('5. Comment on the recent post of a user')
                print('6. Delete negative comments from the recent post of a user')
                print('7. Plot the trends of entered hash-tags(#)')
                print('8. Get back to the previous menu')

                choice = eval(input('Enter your choice : '))

                if choice == 1:
                    get_user_info(user)

                elif choice == 2:
                    get_user_post(user)

                elif choice == 3:
                    like_post(user)

                elif choice == 4:
                    comment_list(user)

                elif choice == 5:
                    post_a_comment(user)

                elif choice == 6:
                    delete_negative_comment(user)

                elif choice == 7:
                    tag_count_plot()

                elif choice == 8:
                    break

                else:
                    print('You did not enter a valid choice')


instabot()
