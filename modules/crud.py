import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import math
from tkinter import filedialog

# ======================= CRUD FUNCTIONS =======================
def read_data(file_path):
    """Đọc dữ liệu từ file CSV và trả về DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}") 
        return None
    
def add_record(df, new_record: dict):
    return df.append(new_record, ignore_index=True)

def update_record(df, index: int, updated_record: dict):
    if 0 <= index < len(df):
        for key, value in updated_record.items():
            df.at[index, key] = value
    return df

def delete_record(df, index):
    if 0 <= index < len(df):
        df.drop(index, inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df

def search_record(df, query):
    query = query.lower()
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)
    return df[mask]

def sort_record(df, column, ascending=True):
    if column in df.columns:
        return df.sort_values(by=column, ascending=ascending).reset_index(drop=True)
    return df

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

# cập nhật bảng dữ liệu (Treeview) trên giao diện bằng cách xóa dữ liệu cũ và hiển thị dữ liệu theo trang hiện tại.
def update_table_display(target_table, target_page_label, df_to_display, current_page_num, items_per_pg):
    """
    Hàm cập nhật một bảng dữ liệu (Treeview) trên giao diện.
    Nhận target_table (Treeview), target_page_label (Label), DataFrame cần hiển thị,
    số trang hiện tại và số mục trên trang làm đối số.
    """
    if df_to_display is None or df_to_display.empty:
        for row in target_table.get_children():
            target_table.delete(row)
        target_page_label.config(text="Trang -/-")
        return
    
    total_pages = get_total_pages(df_to_display, items_per_pg)

    # Phân trang dữ liệu
    start_idx = (current_page_num - 1) * items_per_pg
    end_idx = start_idx + items_per_pg
    page_data = df_to_display.iloc[start_idx:end_idx]

    # Xóa dữ liệu cũ trong bảng
    for row in target_table.get_children():
        target_table.delete(row)

    # Cập nhật dữ liệu vào bảng
    for _, row in page_data.iterrows():

        target_table.insert("", "end", values=list(row))

    target_page_label.config(text=f"Trang {current_page_num}/{total_pages}")
