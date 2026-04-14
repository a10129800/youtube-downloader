import tkinter as tk
from tkinter import messagebox, ttk
import yt_dlp
import os

# 儲存畫質對應的 format_id
video_formats = {}

def fetch_resolutions():
    url = entry.get()
    if not url:
        messagebox.showwarning("錯誤", "請先輸入網址再獲取畫質！")
        return
    
    status_label.config(text="正在獲取畫質清單...", fg="orange")
    root.update()
    
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # 清空舊資料
            video_formats.clear()
            res_list = []
            
            for f in formats:
                # 只要有影片軌 (vcodec) 就抓出來，不管它有沒有聲音
                if f.get('vcodec') != 'none':
                    res = f.get('resolution')
                    if res and res not in video_formats:
                        # 取得高度 (例如 1080) 來判斷名稱
                        try:
                            height = int(res.split('x')[1])
                        except:
                            height = 0
                        
                        # 定義標籤
                        label = ""
                        if height >= 2160: label = " (4K)"
                        elif height >= 1440: label = " (2K)"
                        elif height >= 1080: label = " (1080P)"
                        elif height >= 720: label = " (720P)"
                        elif height >= 480: label = " (480P)"
                        
                        display_name = f"{res}{label}"
                        # 2. 【關鍵修正】檢查這個名稱是否已經加過了
                        if display_name not in res_list:
                            res_list.append(display_name)
                            # 儲存這個解析度對應的最後一個 format_id (通常是畫質較好的)
                            video_formats[display_name] = f.get('format_id')

            # 排序（確保 4K 在最上面）
            res_list.sort(key=lambda x: int(x.split('x')[1].split(' ')[0]) if 'x' in x else 0, reverse=True)
            res_combo['values'] = res_list
            
            # 更新下拉選單
            res_combo['values'] = res_list
            if res_list:
                res_combo.current(0)
                status_label.config(text="✅ 已獲取畫質，請選擇後下載", fg="green")
            else:
                status_label.config(text="❌ 找不到可用畫質", fg="red")
                
    except Exception as e:
        messagebox.showerror("錯誤", f"獲取失敗: {e}")

def download():
    url = entry.get()
    selected_res = res_combo.get()
    
    if not url or not selected_res:
        messagebox.showwarning("錯誤", "請選擇畫質！")
        return
    
    format_id = video_formats.get(selected_res)
    status_label.config(text=f"🚀 正在下載並合併 {selected_res}...", fg="blue")
    root.update()
    
    try:
        ydl_opts = {
            # 關鍵修改：format_id 是你選的影像，加上最好的聲音
            'format': f'{format_id}+bestaudio/best', 
            'outtmpl': '%(title)s.%(ext)s',
            # 告訴程式 ffmpeg 在哪裡（如果你放在程式旁邊，就寫 './ffmpeg.exe'）
            'ffmpeg_location': './ffmpeg.exe', 
            'merge_output_format': 'mp4', # 合併成大家都能看的 mp4
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        status_label.config(text="✅ 高畫質合併完成！", fg="green")
        messagebox.showinfo("成功", f"已成功下載 {selected_res} 影音合一檔案！")
    except Exception as e:
        status_label.config(text="❌ 下載或合併出錯", fg="red")
        messagebox.showerror("錯誤", str(e))

# 介面設定
root = tk.Tk()
root.title("進階版下載器")
root.geometry("450x450")
root.configure(bg="#212121")

# UI 元件
tk.Label(root, text="YouTube 影片網址:", font=("Arial", 12, "bold"), bg="#212121", fg="white").pack(pady=10)
entry = tk.Entry(root, width=45)
entry.pack(pady=5)

# 新增：獲取畫質按鈕
tk.Button(root, text="1. 解析網址獲取畫質", command=fetch_resolutions, bg="#6c757d", fg="white").pack(pady=10)

tk.Label(root, text="選擇解析度:", font=("Arial", 10), bg="#212121", fg="white").pack(pady=5)
res_combo = ttk.Combobox(root, width=40, state="readonly")
res_combo.pack(pady=5)

# 下載按鈕
tk.Button(root, text="2. 開始下載", command=download, bg="#007BFF", fg="white", font=("Arial", 12, "bold"), width=20).pack(pady=30)

status_label = tk.Label(root, text="準備就緒", bg="#212121", fg="#AAAAAA")
status_label.pack()

root.mainloop()
