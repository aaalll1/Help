FROM python:3.10-buster

RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/
RUN pip3 install -U https://github.com/coletdjnz/yt-dlp-youtube-oauth2/archive/refs/heads/master.zip
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
RUN yt-dlp --username oauth2 --password '' -F https://www.youtube.com/watch?v=nVjsGKrE6E8 && echo "Authentication complete. Continuing build..."
CMD python3 -m YukkiMusic
