# modules/navigation.py
import math
from tkinter import messagebox

def get_total_pages(df, items_per_page):
    """Tính tổng số trang dựa trên kích thước DataFrame và số item mỗi trang"""
    if df is None or df.empty:
        return 1
    return math.ceil(len(df) / items_per_page)

def handle_page_navigation(df_current, current_page, items_per_page, action_type):
    """Xử lý điều hướng trang và trả về trang mới"""
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