from flask import Flask, request, send_file, jsonify
import youtube_dl
import os

app = Flask(__name__)

@app.route("/download", methods=["POST"])
def download_audio():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # Tìm file MP3 đã tải
        for file in os.listdir('.'):
            if file.endswith(".mp3"):
                return send_file(file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Dọn dẹp các file tải về sau khi tải xong
        for file in os.listdir('.'):
            if file.endswith(".mp3") or file.startswith("downloaded_video"):
                os.remove(file)

    return jsonify({"error": "Failed to download"}), 500

if __name__ == "__main__":
    app.run(debug=True)
