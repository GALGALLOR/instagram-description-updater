from flask import Flask
from datetime import datetime
from youtube_api import YouTubeDataAPI
import os
from dotenv import load_dotenv



app = Flask(__name__)

@app.route('/')
def homepage():
    load_dotenv()
    api_key = os.getenv('YT_DATA_API_KEY')
    yt = YouTubeDataAPI(api_key)
    return yt.search('alexandria ocasio-cortez')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)