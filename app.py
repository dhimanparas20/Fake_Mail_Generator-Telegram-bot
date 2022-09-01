from module import latest_mail,count,purge,pass_value,chk_private,attach,getConfig
from dotenv import load_dotenv
from os import system,environ
from flask import Response
from flask import request
from flask import Flask
from ping3 import ping
from time import sleep
import requests

BOT_TOKEN = None
HEROKU_APP_NAME = ""
BOT_TOKEN = getConfig("BOT_TOKEN")
HEROKU_APP_NAME = getConfig("HEROKU_APP_NAME")

system("clear")  
# Heroku Run, to configure Webhook
print("-----------------------Attaching Webhook---------------------------")
system (f"curl https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://{HEROKU_APP_NAME}.herokuapp.com/ ")
print("\n-----------------------------------------------------------------")

# Local Run. keep this commented untill deploying manually/locally
#print("-----------------------Attaching Webhook---------------------------")
#system(f"curl https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={HEROKU_APP_NAME}")
#print("\n-----------------------------------------------------------------")

sleep(2)
app = Flask(__name__)
# function to parse Bot data from JSON
def parse_message(message):
    print("📺 TG-JSON-->",message)
    try: 
      try:  # User has a username
        print(f"Length of username: {len(message['message']['chat']['username'])}")
        try: # user didnt edit his message
          chat_id = message['message']['chat']['id']
          fname = message['message']['chat']['first_name']
          uname = message['message']['chat']['username']
          txt = message['message']['text']
        except: # user edited his message
          chat_id = message['edited_message']['from']['id'] # for edited messages
          fname = message['edited_message']['chat']['first_name'] # for edited messages
          uname = message['edited_message']['chat']['username'] # for edited messages
          txt = message['edited_message']['text'] # for edited messages
      except: # User has no username
        try: # user didnt edit his message
          print("\nUSER HAS NO USERNAME SO ASSIGNED HIS NAME TO USERNAME VARIABLE :-) ")
          chat_id = message['message']['chat']['id']
          fname = message['message']['chat']['first_name']
          uname = fname
          txt = message['message']['text']    
        except:  # user edited his message
          print("\nUSER HAS NO USERNAME SO ASSIGNED HIS NAME TO USERNAME VARIABLE :-) ")
          chat_id = message['edited_message']['chat']['id']
          fname = message['edited_message']['chat']['first_name']
          uname = fname
          txt = message['edited_message']['text'] 
    except:
      try:  # User has a username
        chat_id = message['my_chat_member']['from']['id']
        fname = message['my_chat_member']['chat']['first_name'] 
        uname = message['my_chat_member']['chat']['username']
        txt = message['my_chat_member']['chat']['first_name']      
      except: # User has no username
        print("\nUSER HAS NO USERNAME SO ASSIGNED HIS NAME TO USERNAME VARIABLE :-) ")
        chat_id = message['my_chat_member']['from']['id']
        fname = message['my_chat_member']['chat']['first_name'] 
        uname = fname
        txt = message['my_chat_member']['chat']['first_name']     
    print("-------------------------------------------")
    print("💬chat_id-->", chat_id)
    print("first_name-->", fname)
    print("👥username->", uname)
    print("📖txt-->", txt)
    print("-------------------------------------------")
    return chat_id,txt,fname,uname
# function to send message to the user
def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text,
                }

    r = requests.post(url,json=payload)
    return r  
    
# function to send message with formatting options
def send_parse_message(chat_id, text, parse_mode):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
                }

    r = requests.post(url,json=payload)
    return r      
# sending a file
def send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
 
    payload = {
        'chat_id': chat_id,
        "document": "https://gofile.io/d/BhdcLB"
    }
 
    r = requests.post(url, json=payload)
 
    return r    
# function to remove extra spaces while extracting substrings
def remove(string):
    return string.replace(" ", "")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      msg = request.get_json()

      chat_id,txt,fname,uname = parse_message(msg)
      if txt == "/start":  # Display welcome text
        send_message(chat_id,f"👋Hello! @{uname} AKA 😊{fname}.\nPlease type /help to ℹ️learn how this bot works.🤔")
        send_message(chat_id,f"Or if you just want to see most recent mail 🤷‍♂️ then type /inbox <email@mailsac.com>.\ne.g. /inbox abc@mailsac.com")
      elif txt != None and txt == "/help": # Help
        send_message(chat_id,f"🔥GETTING STARTED:\n-->This bot generates instant inbox of an email address.\n-->First of all, come up with an email address with mailsac.com domain e.g. abc@mailsac.com . \
\n-->Check if the email is available by command /available abc@mailsac.com.\n-->If available continue else think of another address.\n\n🪧USAGE:\n1⃣ : To count the total no of mails inside \
inbox, use /count abc@mailsac.com.\n2⃣ : To see the most recent mail, type /inbox abc@mailsac.com.\n3⃣ : To check last n(1to9) number of email, use /list <1-9> <mail> \e.g. /list 3 abc@mailsac.com. \
\n4⃣ : To purge/delete complete inbox use /purge abc@mailsac.com.\n5⃣ : To see a specific mail remeber its index number (from /list) and use /index n(1-9) <mail> e.g./index 5 abc@mailsac.com  . \
\n6⃣ : use /repo to see bot repo.\n\n🤚LIMITATIONS:\n1⃣ : You can only use @mailsac.com as a domain.\n2⃣ : Max. index or list range is 9.")  
      elif txt != None and "@mailsac.com" in txt and "/inbox" in txt:  # shows most recent mail
        mail  = remove(txt[6:])
        send_message(chat_id,latest_mail(mail,indx=0))
      elif txt != None and "@mailsac.com" in txt and "/count" in txt: # counts total no of mail
        mail  = remove(txt[6:])
        send_message(chat_id,count(mail))
      elif txt != None and "@mailsac.com" in txt and "/list" in txt:    # shows last n mails
        mail  = remove(txt[7:])  # for the mail
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[5:]) #for the number of values
        rng = remove(txt[5:-(len(cutoff))]) 
        if rng.isdigit():
          intrng = int(rng)
          coun = pass_value(mail)
          print(f"no of recent mails to display: {intrng}")
          print(f"Total mails in the inbox: {coun}")
          if intrng <= coun:
            for i in range (0,intrng):
              send_message(chat_id,latest_mail(mail,i)) 
          else:
            send_message(chat_id,f"Total mails inbox = {coun} but you requested for {intrng}😕.\n please type number equal or less than {coun}.")      
        else:
          send_message(chat_id,f"The range of numbers is either not Given or invalid")      
      elif txt != None and "@mailsac.com" in txt and "/index" in txt:    # shows a specifix indexed mail
        mail  = remove(txt[8:])
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[6:])
        rng = remove(txt[6:-(len(cutoff))]) 
        if rng.isdigit():
          indx = int(rng)
          coun = pass_value(mail)
          print(f"indexed mail to display: {indx}")
          print(f"Total mails in the inbox: {coun}") 
          if indx <= coun:
            send_message(chat_id,latest_mail(mail,indx-1)) 
          else:
            send_message(chat_id,f"Total mails inbox = {coun} but you requested for {indx}😕.\n please type number equal or less than {coun}.")                     
        else:
          send_message(chat_id,f"The range of numbers is either not given or invalid")    
      elif txt != None and "@mailsac.com" in txt and "/purge" in txt:  # To the inbox  
        mail  = remove(txt[6:])  # for the mailaddress
        coun = pass_value(mail)  # total no of mails present
        print(coun)
        print(f"trimmed mail: {mail}")
        send_message(chat_id,purge(mail))        
      elif txt != None and "@mailsac.com" in txt and "/attachment" in txt: # Sends attachment as file   
        mail  = remove(txt[13:])  # for the mail
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[13:]) #for the number of values
        rng = remove(txt[11:-(len(cutoff))]) 
        indx = int(rng)
        coun = pass_value(mail)
        print(f"indexed attachment to display: {indx}")
        print(f"Total mails in the inbox: {coun}") 
        if indx <= coun:
          send_message(chat_id,attach(mail,indx-1)) 
        else:
          send_message(chat_id,f"Total mails inbox = {coun} but you requested for {indx}😕.\n please type number equal or less than {coun}.") 
      elif txt != None and "@mailsac.com" in txt and "/available" in txt: # check availability of an address
        mail  = remove(txt[10:])  # for the mail
        send_message(chat_id,chk_private(mail))      
      elif txt == "file":  #Sends a document
        send_document(chat_id)  
      elif txt == "/repo": 
        text = '[HERE](https://github.com/dhimanparas20/python-telegram-Temp_Mail-bot)'
        send_parse_message(chat_id,text,parse_mode='MarkdownV2') 
      elif txt != None and "/count" in txt:  #incomplete command
        send_message(chat_id,"🤦‍♂️Please add email address after the /count command.\n e.g. /count abc@mailsac.com")
      elif txt != None and "/inbox" in txt: #incomplete command
        send_message(chat_id,"🤦‍♂️Please add email address after the /inbox command.\n e.g. /inbox abc@mailsac.com") 
      elif txt != None and "/list" in txt:                 
        send_message(chat_id,"🤦‍♂️Please add number and email address after the /list command.\n e.g. /list abc@mailsac.com") 
      elif txt != None and "/available" in txt:  #incomplete command               
        send_message(chat_id,"🤦‍♂️Please add email address after the /purge command.\n e.g. /available abc@mailsac.com")
      elif txt != None and "/purge" in txt:   #incomplete command              
        send_message(chat_id,"🤦‍♂️Please add email address after the /purge command.\n e.g. /purge abc@mailsac.com")  
      elif txt != None and "/index" in txt:  #incomplete command               
        send_message(chat_id,"🤦‍♂️Please add index number and email address after /index command.\n e.g. /index 2 abc@mailsac.com")     
      elif txt == "/ping":
#        ab = ping('www.mailsac.com.com')
#        print(str(ab)[2:5])
        send_message(chat_id,f"Pong 🏓") 
      else: # invalid command
        send_message(chat_id,f'⚠️Error! Invalid Command 🙂') 

      return Response('ok', status=200)
    else:
        return "<h1>Welcome! To MST Production</h1>"

if __name__ == '__main__':
   app.run(debug=True)
