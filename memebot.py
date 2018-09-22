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
y_balance = []
x_time = []
bot_string = ' | investments made by memebot pm me if things get out of control'

def MemeBot():
    get_balance()
    invest()

def create_graph():
    global total
    global y_balance
    global x_time
    
    y_balance.append(total)
    x_time.append(time.strftime("%H:%M"))

    if len(y_balance) > 10:
        del y_balance[0]
    if len(x_time) > 10:
        del x_time[0]

    for i in range(len(y_balance)):
        print(x_time[i] + " |" + ("*" * (y_balance[i] // 1000)))

    
def delete_messages():
    x = 0
    for comment in reddit.redditor('Talbertross').comments.new(limit=20):
        if comment.body[0] == '!':
            x = x + 1
            comment.delete()
    print('Deleted ' + str(x) + ' comments.')

def get_balance():
    x = 0
    for submission in subreddit.rising():
        for toplevel in submission.comments:
            if x == 0:
                x = 1
                print("Requesting balance...")
                replyid = toplevel.reply("!balance" + bot_string)
                replyid.refresh()
                time.sleep(5)
                
    read_balance_reply(replyid, 0)
    

def read_balance_reply(replyid, x):
    global total
    num = ''
    for reply in replyid.replies.list():
        print("Reading balance.")
        for letter in reply.body:
            if letter.isdigit():
                num = num + letter
    
    if num != '':
        print('Current total: ' + num + ' Memecoins')
        total = int(num)
    elif num == '' and x < 5:
        x = x + 1
        replyid.refresh()
        time.sleep(1)
        read_balance_reply(replyid, x)
    elif num == '' and x >= 5:
        print("Error retrieving balance. Exiting.")
        num = 0

def mark_read():
    for message in inbox:
        if message.author.name == 'MemeInvestor_bot':
            message.mark_read()

def clear_screen():
    os.system('cls')

def calculate_floor():
    current_time = int(time.strftime("%H"))
    if current_time > 21 or current_time <= 6:
        return 80
    else:
        return 50

def invest():
    global total
    invest_amt = total // 5
    if invest_amt < 100:
        invest_amt = 100
    invest_str = "!invest " + str(invest_amt) + bot_string
    submissions = []
    invest_floor = calculate_floor()
    
    for submission in subreddit.rising():
        if submission.score >= invest_floor:
            print(submission.title)
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
        hours = 1
    elif memecount > 0 and memecount < 5:
        print('Invested in ' + str(memecount) + ' meme(s). Checking again in 1 hour.')
        print("Current time: " + time.strftime("%H:%M") + ".")
        hours = 1
    elif memecount >= 5:
        print('Invested in ' + str(memecount) + ' memes. Checking again in 4 hours.')
        print("Current time: " + time.strftime("%H:%M") + ".")
        hours = 4

    delete_messages()
    mark_read()
    create_graph()
    time.sleep(hours * 3600)

while total >= 1000:
    MemeBot()
    clear_screen()

delete_messages()


print("Temporarily bankrupt. Halting investments.")
