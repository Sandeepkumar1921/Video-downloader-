from flask import Flask, request, jsonify, render_template
import yt_dlp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # CORS ko enable kiya gaya hai

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('video_url')
    
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400  # Bad Request agar URL nahi diya hai

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save in 'downloads' folder
        'noplaylist': True,  # Don't download playlists
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'Video')
            return jsonify({'message': f'Video "{video_title}" downloaded successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Flask ko public IP pe run kareng