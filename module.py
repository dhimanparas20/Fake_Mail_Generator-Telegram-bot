from dotenv import load_dotenv
from os import path,system,environ
from requests import get as rget
import requests, json 
from time import sleep
import os

# Downloads the Config.env file
CONFIG_FILE_URL = environ.get('CONFIG_FILE_URL')
try:
    if len(CONFIG_FILE_URL) == 0:
        raise TypeError
    try:
        res = rget(CONFIG_FILE_URL)
        if res.status_code == 200:
            with open('config.env', 'wb+') as f:
                f.write(res.content)
        else:
            log_error(f"Failed to download config.env {res.status_code}")
    except Exception as e:
        log_error(f"CONFIG_FILE_URL: {e}")
except:
    pass       
  
# Loading Config Vars from Config.env file
load_dotenv('config.env', override=True)
def getConfig(name: str):
    return environ[name]
 
MAILSAC_API_KEY = ""    
MAILSAC_API_KEY = getConfig("MAILSAC_API_KEY")    

# Adding API headers
headers = {"Mailsac-Key": MAILSAC_API_KEY}    

 
# Returns total no of messages for a mail id  
def count(mail):
  req = requests.get(f'https://mailsac.com/api/addresses/{mail}/messages', headers=headers) # Fetch data using API
  jon = req.json() #convert data intoto JSON
  if req.status_code != 403 :
    count  = len(jon)
    return(count)  
  else:
    return(0)   
    
# To purge inbox
def purge(mail):
  req = requests.get(f'https://mailsac.com/api/addresses/{mail}/messages', headers=headers) # Fetch data using API
  jon = req.json() #convert data intoto JSON
  if req.status_code != 403 :
    count = len(jon)
    if count !=0 :
      for i in range(0,count):
        dell = requests.delete(f'https://mailsac.com/api/addresses/{mail}/messages/{jon[i]["_id"]}', headers=headers) #Deleted the mail.
        print(f"status code: {dell.status_code}")
        if dell.status_code == 200 :
                print(f"🗑 Delete sucess")
        else:
          print(f"Message Deletion failed, error code: {req.status_code}")  
      return(f"{mail}:\n👉 Purged {count} mails.\nThe inbox is EMPTY 🗑 now.")    
    else:
      return(f"💡Inbox for {mail} is alredy 🗑 empty. Nothing to purge.")   
  else: #IF the mail is private
    print(f"{mail}:\n👉 is Private you cant purge it.🤷‍♂️")        
    return(f"{mail}\n👉 is Private you cant purge it.🤷‍♂️")
                 
# Checks if the mail is private or not     
def chk_private(mail):
  req = requests.get(f'https://mailsac.com/api/addresses/{mail}/messages', headers=headers) # Fetch data using API
  jon = req.json() #convert data intoto JSON
  if req.status_code == 403 :
    return(f"Private, you cant use it😔")
  else:
    return(f"Available, You can use it😁")  
    
# sends Attachment only (BETA)
def attach(mail,i):
  req = requests.get(f'https://mailsac.com/api/addresses/{mail}/messages', headers=headers) # Fetch data using API
  jon = req.json() #convert data intoto JSON
  if len(jon[i]['attachments']) >= 1: # For Downloading the Attachment.
            ab =  jon[i]['attachments'][0]
            att = requests.get(f"https://mailsac.com/api/addresses/{mail}/messages/{jon[i]['_id']}/attachments/{ab}", headers=headers , allow_redirects=True) 
            ext = att.headers.get('content-type').partition('/')[2]
            download_name = "attachment."+ext  # Final combined Download name
            open(f'{download_name}', 'wb').write(att.content)
            print(f"Attachment file {download_name} Downloaded.")   
                               
# Parses the JSON
def parse_mail(mail,i):  
   req = requests.get(f'https://mailsac.com/api/addresses/{mail}/messages', headers=headers) # Fetch data using API
   jon = req.json() #convert data intoto JSON
   if req.status_code != 403 :
     priv = False  # the mail is not priave  
     if len(jon) != 0:
       print(f"processing message no {i+1}")
       msg = requests.get(f'https://mailsac.com/api/text/{mail}/{jon[i]["_id"]}', headers=headers) #Get message data from mail
       if len(jon[i]['attachments']) >= 1:  # Shows Attachment ID if exixts.
         aid =  jon[i]['attachments'][0]
       else:
         aid = "NULL"
       index = i+1  
       total_mails = len(jon)
       frm = jon[i]['from'][0]['name']
       frm_mail = jon[i]['from'][0]['address']
       date_time = jon[i]['received']
       id_code = jon[i]['_id']
       attachment_id = aid
       subject = jon[i]['subject']
       message = msg.text
       return jon,total_mails,frm,frm_mail,date_time,id_code,attachment_id,subject,index,priv,message
     else:
       index = "NULL"
       total_mails = "NULL"
       frm = "NULL"
       frm_mail = "NULL"
       date_time = "NULL"
       id_code = "NULL"
       attachment_id = "NULL"
       subject = "NULL"
       message = "NULL"
       return jon,total_mails,frm,frm_mail,date_time,id_code,attachment_id,subject,index,priv,message
   else: #IF the mail is private
     index = "NULL"
     priv = True
     total_mails = "NULL"
     frm = "NULL"
     frm_mail = "NULL"
     date_time = "NULL"
     id_code = "NULL"
     attachment_id = "NULL"
     subject = "NULL"
     message = "NULL"
     return jon,total_mails,frm,frm_mail,date_time,id_code,attachment_id,subject,index,priv,message         
    

 # latest mail  only
def send_mail(mail,indx):
  print(f"processing JSON📂 {indx}")
  jon,total_mails,frm,frm_mail,date_time,id_code,attachment_id,subject,index,priv,message = parse_mail(mail,indx)
  print("----------------------------------EMAIL JSON DATA----------------------------------")
  print(jon)
  print("-----------------------------------------------------------------------------------")
  if priv == False:
    print("JSON processed✅")
    if len(jon) != 0:
      return(
             f"Showing message N.o. {index} out of {total_mails} message/s"+
             f"\n\nFrom: {frm} <{frm_mail}>"+
             f'\nTo: {mail}'+
             f"\nDate & Time: {date_time}"+
             f"\nid code: {id_code}"+
             f"\nAttachment ID: {attachment_id}"+
             f"\n\nSubject: {subject:}"+
             f"\n\n📧{message}")
    else:
      return(f"☺️ Dear user, the inbox for {mail} is currenty empty, please wait or get some mails☺️")
  else:
    return(f"☺️ Dear user, the email {mail} is owned by another account.\nPlease try another Address☺️")
