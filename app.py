from flask import Flask,render_template
from dotenv import load_dotenv
from os import system,environ
from module import weather,getConfig
from flask import Response
from flask import request
from time import sleep
import requests

# Calling values of Environment Variables
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
      chat_id = message['message']['chat']['id']
      fname = message['message']['chat']['first_name']
      uname = message['message']['chat']['username']
      txt = message['message']['text']      
    elif "edited_message" in message.keys():
      chat_id = message['edited_message']['chat']['id'] 
      fname = message['edited_message']['from']['first_name'] 
      uname = message['edited_message']['from']['username'] 
      txt = message['edited_message']['text']
    elif "callback_query" in message.keys():
      chat_id = message['callback_query']['chat']['id']
      fname = message['callback_query']['from']['first_name'] 
      uname = message['callback_query']['from']['username'] 
      txt = message['callback_query']['data']  
    elif "my_chat_member" in message.keys():
      chat_id = message['my_chat_member']['chat']['id']
      fname = message['my_chat_member']['from']['first_name'] 
      uname = message['my_chat_member']['from']['username']
      txt = message['my_chat_member']['from']['first_name']  
  except: # IF user has no username
    uname = " NoUsername"
    if "message" in message.keys(): 
      chat_id = message['message']['chat']['id']
      fname = message['message']['from']['first_name']
      txt = message['message']['text']
    elif "edited_message" in message.keys():
      chat_id = message['edited_message']['chat']['id'] 
      fname = message['edited_message']['from']['first_name'] 
      txt = message['edited_message']['text']
    elif "callback_query" in message.keys():
      chat_id = message['callback_query']['chat']['id']
      fname = message['callback_query']['from']['first_name'] 
      txt = message['callback_query']['data']  
    elif "my_chat_member" in message.keys():
      chat_id = message['my_chat_member']['chat']['id']
      fname = message['my_chat_member']['from']['first_name'] 
      txt = message['my_chat_member']['from']['first_name']    
  print("================================|  JSON  |==========================")    
  print("📺 TG-JSON-->",message)        
  print("-------------------------------------------")
  print("💬chat_id-->", chat_id)
  print("first_name-->", fname)
  print("👥username->", uname)
  print("📖txt-->", txt)
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

# Buttton Function
def send_inlinebutton(chat_id,welcome_text,repo,support):
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
        welcome_text = f"👋Hello! {fname}.\n🔹Press Help Button For for details."
        support = "https://t.me/mst_roms_X00T"
        repo = "https://github.com/dhimanparas20/telegram-weather-bot "
        send_inlinebutton(chat_id,welcome_text,repo,support)
        
      elif txt != None and txt == "/help": # Help
        send_message(chat_id,f"Simply type /use followed by city name to get weather details.")
                
      elif txt != None and "/city" in txt : 
        city  = remove(txt[5:])
        send_message(chat_id,weather(city))

      else: # invalid command
        send_message(chat_id,"") 
        
      return Response('ok', status=200)
    
    else:
        return "<h1> HEllo </h1>"

if __name__ == '__main__':
   app.run(debug=True)
