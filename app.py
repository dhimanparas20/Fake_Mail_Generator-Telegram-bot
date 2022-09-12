from module import send_mail,count,purge,chk_private,attach,getConfig
from dotenv import load_dotenv
from os import system,environ
from flask import Response
from flask import request
from flask import Flask,render_template
from ping3 import ping
from time import sleep
import requests

# Calling valies of Environment Variables
BOT_TOKEN = None
HEROKU_APP_NAME = ""
BOT_TOKEN = getConfig("BOT_TOKEN")
HEROKU_APP_NAME = getConfig("HEROKU_APP_NAME")

system("clear")  # Cause we like everything clean 

# Heroku Run, to configure Webhook
print("-----------------------Attaching HEROKU Webhook---------------------------")
system (f"curl https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url=https://{HEROKU_APP_NAME}.herokuapp.com/ ")
print("\n-----------------------------------------------------------------")

# Local Run. keep this commented untill deploying manually/locally
#print("-----------------------Attaching LOCAL Webhook---------------------------")
#system(f"curl https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={HEROKU_APP_NAME}")
#print("\n-----------------------------------------------------------------")
sleep(2)

app = Flask(__name__)
# function to parse Bot data from JSON.
def parse_message(message):
  try: # If user has a username
    if "message" in message.keys(): 
      chat_id = message['message']['from']['id']
      fname = message['message']['from']['first_name']
      uname = message['message']['from']['username']
      txt = message['message']['text']      
    elif "edited_message" in message.keys():
      chat_id = message['edited_message']['from']['id'] 
      fname = message['edited_message']['from']['first_name'] 
      uname = message['edited_message']['from']['username'] 
      txt = message['edited_message']['text']
    elif "callback_query" in message.keys():
      chat_id = message['callback_query']['from']['id']
      fname = message['callback_query']['from']['first_name'] 
      uname = message['callback_query']['from']['username'] 
      txt = message['callback_query']['data']  
    elif "my_chat_member" in message.keys():
      chat_id = message['my_chat_member']['from']['id']
      fname = message['my_chat_member']['from']['first_name'] 
      uname = message['my_chat_member']['from']['username']
      txt = message['my_chat_member']['from']['first_name']  
  except: # IF user has no username
    uname = " NoUsername"
    if "message" in message.keys(): 
      chat_id = message['message']['from']['id']
      fname = message['message']['from']['first_name']
      txt = message['message']['text']      
    elif "edited_message" in message.keys():
      chat_id = message['edited_message']['from']['id'] 
      fname = message['edited_message']['from']['first_name'] 
      txt = message['edited_message']['text']
    elif "callback_query" in message.keys():
      chat_id = message['callback_query']['from']['id']
      fname = message['callback_query']['from']['first_name'] 
      txt = message['callback_query']['data']  
    elif "my_chat_member" in message.keys():
      chat_id = message['my_chat_member']['from']['id']
      fname = message['my_chat_member']['from']['first_name'] 
      txt = message['my_chat_member']['from']['first_name'] 
  print("================================|  JSON  |==========================")    
  print("📺 TG-JSON-->",message)        
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
  
# sending a file/document (BETA)
def send_document(chat_id):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
 
    payload = {
        'chat_id': chat_id,
        "document": "https://gofile.io/d/BhdcLB"
    }
 
    r = requests.post(url, json=payload)
 
    return r    

# Buttton Function 1
def send_inlinebutton1(chat_id,welcome_text,repo,support):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': f"{welcome_text}",
        'reply_markup': {
            "inline_keyboard": [
                [{"text":"HELP","callback_data":"/help"}],
                [{"text": "Bot Repo", "url": f"{repo}"}],
                [{"text": "Support", "url": f"{support}"}]
            ]    
        }
    }
    r = requests.post(url, json=payload)
    return r        
                
# Buttton Function 2                    
def send_inlinebutton2(chat_id,mail,coun):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': f"▪️Current Mail👉 {mail}\n▪️Access👉 {chk_private(mail)}\n▪️Total No. of mails👉 {coun}",
        'reply_markup': {
            "inline_keyboard": [
                [{"text": "Read Latest Mail","callback_data": f"/inbox {mail}"},{"text": "\nPurge/Delete/Empty - INBOX","callback_data": f"/purge {mail}"}],
                [{"text": "Show last 5 mails","callback_data": f"/list 5 {mail}"},{"text": "Show last 9 mails","callback_data": f"/list 9 {mail}"}],
                [{"text": "Read a specific mail","callback_data": f"/read {mail}"},{"text": "See total number of mails","callback_data": f"/count {mail}"}],
                [{"text": "Help","callback_data": "/help"},{"text": "PinG","callback_data": "ping"}]
             ]    
        }
    }
    r = requests.post(url, json=payload)
    return r 
    
# Buttton Function 3
def send_inlinebutton3(chat_id,mail):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    payload = {
        'chat_id': chat_id,
        'text': f"▪️Enter the Index Number of mail you want to see",
        'reply_markup': {
            "inline_keyboard": [
                [{"text": "1","callback_data": f"/index 1 {mail}"},{"text": "2","callback_data": f"/index 2 {mail}"},{"text": "3","callback_data": f"/index 3 {mail}"}],
                [{"text": "4","callback_data": f"/index 4 {mail}"},{"text": "5","callback_data": f"/index 5 {mail}"},{"text": "6","callback_data": f"/index 6 {mail}"}],
                [{"text": "7","callback_data": f"/index 7 {mail}"},{"text": "8","callback_data": f"/index 8 {mail}"},{"text": "9","callback_data": f"/index 9 {mail}"}]
             ]    
        }
    }
    r = requests.post(url, json=payload)
    return r      
    
# function to remove extra spaces while extracting substrings
def remove(string):
    return string.replace(" ", "")  
     
# The Magical Kitchen
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      msg = request.get_json()
      chat_id,txt,fname,uname = parse_message(msg)
      
      if txt == "/start":  # Display welcome text
        welcome_text = f"👋Hello! {fname}.\n\n🔹First of all, come up with an email address with mailsac.com domain eg: abc@mailsac.com.\n🔹To start using that mail \
simply type: /use <address@mailsac.com>\neg: /use abc@mailsac.com.\n🔹Confirm access of mail and you are good to go👍."
        repo = "https://github.com/dhimanparas20/Fake_Mail_Generator-Telegram-bot"
        support = "https://t.me/mst_roms_X00T"
        send_inlinebutton1(chat_id,welcome_text,repo,support)
        
      elif txt != None and txt == "/help": # Help
        send_message(chat_id,f"🔥GETTING STARTED:\n-->This bot generates instant inbox of an email address.\n-->First of all, come up with an email address with mailsac.com domain \
e.g: abc@mailsac.com (we will be using this mail for further examples).\n\n🪧USAGE:\n--> Type: /use abc@mailsac.com. This will provide you some information and options regarding \
the Email you chose. Make sure the Access section says 'Available'. If not please try another email address and you are good to go👍.\n\nLIMITATIONS:\n🔹You can only see either \
last 5 or last 10 mails, or Read a specific mail.")
                
      elif txt != None and "@mailsac.com" in txt and "/use" in txt: #The main config button
        mail  = remove(txt[4:])  # Extraction of Email address.
        coun = count(mail) # Total number of Emails.
        send_inlinebutton2(chat_id,mail,coun) 
        
      elif txt != None and "@mailsac.com" in txt and "/read" in txt: # Displays the index buttons
        mail  = remove(txt[5:])
        coun = count(mail)
        send_inlinebutton3(chat_id,mail)
        
      elif txt != None and "@mailsac.com" in txt and "/inbox" in txt:  # shows most recent mail
        mail  = remove(txt[6:])
        send_message(chat_id,send_mail(mail,indx=0))
        
      elif txt != None and "@mailsac.com" in txt and "/count" in txt: # Shows total no of mails 
        mail  = remove(txt[6:])  
        send_message(chat_id,f"Total no of mails for {mail}: {count(mail)}")
      elif txt != None and "@mailsac.com" in txt and "/list" in txt:    # shows last n mails
        mail  = remove(txt[7:])  # for the mail
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[5:]) #for the number of values
        rng = remove(txt[5:-(len(cutoff))]) 
        if rng.isdigit():
          intrng = int(rng)
          coun = count(mail)
          print(f"no of recent mails to display: {intrng}")
          print(f"Total mails in the inbox: {coun}")
          if intrng <= coun:
            for i in range (0,intrng):
              send_message(chat_id,send_mail(mail,i)) 
          else:
            print(coun)
            send_message(chat_id,f"Total mails inbox = {coun} but you requested for {intrng}😕.\nPlease type number withing range")    
        else:
          send_message(chat_id,f"The range of numbers is either not Given or invalid")    
            
      elif txt != None and "@mailsac.com" in txt and "/index" in txt:    # shows a specific indexed mail
        mail  = remove(txt[8:])
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[6:])
        rng = remove(txt[6:-(len(cutoff))]) 
        if rng.isdigit():
          indx = int(rng)
          coun = count(mail)
          print(f"indexed mail to display: {indx}")
          print(f"Total mails in the inbox: {coun}") 
          if indx <= coun:
            send_message(chat_id,send_mail(mail,indx-1)) 
          else:
            send_message(chat_id,f"Total mails inbox = {coun} but you requested for {indx}😕.\nPlease type number withing range")
        else:
          send_message(chat_id,f"The range of numbers is either not given or invalid")  
            
      elif txt != None and "@mailsac.com" in txt and "/purge" in txt:  # To the inbox  
        mail  = remove(txt[6:])  # for the mailaddress
        coun = count(mail)  # total no of mails present
        print(coun)
        print(f"trimmed mail: {mail}")
        send_message(chat_id,purge(mail))        
        
      elif txt != None and "@mailsac.com" in txt and "/attachment" in txt: # Sends attachment as file  (BETA)
        mail  = remove(txt[13:])  # for the mail
        print(f"trimmed mail: {mail}")
        cutoff = remove(txt[13:]) #for the number of values
        rng = remove(txt[11:-(len(cutoff))]) 
        indx = int(rng)
        coun = count(mail)
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
           
      elif txt == "ping" or txt == "Ping":
#        ab = ping('www.mailsac.com.com')
#        print(str(ab)[2:5])
        send_message(chat_id,f"Pong 🏓") 

      else: # invalid command
        send_message(chat_id,f'⚠️Error! Invalid Command 🙂') 
      
      print()
      return Response('ok', status=200)
    else:
        return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)
