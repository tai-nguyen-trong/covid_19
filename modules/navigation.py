import math
from tkinter import messagebox
import pandas as pd
from modules import updateTable

# Điều hướng phân trang
df_current = None  # 🔥 Đảm bảo biến toàn cục chứa dữ liệu hiện tại
current_page = 1  # 🔥 Đặt giá trị trang mặc định
items_per_page = 30

def paginate_data(df, page_number, items_per_page):
    """Phân trang dữ liệu."""
    if df is None or df.empty:
        return pd.DataFrame() # Trả về DataFrame rỗng nếu không có dữ liệu

    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return df.iloc[start_index:end_index]

def get_total_pages(df, items_per_page):
    """Tính tổng số trang dựa trên DataFrame và số mục trên mỗi trang."""
    if df is None or df.empty:
        return 1 # Trả về 1 trang nếu không có dữ liệu
    total_items = len(df)
    return math.ceil(total_items / items_per_page)

def handle_page_navigation(df_current, current_page_num, items_per_pg, action_type):
    """Xử lý điều hướng trang với dữ liệu hiện tại."""
    if df_current is None or df_current.empty:
        print("Dữ liệu rỗng, không thể điều hướng!")  # 🔥 Kiểm tra nếu dữ liệu trống
        return current_page_num

    total_pages = get_total_pages(df_current, items_per_pg)  # Lấy số trang từ dữ liệu hiện tại
    print(f"Tổng số trang: {total_pages}, Trang hiện tại: {current_page_num}")  # 🔥 Kiểm tra trang trước khi điều hướng

    if action_type == "next":
        if current_page_num < total_pages:
            current_page_num += 1
        else:
            messagebox.showinfo("Thông báo", "Bạn đang ở trang cuối cùng!")
    elif action_type == "prev":
        if current_page_num > 1:
            current_page_num -= 1
        else:
            messagebox.showinfo("Thông báo", "Bạn đang ở trang đầu tiên!")
    elif action_type == "first":
        current_page_num = 1
    elif action_type == "last":
        current_page_num = total_pages

    print(f"Trang mới sau điều hướng: {current_page_num}")  # 🔥 Kiểm tra kết quả cuối cùng
    return current_page_num  # Trả về số trang mới
