from flask import Flask, render_template, request, url_for, redirect, send_file, send_from_directory
import yt_dlp
from os import path

app = Flask(__name__, static_url_path='')

#app.config['SECRET_KEY'] = "DemoString"

def download(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)
    file = '' + video_title + '.mp3'
    filepath = path.join(path.dirname(__file__), file)

    ydl_opts = {
        'outtmpl': '' + video_title + '.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192', }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filepath
def get_thumb(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_thumb = info_dict.get('thumbnail', None)

    return video_thumb

def get_title(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None)

    return video_title


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        filepath = download(url)
        print(filepath)
        thumb = get_thumb(url)
        title = get_title(url)
        return render_template('see_video.html', filepath=filepath, thumb=thumb, title=title)
    return render_template("index.html")

@app.route("/download", methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        filepath = request.form.get('filepath')
        return send_file(filepath, as_attachment=True)
    return redirect(url_for('index'))

@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000)