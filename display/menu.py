# display/menu.py

import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox # Cần để hiển thị cảnh báo trực tiếp từ menu.py

from modules import app_logic # Chỉ import app_logic

# Biến toàn cục cho ứng dụng (QUẢN LÝ DỮ LIỆU TẠI ĐÂY)
df = None # df hiện tại đang hiển thị trên bảng chính (có thể là original hoặc đã lọc trước đó)
df_original = None # Luôn là dữ liệu gốc sau khi tải file
current_page = 1
items_per_page = 20

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("COVID-19 Data Analysis")
root.geometry("1000x700")

# Cấu hình grid cho cửa sổ chính
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=3) # Hàng chứa bảng
root.grid_rowconfigure(2, weight=1) # Hàng chứa nút phân trang
root.grid_rowconfigure(3, weight=1) # Hàng chứa nút lọc

# --- TẠO CÁC PHẦN TỬ GIAO DIỆN (CHỈ UI) ---

# Tạo menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)

def handle_open_file():
    global df, df_original, current_page
    # app_logic.open_file_action sẽ trả về DataFrame đã đọc
    new_df_read = app_logic.open_file_action()
    print("Tat Ca Data trong csv:", new_df_read)
    if new_df_read is not None:
        df_original = new_df_read.copy() # Cập nhật df_original của menu.py
        df = new_df_read.copy() # Bảng chính hiển thị dữ liệu gốc ban đầu
        
        # Cấu hình cột Treeview sau khi có df
        for row in table.get_children():
            table.delete(row)
        table["columns"] = list(df.columns)
        for col_name in df.columns:
            table.heading(col_name, text=col_name)
            table.column(col_name, width=120, anchor="center", stretch=tk.YES)
        table.column("#0", width=0, stretch=tk.NO) # Ẩn cột ID mặc định

        current_page = 1 # Về trang đầu sau khi tải
        app_logic.update_table_display(table, page_label, df, current_page, items_per_page)

file_menu.add_command(label="Open File", command=handle_open_file)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Tạo Frame để chứa Treeview và Scrollbar
table_frame = tk.Frame(root)
table_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

table_frame.grid_columnconfigure(0, weight=1)
table_frame.grid_rowconfigure(0, weight=1)

# Tạo Scrollbar dọc
v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
v_scrollbar.grid(row=0, column=1, sticky="ns")

# Tạo Scrollbar ngang
h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
h_scrollbar.grid(row=1, column=0, sticky="ew")

# Tạo Treeview bên trong table_frame và liên kết với scrollbars
table = ttk.Treeview(table_frame, show="headings",
                     yscrollcommand=v_scrollbar.set,
                     xscrollcommand=h_scrollbar.set)
table.grid(row=0, column=0, sticky="nsew")

v_scrollbar.config(command=table.yview)
h_scrollbar.config(command=table.xview)

# Hàm xử lý điều hướng trang (gọi app_logic.handle_page_navigation)
def navigate_page(action_type):
    global current_page
    if df is None: return # Không làm gì nếu chưa có dữ liệu

    # app_logic.handle_page_navigation sẽ trả về số trang mới
    new_page = app_logic.handle_page_navigation(df, current_page, items_per_page, action_type)
    
    if new_page != current_page: # Chỉ cập nhật và hiển thị nếu trang thay đổi
        current_page = new_page
        app_logic.update_table_display(table, page_label, df, current_page, items_per_page)

# Nút điều hướng phân trang
first_page_button = tk.Button(root, text="Trang đầu", command=lambda: navigate_page("first"))
first_page_button.grid(row=2, column=0, padx=5, pady=5)

prev_page_button = tk.Button(root, text="Trang trước", command=lambda: navigate_page("prev"))
prev_page_button.grid(row=2, column=1, padx=5, pady=5)

next_page_button = tk.Button(root, text="Trang sau", command=lambda: navigate_page("next"))
next_page_button.grid(row=2, column=2, padx=5, pady=5)

last_page_button = tk.Button(root, text="Trang cuối", command=lambda: navigate_page("last"))
last_page_button.grid(row=2, column=3, padx=5, pady=5)

page_label = tk.Label(root, text="Trang -/-")
page_label.grid(row=2, column=4, padx=5, pady=5)

# Nút lọc dữ liệu
def handle_filter_click():
    if df_original is None:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return
    # Truyền root và df_original vào hàm lọc để app_logic có thể dùng
    app_logic.show_filter_window(root, df_original)

filter_button = tk.Button(root, text="Lọc dữ liệu", command=handle_filter_click)
filter_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# --- KHỞI TẠO LOGIC ỨNG DỤNG ---
# app_logic không còn cần các biến toàn cục nữa.
app_logic.init_logic()

# Chạy giao diện Tkinter
root.mainloop()