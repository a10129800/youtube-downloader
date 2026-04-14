from flask import Flask, render_template, request
import yt_dlp

app = Flask(__name__)

# 這段就是你原本寫的下載邏輯
def download_video(url):
    ydl_opts = {
        'format': 'best',
        # 強制它下載到你的桌面，並取名為「new_test_video」
        'outtmpl': 'C:/Users/adobe/Desktop/new_test_video.%(ext)s', 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# 設定網頁首頁
@app.route('/')
def index():
    return render_template('index.html')

# 設定按下按鈕後的動作
@app.route('/download', methods=['POST'])
def start_download():
    video_url = request.form.get('url')
    if video_url:
        try:
            download_video(video_url)
            return "下載完成！請去桌面看有沒有 new_test_video。"
        except Exception as e:
            print(f"發生錯誤了：{e}")
            return f"下載失敗，原因：{e}"
    return "網址無效！"

if __name__ == '__main__':
    app.run(debug=False)
