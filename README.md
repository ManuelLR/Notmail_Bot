# Notmail Bot
> Telegram bot that acts as an email client.

**V.0.1.0**

# Usage Preview
_Work in progress_

# Features

- Auto check email account and notify news.
- Friendly interface.
- Multiple email accounts.
- Compatible with IMAP protocol. (More in the future).
- Read email on Telegram, mark as read/unread, archive/delete and much more.

# Basic configuration
First of all, we need to know our `username` and the `bot_token`. The `username` could be configure in your Telegram app settings (also known as `alias`). To get the`bot_token` is necessary to speak with the [@BotFather](https://telegram.me/BotFather) and introduce the `/newbot` command. It will ask all necesary data and finally, it will give to you the `bot_token` also called `API Token`.

# Launch
We can launch in several ways:
- [Docker Compose](./README.md#docker-compose) **(recomended)**
- [Docker](./README.md#docker)
- [Python](./README.md#python)

### Docker Compose
To use [docker-compose](https://docs.docker.com/compose/overview/) you need to install on your computer [Docker-CE](https://docs.docker.com/) and [Docker-compose](https://docs.docker.com/compose/install/). 

Before running it you need to enter the variables in the new file called `.env`.

```
cp .example.env .env
nano .env
```

Finally, we execute the next command and can start to talk with the bot:

```
docker-compose up -d
```

If we update the code, you only need to update it (`git pull`) and relaunch docker compose with the following command:

```
git pull
docker-compose up -d --build
```

### Docker

```bash
sudo docker build -t notmail_bot .
sudo docker run -d --name Notmail_bot \
    --restart always \
    --env-file .env \
    manuellr/notmail_bot
```


### Python
```bash
pip install -r requirements.txt
python notmail_bot.py --config_path my-config/my_config.ini
```


# License
- The main code is licensed under [GPLv3](./LICENSE)
- The logo of Notmail is licensed under [Free Art License v1.3](./img/notmailbotLogoLicense.txt)

You can consult the contributors in the [AUTHORS file](./AUTHORS) or see the contributors of a specific file executing the next script:
```bash
git blame -C -C -M -- FILE_TO_CONSULT | \
    sed -e 's/[^(]*(\([^0-9]*\).*/\1/' -e 's/[\t ]*$//' | \
    sort | uniq -c | sort -nr
```
