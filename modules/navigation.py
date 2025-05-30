# modules/navigation.py
import math
from tkinter import messagebox
<<<<<<< HEAD
=======
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
>>>>>>> 9ac5d4e8940c67b7986b8385ebf392ed304f0a4a

def get_total_pages(df, items_per_page):
    """Tính tổng số trang dựa trên kích thước DataFrame và số item mỗi trang"""
    if df is None or df.empty:
        return 1
    return math.ceil(len(df) / items_per_page)

<<<<<<< HEAD
def handle_page_navigation(df_current, current_page, items_per_page, action_type):
    """Xử lý điều hướng trang và trả về trang mới"""
=======
def handle_page_navigation(df_current, current_page_num, items_per_pg, action_type):
    """Xử lý điều hướng trang với dữ liệu hiện tại."""
>>>>>>> 9ac5d4e8940c67b7986b8385ebf392ed304f0a4a
    if df_current is None or df_current.empty:
        return current_page
    
    total_pages = get_total_pages(df_current, items_per_page)
    
    if action_type == "first":
        return 1
    elif action_type == "prev":
        return max(1, current_page - 1)
    elif action_type == "next":
        return min(total_pages, current_page + 1)
    elif action_type == "last":
        return total_pages
    
    return current_page

<<<<<<< HEAD
def paginate_data(df, current_page, items_per_page):
    """Phân trang dữ liệu và trả về DataFrame cho trang hiện tại"""
    if df is None or df.empty:
        return df
    
    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    return df.iloc[start_idx:end_idx]

def navigate_page(action_type, tree, page_label, items_per_page, update_table_display, get_total_pages, handle_page_navigation):
    """Hàm điều hướng trang (legacy function - có thể bỏ nếu không dùng)"""
    # Hàm này có thể được thay thế bằng handle_page_navigation ở trên
    pass
=======
    print(f"Trang mới sau điều hướng: {current_page_num}")  # 🔥 Kiểm tra kết quả cuối cùng
    return current_page_num  # Trả về số trang mới
>>>>>>> 9ac5d4e8940c67b7986b8385ebf392ed304f0a4a
