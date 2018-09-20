#!/usr/bin/python
import praw
import pdb
import re
import os
import time

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("memeeconomy")
inbox = reddit.inbox.comment_replies()
total = 1000
hours = 1.0
bot_string = ' | investments made by memebot pm me if things get out of control'

def MemeBot():
    while total >= 1000:
        get_balance()
        check_messages()
        invest()
        create_graph()

def create_graph():
    global total
    y_balance = []
    x_time = []
    
    y_balance.append(total)
    x_time.append(time.strftime("%H:%M"))

    if len(y_balance) > 10:
        del y_balance[0]
    if len(x_time) > 10:
        del x_time[0]

    for i in range(len(y_balance)):
        print(x_time[i] + " |" + ("*" * (y_balance[i] // 1000)) + '\n')

    
def delete_messages():
    x = 0
    for comment in reddit.redditor('Talbertross').comments.new(limit=None):
        if comment.body[0] == '!':
            x = x + 1
            comment.delete()
    print('Deleted ' + str(x) + ' comments.')

def get_balance():
    x = 0
    for submission in subreddit.rising():
        for toplevel in submission.comments:
            if x == 0:
                print("Requesting balance...")
                toplevel.reply("!balance" + bot_string)
                x = x + 1
                time.sleep(5)

def mark_read():
    for message in inbox:
        if message.author.name == 'MemeInvestor_bot':
            message.mark_read()

        
def check_messages():
    num = ''
    global total
    num = read_messages()
    total = int(num)

def read_messages():
    num = ''
    global total
    x = 0
    for message in inbox:
        if x == 0 and message.author.name == 'MemeInvestor_bot':
            message.mark_read()
            x = 1
            if 'Currently' in message.body:
                print(message.body)
                for letter in message.body:
                    if letter.isdigit():
                        num = num + letter
    if num == '':
        num = total
    return num

def invest():
    global total
    global hours
    invest_amt = total // 5
    if invest_amt < 100:
        invest_amt = 100
    invest_str = "!invest " + str(invest_amt) + bot_string
    submissions = []
    
    for submission in subreddit.rising():
        if submission.score >= 50:
            #print(submission.title)
            submissions.append(submission.id)
            x = 0
            submission.downvote()
            time.sleep(5)
            for toplevel in submission.comments:
                if x == 0:
                    toplevel.reply(invest_str)
                    x = x + 1
                    total = total - invest_amt
                    print("Investing " + str(invest_amt) + ", you have " + str(total) + " remaining.")
                    print('\n')
                    time.sleep(5)
            submission.upvote()
    memecount = len(submissions)
    
    if memecount == 0:
        print('No qualifying memes. Trying again in 1 hour.')
        print("Current time: " + time.strftime("%H:%M") + ".")
        print('\n')
        hours = 1
    elif memecount > 0 and memecount < 5:
        print('Invested in ' + str(memecount) + ' memes. Checking again in 2 hours.')
        print("Current time: " + time.strftime("%H:%M") + ".")
        print('\n')
        hours = 2
    elif memecount >= 5:
        print('Invested in ' + str(memecount) + ' memes. Checking again in 4 hours.')
        print("Current time: " + time.strftime("%H:%M") + ".")
        print('\n')
        hours = 4

    delete_messages()
    mark_read()
    time.sleep(hours * 3600)

MemeBot()
