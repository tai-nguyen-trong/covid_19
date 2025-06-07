# modules/search.py
import pandas as pd
from tkinter import messagebox
from .navigation import get_total_pages
from .updateTable import update_table_display

def handle_search_data(keyword, df_original, df_current, current_page, items_per_page, tree, page_label):
    """Hàm tìm kiếm dữ liệu"""
    if not keyword or df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Dữ liệu gốc không hợp lệ hoặc từ khóa tìm kiếm trống!")
        return df_current, current_page

    keyword = keyword.lower()

    # Lọc dữ liệu
    df_filtered = df_original[df_original.astype(str).apply(
        lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]

    if df_filtered.empty:
        messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp!")

        # Khôi phục dữ liệu gốc để tránh lỗi hiển thị
        df_current = df_original.copy()
        current_page = 1

        total_pages = get_total_pages(df_current, items_per_page)

        update_table_display(tree, page_label, df_current, current_page, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages}")
        return df_current, current_page

    # Cập nhật dữ liệu tìm kiếm
    df_current = df_filtered
    current_page = 1
    total_pages_filtered = get_total_pages(df_current, items_per_page)

    # Hiển thị kết quả tìm kiếm với số trang mới
    update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages_filtered}")

    return df_current, current_page

def handle_reset_search(df_original, current_page, items_per_page, tree, page_label, search_entry):
    """Hàm reset tìm kiếm về dữ liệu gốc"""
    if df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Không có dữ liệu gốc để reset!")
        return df_original, current_page

    # Khôi phục dữ liệu về trạng thái ban đầu
    df_current = df_original.copy()
    current_page = 1

    # Xóa nội dung ô tìm kiếm để đảm bảo reset hoàn toàn
    search_entry.delete(0, 'end')

    # Tính lại số trang sau khi reset
    total_pages = get_total_pages(df_current, items_per_page)

    # Cập nhật lại bảng hiển thị
    update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")

    messagebox.showinfo("Thông báo", "Đã reset tìm kiếm về dữ liệu gốc!")

    return df_current, current_page