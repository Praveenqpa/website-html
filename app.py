from flask import Flask, render_template_string, request, redirect
import yt_dlp

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Termux Insta Downloader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #121212; color: #fff; padding: 30px 15px; }
        .container { max-width: 500px; margin: 0 auto; background: #1e1e1e; padding: 25px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        h1 { color: #e1306c; margin-bottom: 20px; }
        input[type="text"] { width: 90%; padding: 12px; border: 2px solid #333; border-radius: 6px; background: #2a2a2a; color: #fff; font-size: 16px; margin-bottom: 15px; }
        input[type="text"]:focus { border-color: #e1306c; outline: none; }
        button { width: 95%; padding: 12px; font-size: 16px; border: none; background: #e1306c; color: white; border-radius: 6px; font-weight: bold; cursor: pointer; }
        button:active { background: #b82354; }
        .footer { margin-top: 30px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Insta Video Grabber</h1>
        <p>Paste your Instagram Reel or Post link below:</p>
        <form action="/download" method="post">
            <input type="text" name="url" placeholder="https://www.instagram.com/reel/..." required>
            <button type="submit">Get Video Link</button>
        </form>
    </div>
    <p class="footer">Powered by Termux & yt-dlp</p>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    # Advanced bypass configuration options
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        # This masks the Python script as a standard desktop browser
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            
            if video_url:
                return redirect(video_url)
            else:
                return "<h3>Could not extract video URL.</h3><a href='/'>Try again</a>"
    except Exception as e:
        return f"<h3>Instagram Blocked the request. Error: {str(e)}</h3><a href='/'>Try again</a>"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
