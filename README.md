# Tmail-bot
Telegram bot that acts as an email client

# Use
You can use it like a regular program or run inside a docker container (recomended). But first we need to know some data.

## Bot variables
First of all, we need to know our `username` and the `bot_token`. The `username` could be configure in your Telegram app settings. To get the`bot_token` is necessary to speak with the [@BotFather](https://telegram.me/BotFather) and introduce the `/newbot` command. It will ask all necesary data and finally, it will give to you the `bot_token` also called `API Token`.

## Docker
We use [docker-compose](https://docs.docker.com/compose/overview/) so you need to install on your computer [Docker-CE](https://docs.docker.com/) and [Docker-compose](https://docs.docker.com/compose/install/). 


After install, you only need to edit the enviroments values in your computer's file [docker-compose.yml](./docker-compose.yml) replacing the data of the previous section.

Finally, we execute the next command and can start to talk with the bot:

```
docker-compose up -d
```

If we update the code, you only need to update it (`git pull`) and relaunch docker compose with the following command:

```
docker-compose up -d --build
```

## Without docker
