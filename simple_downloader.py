import tkinter as tk
from tkinter import messagebox
import yt_dlp
import os

def download():
    url = entry.get()
    if not url:
        messagebox.showwarning("錯誤", "請輸入網址！")
        return
    
    status_label.config(text="下載中...請稍候", fg="blue")
    root.update() 
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status_label.config(text="✅ 下載完成！", fg="green")
        messagebox.showinfo("成功", "影片已下載到程式旁邊的資料夾！")
    except Exception as e:
        status_label.config(text="❌ 出錯了", fg="red")
        messagebox.showerror("錯誤", str(e))

# 建立小視窗介面
root = tk.Tk()
root.title("我的專屬下載器")
root.geometry("450x300")
root.configure(bg="#212121") 

# 1. 標籤
tk.Label(root, 
         text="YouTube 影片網址:", 
         font=("Microsoft JhengHei", 14, "bold"), 
         bg="#212121", 
         fg="#FFFFFF").pack(pady=20)

# 2. 輸入框
entry = tk.Entry(root, width=45, font=("Arial", 12))
entry.pack(pady=5)

# 3. 按鈕 (修正了 bold 後面的逗號)
tk.Button(root, 
          text="開始下載", 
          command=download, 
          bg="#007BFF", 
          fg="white", 
          font=("Microsoft JhengHei", 12, "bold"),
          width=20,
          height=2).pack(pady=25)

# 4. 狀態列
status_label = tk.Label(root, text="準備就緒", bg="#212121", fg="#AAAAAA")
status_label.pack()

root.mainloop()
