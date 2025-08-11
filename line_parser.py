import csv
import os
import sys
from bs4 import BeautifulSoup

# --- 設定 ---
# 請將從LINE@網頁儲存的HTML檔案命名為這個名稱
HTML_FILENAME = "LINE Chat.html"
# 最終匯出的CSV檔案名稱
CSV_FILENAME = "line_group_members.csv"
# --- 設定結束 ---

def extract_line_members():
    """
    主要執行函數：讀取HTML，解析成員名單，並匯出成CSV。
    """
    # 判斷執行檔所在的目錄
    if getattr(sys, 'frozen', False):
        # 如果是打包後的 .exe
        script_dir = os.path.dirname(sys.executable)
    else:
        # 如果是直接執行 .py
        script_dir = os.path.dirname(os.path.abspath(__file__))

    html_file_path = os.path.join(script_dir, HTML_FILENAME)
    csv_file_path = os.path.join(script_dir, CSV_FILENAME)

    # 1. 檢查HTML檔案是否存在
    if not os.path.exists(html_file_path):
        print(f"錯誤：找不到 '{HTML_FILENAME}' 檔案。")
        print(f"請確認您已經將HTML檔案儲存為 '{HTML_FILENAME}'，")
        print("並且和這個執行檔放在同一個資料夾中。")
        input("\n請按 Enter 鍵結束...")
        return

    print(f"正在讀取 '{HTML_FILENAME}'...")

    try:
        # 2. 讀取並解析HTML
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'lxml')

        # === 程式碼修正處 ===
        # 舊的寫法是 soup.select('div.list-group-item h6')，範圍太廣
        # 新的寫法加入了 'div.modal'，明確指定只搜尋「成員列表」的彈出視窗
        member_tags = soup.select('div.modal div.list-group-item h6')
        # === 修正結束 ===


        if not member_tags:
            print("\n錯誤：在HTML檔案中找不到任何成員名單。")
            print("請確認您儲存的HTML頁面是正確的（需要看到成員列表彈出視窗）。")
            input("\n請按 Enter 鍵結束...")
            return

        # 3. 提取所有成員名稱
        member_names = [tag.get_text(strip=True) for tag in member_tags]
        
        print(f"\n成功找到 {len(member_names)} 位成員。")
        print(f"準備將名單匯出至 '{CSV_FILENAME}'...")

        # 4. 將名稱寫入CSV檔案
        with open(csv_file_path, 'w', newline='', encoding='utf-8-sig') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['成員名稱'])
            for name in member_names:
                writer.writerow([name])

        print("\n匯出完成！")
        print(f"檔案已成功儲存於：{csv_file_path}")

    except Exception as e:
        print(f"\n處理過程中發生未預期的錯誤：{e}")
    
    input("\n請按 Enter 鍵結束...")

if __name__ == "__main__":
    extract_line_members()