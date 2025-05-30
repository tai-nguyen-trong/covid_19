# modules/sort.py
import tkinter as tk
from modules.navigation import get_total_pages
from modules.updateTable import update_table_display

# Dictionary để lưu trạng thái sắp xếp từng cột
ascending_order = {}

def sort_column(col, tree, page_label, df_current, current_page, items_per_page):
    """Hàm sắp xếp cột tăng hoặc giảm dần khi nhấp vào tiêu đề"""
    global ascending_order
    
    if df_current is None or df_current.empty:
        return df_current, current_page
    
    # Kiểm tra trạng thái sắp xếp ban đầu
    if col not in ascending_order:
        ascending_order[col] = True
    
    # Đảo trạng thái sắp xếp mỗi lần nhấn
    ascending_order[col] = not ascending_order[col]
    
    # Sắp xếp dữ liệu hiện tại
    df_sorted = df_current.sort_values(by=col, ascending=ascending_order[col])
    
    # Cập nhật tiêu đề với biểu tượng đúng
    up_icon = "▲"
    down_icon = "▼"
    icon = up_icon if ascending_order[col] else down_icon
    tree.heading(col, text=f"{col} {icon}", command=lambda _col=col: sort_column(_col, tree, page_label, df_sorted, current_page, items_per_page))
    
    # Tính lại số trang sau khi sắp xếp
    total_pages = get_total_pages(df_sorted, items_per_page)
    current_page = min(current_page, total_pages)
    
    # Cập nhật lại bảng hiển thị theo dữ liệu đã lọc
    update_table_display(tree, page_label, df_sorted, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")
    
    return df_sorted, current_page

def setup_treeview(tree, df_current):
    """Thiết lập cấu hình ban đầu cho Treeview"""
    global ascending_order
    
    if df_current is None or df_current.empty:
        return
    
    headers = list(df_current.columns)
    tree["columns"] = headers
    tree["show"] = "headings"
    
    # Khởi tạo trạng thái sắp xếp của mỗi cột
    for col in headers:
        ascending_order[col] = False  # Đặt mặc định là giảm dần
        tree.heading(col, text=f"{col} ▼", command=lambda _col=col: sort_column(_col, tree, None, df_current, 1, 30))
        tree.column(col, width=120, anchor="center", stretch=tk.YES)

def reset_sort_order():
    """Reset trạng thái sắp xếp về mặc định"""
    global ascending_order
    ascending_order = {}