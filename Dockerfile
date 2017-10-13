FROM python:3.6-alpine
LABEL maintainer="@ManuelLR <manuellr.git@gmail.com>"

WORKDIR /usr/src/bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./tmail-bot.py" ]
