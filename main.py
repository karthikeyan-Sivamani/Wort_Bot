#!/usr/bin/python3

import requests as req
from bs4 import BeautifulSoup as bs
import tweepy
import random
import os
import dropbox
import boto
import boto.s3.connection
import boto3

# Dropbox token
#dbx = dropbox.Dropbox('***************')

# Twitter API credentials
consumer_key = "******************"
consumer_secret = "****************************"
access_key = "***********************************"
access_secret = "***************************"

#S3 Bucket:
access_key_s3='******************'
secret_key='****************************'

conn = boto.s3.connect_to_region('eu-central-1',
        aws_access_key_id = access_key_s3,
        aws_secret_access_key = secret_key
        )


for bucket in conn.get_all_buckets():
        print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        ))



def dropbox_download():
    '''
  Method downloads the text file from dropbox
  and converts the contents from bytes to str
  '''
    conn = boto.s3.connect_to_region('eu-central-1',
        aws_access_key_id = access_key_s3,
        aws_secret_access_key = secret_key
        )


    for bucket in conn.get_all_buckets():
         print ("{name}\t{created}".format(
                name = bucket.name,
                created = bucket.creation_date,
        ))
    local_file_name = '/tmp/TEST.txt'
    s3 = boto3.client('s3')
    s3.download_file('karthiktests3', 'TEST.txt', local_file_name)

#s3.upload_file(local_file_name,'karthiktests3', 'TEST.txt')
    file = open(local_file_name,mode='r')

# read all lines at once
    file_content = file.read()
    print (file_content)

# close the file
    file.close()

#file_content=(file_content, 'utf-8', 'ignore')
    dropbox_download.file_con = (str(file_content))
    #print(dropbox_download.file_con)
    #print(type(dropbox_download.file_con))

# Converts the string into a list
    dropbox_download.word_list = list(dropbox_download.file_con.split(','))
    print (dropbox_download.word_list)

    #print(dbx.files_download('/word.txt'))
    #md, response = dbx.files_download('/word.txt')
    #file_contents = response.content
    #print(type(file_contents))
    #print(file_contents)
    #file_content=(file_contents, 'utf-8', 'ignore')
    #dropbox_download.file_con = (str(file_content))
    #print(dropbox_download.file_con)
    #print(type(dropbox_download.file_con))
    # Converts the string into a list
    #dropbox_download.word_list = list(dropbox_download.file_con.split(','))


# To Get the News page sentence from Google news
url = 'https://news.google.com/?edchanged=1&hl=de&gl=DE&ceid=DE:de'
r = req.get(url)
soup = bs(r.text, 'html.parser')
a = []
# Scraps the news from URL
for i in soup.find_all('a'):
    a.append(i.get_text())
a = list(filter(None, a))  # removes the Null values from the list
#print (a)


def file_write():
    '''
    Convert the string to bytes and then upload the updated file to dropbox
    '''

    #dropbox_download.file_con = dropbox_download.file_con.encode('utf-8')

    #res = dbx.files_upload(
     #   dropbox_download.file_con, '/word.txt', dropbox.files.WriteMode.overwrite,
     #   mute=True)
    s3 = boto3.client('s3')
    local_file_name = '/tmp/TEST.txt'
    overwrite = open(local_file_name,'w')
    overwrite.write(dropbox_download.file_con)
    overwrite.close()
    s3.upload_file(local_file_name,'karthiktests3', 'TEST.txt')

def dict_verb(search_word, a, w):
    '''
    Gets the meaning of the German Word from online dictionary
    '''
    url = 'https://dict.leo.org/german-english/' + search_word
    encode_line = url.encode('utf8').strip()
    u = encode_line.decode('utf8').strip()
    r = req.get(u)
    soup = bs(r.text, 'html.parser')

    mesg = []
    mesg.append(search_word)
    mesg.append(w)

    try:
        m = soup.find(attrs={'data-dz-ui': 'dictentry'})
        mesg.append(m.get_text())

        if search_word[0].isupper():
            if 'pl.' in m.get_text():
                status(mesg)
            else:
                rand(a)
        elif m.get_text() is not None:
            status(mesg)
        else:
            rand(a)
    except TypeError:
        rand(a)
    except AttributeError:
        rand(a)


def rand(a):
    '''
    Selects a random word and check few criterias.
    Appends the random word  to dropbbox file so that words are not repeated later
    '''

    w = random.choice(a)
    if len(w) > 40:
        word = random.choice(w.split(' '))
        #print(word)
        if len(word) <= 4:
            rand(a)
        elif word in dropbox_download.word_list:
            rand(a)
        else:
            print("Drp")
            if word[0].isupper():
                dict_verb(word, a, w)
                dropbox_download.file_con = dropbox_download.file_con + ',' + word

            else:
                dict_verb(word, a, w)
                dropbox_download.file_con = dropbox_download.file_con + ',' + word

    else:
        rand(a)


def downloadimages(query):

    #print (query)
    URL="https://unsplash.com/s/photos/"+query
    print (URL)
    page =  req.get(URL)
    soup = bs(page.content, 'html.parser')

    #print (soup)

    u = soup.find('div', class_='_1tO5-')
    print (u)
    src=(u.img['src'])
    print (src)

    img_data = req.get(src).content
    with open('/tmp/image_name.jpg', 'wb') as handler:
        handler.write(img_data)
    print ('exiting downlaodimages')


# Function to post tweets
def post_tweet(post):
    # Authorization to consumer key and consumer secret

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Downloads the image based on the URL extracted from method downloadimages()
    #filename = '/tmp/image_name.jpg'
    '''
    request = req.get(image_link[2:-2], stream=True)
    if request.status_code == 200:
        with open('/tmp/image_name.jpg', 'wb') as image:
            for chunk in request:
                a = image.write(chunk)

    '''
    # Calling api and posting a tweet using the image and staus
    api = tweepy.API(auth)

    api.update_with_media('/tmp/image_name.jpg', status=post)
    os.remove('/tmp/image_name.jpg')


def status(mesg):
    '''
    Creates the list  'post' to hold the information obtained from online Dict.
    '''
    msg = mesg
    post = []
    post.append('German Word : ' + msg[0])
    post.append('Meaning : ' + msg[2])
    post.append('Word Usage : ' + msg[1])
    post.append("#learngerman #DeutschLernen #Deutsch #German")
    '''
    Gets the english meaning of selected German word to search for suitable image
    '''
    print (post)
    print('I am here')
    eng_word = msg[2].replace(u'\xa0', u' ')
    eng_word = eng_word.lstrip()
    eng_word = eng_word.split('  ')
    print(eng_word)
    if 'sth' in eng_word[0]:
        e_word = eng_word[0].split('sth')
    elif '[' in eng_word[0]:
        e_word = eng_word[0].split('[')
    else:
        e_word = eng_word[0]
    print(e_word)
    downloadimages(e_word)

    # checking if the word got a matcing picture, if not call the main function again
    '''
    url_check = downloadimages.image_url
    print ("checking the URL")
    print (url_check)

    res = ",".join(("{}=:={}".format(*i) for i in url_check[0].items()))
    split = (res.split('=:='))
    image_link = split[1]
    print (image_link)
    if '[]' in image_link:
        print ("no image link")
        rand(a)
    else:
        print(post)

    '''
    '''
    Creates a string to pass the Tweet to post_tweet() method
    '''
    lines_seen = set()
    tweet = ''
    for line in post:
        if line not in lines_seen:
            tweet += '\n'
            encode_line = line.encode('utf8').strip()
            tweet += encode_line.decode('utf8').strip()

        lines_seen.add(line)
    tweet += '\n'
    print (tweet)
    # if image found call tweepy fn to tweet
    post_tweet(tweet)

def handler(event=None, context=None):
    dropbox_download()
    rand(a)
    file_write()
