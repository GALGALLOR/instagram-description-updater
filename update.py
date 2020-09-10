from flask import Flask
from datetime import datetime
import os
# from dotenv import load_dotenv
import requests
import json
from ftplib import FTP

# app = Flask(__name__)
# load_dotenv()
api_key = os.environ['YT_DATA_API_KEY']
channel_id = os.environ['CHANNEL_ID']
user = os.environ['USER']
passwd= os.environ['PASSWD']
ip_address = os.environ['IPADDRESS']
htaccess = ".htaccess"
latest_video_text = "latest-video"
latest_video_formatter = "   RedirectMatch 301 ^/{latest_video_text} {latest_video}\n"
# @app.route('/latest-video', methods=['GET'])
def getLatestVideo():
    url = f'https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&channelId={channel_id}&maxResults=10&key={api_key}'
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    all_videos = data.get('items', {})
    video_id = all_videos[0].get('id', {}).get('videoId')
    lastest_video_url = f'https://www.youtube.com/watch?v={video_id}'
    return lastest_video_url

# @app.route('/update', methods=['GET'])
def updateHtaccess():
    ftp = FTP(ip_address) 
    ftp.login(user=user, passwd=passwd)  
    latest_video = getLatestVideo()
    # save my existing htaccess file to disk.
    with open(htaccess, "wb") as file:
        ftp.retrbinary(f"RETR {htaccess}", file.write)
    # load all lines into memory
    with open(htaccess) as file:
        lines = file.readlines()
    # edit the file to reflect the new video format
    with open(htaccess, "w") as file:
        for line in lines:
            if latest_video_text in line:
                if latest_video not in line:
                    line = latest_video_formatter.format(latest_video_text=latest_video_text, latest_video=latest_video)
                else:
                    return f'SUCCESS latest video is already {latest_video}'
            file.write(line)
    response = ftp.storbinary(f'STOR {htaccess}', open(htaccess, 'rb'))
    if ("226" in response):
        return f"SUCCESS changing latest video to {latest_video}"
    return f"FAILURE: hmm what went wrong updating latest video to {latest_video} ....?"

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

