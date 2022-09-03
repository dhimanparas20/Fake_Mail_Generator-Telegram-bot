# Temp_Mail Bot 📨
> Saves your origional inbox from spam. 😎

So using this repo you can deploy your Telegram Bot that can generate unlimited emails and do alot more. Or you can just use [MINE](https://t.me/tempmailgen69_bot)

------

## Banner 🖼️
<p align="center">
<img src="https://github.com/dhimanparas20/python-telegram-Temp_Mail-bot/blob/main/mst.jpg" />

------

## Changelog

* Added button GUI <br />
* No need to type email everytime.
  
------
  
## Pre-requests 🧬
  
> [Create](https://signup.heroku.com/) a Heroku account and get its api Key from [settings](https://dashboard.heroku.com/account).
  
> Create a Telagram Bot using [BotFather](https://t.me/BotFather) and get its bot token. Also enable inline mod.
  
> Create a Mailsac [Account](https://mailsac.com/register) and get its api key.
  
> Basic knowledge about Git and Heroku.

------  
  
## Deploy on Heroku With Github Workflow 🗒️
  
> Fork this repo.
  
1. Go to Repository Settings -> Secrets

![Secrets](https://telegra.ph/file/9d6ed26f8981c2d2f226c.jpg)

2. Add the below Required Variables one by one by clicking New Repository Secret every time.

   - HEROKU_EMAIL: Heroku Account Email Id in which the above app will be deployed
   - HEROKU_API_KEY: Your Heroku API key, get it from [HERE](https://dashboard.heroku.com/account)
   - HEROKU_APP_NAME: Your Heroku app name, Name Must be unique
   - CONFIG_FILE_URL: Copy [This](https://raw.githubusercontent.com/dhimanparas20/Fake_Mail_Generator-Telegram-bot/main/config_sample.env) and create a new github [Gist](https://gist.github.com/) ,name it as config.env and paste it here. Fill the variables:<br />
      - MAILSAC_API_KEY: Mailsac api key you got
      - BOT_TOKEN: Telegram Bot token you got
      - HEROKU_APP_NAME: Your Heroku app name, Name Must be unique <br />
      Now save the gist and get its raw link. Remove the commit id from raw link. For more help visit [HERE](https://github.com/anasty17/mirror-leech-telegram-bot/tree/heroku)

3. After adding all the above Required Variables go to Github Actions tab in your repository.
   - Select Manually Deploy to Heroku workflow as shown below:

![Select Manual Deploy](https://telegra.ph/file/cff1c24de42c271b23239.jpg)

4. Choose `heroku` branch and click on Run workflow

![Run Workflow](https://telegra.ph/file/f44c7465d58f9f046328b.png)  
  
5. That's it, if no errors occured, the bot will be live/working in 2-3 minutes.
  
------  
  
## Deploy manually/locally using ngrok (Temperary Deploy) 🗒️
  
> If you want to deploy this bot on your machine follow this <br />
> you system should alredy have flask and ngrok pre installed. <br />

Linux:

> Clone this repo 
```sh
git clone  https://github.com/dhimanparas20/Fake_Mail_Generator-Telegram-bot.git && cd Fake_Mail*
```

> Start Ngrok Server
```sh
ngrok http 5000
```

> Open config.env and fill the variables accordingly but put HEROKU_APP_NAME as "forwarding"link provided after running above command.

> Open app.py and commentout lines 20,21,22 (Add #hash at the beginning).

> Open app.py and uncomment lines 25,26,27 (Remove #hash from the beginning).

> Run the app
```sh
python3 app.py
```
> Thats it. Enjoy
  
------    
  
## Trouble-shooting ☢️
  
> Type /ping in bot chat in telegram. If you get a response, congratulations the BOT is working.
  
> If not then check the Actions in git. See if the workflow completed sucessfully.

> If not then read the error (most probably you should change heroku app name in secrets") 
  
> Check Heroku logs for more details.
  
> You can contact me for Help and Support on my Telegram @ https://t.me/Ken_keneki_69
  
> If you want to change your bot token or mailsac api simple just edit your gist and jsut restart your heroku app.

------  

## Bot Commands 🦾
Save the following Bot commands in BotFather for your bot:
  
>help - learn how to use the bot <br />
>available - Check availability email address <br />
>count - Count total inbox mails <br />
>inbox - View most recent mail <br />
>purge - Empty the inbox <br />
>list - Sends last n(1-9) emails <br />
>index - Read Nth(1-9) mail  <br />
>ping - Gives 'Pong' as response  <br />

------  
  
## Notes ⚠️
Dont edit this script if you hav 0 knowledge about Coding. <br />
Dont be a gey by copying or importing this repo and calling it yours. <br />
Any changes for betterment are welcome,  <br />
If you liked the script or need any kind of help , ping me up  https://t.me/ken_kaneki_69 <br />
Im not responsible for any of your data losses , do it at your own will . <br />
