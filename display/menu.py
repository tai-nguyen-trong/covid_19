# display/menu.py
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox 
from .formInfo import show_form_window
from modules import search
from modules.crud import  handle_add_data, handle_update_data, handle_delete_data
from modules.cleanData import clean_data
from modules import sort
from modules import updateTable
from modules import navigation
from modules.chart import open_chart_window
from modules.filters import show_filter_window
from modules.navigation import get_total_pages, handle_page_navigation
from modules.updateTable import update_table_display
from modules.chart import open_chart_window


# Biến toàn cục cho ứng dụng (QUẢN LÝ DỮ LIỆU TẠI ĐÂY)
df = None # df hiện tại đang hiển thị trên bảng chính (có thể là original hoặc đã lọc trước đó)
df_original = None 
df_current = None
current_page = 1
items_per_page = 30
ascending_order = {}  # Dictionary để lưu trạng thái sắp xếp từng cột

# ======================= GLOBAL VARIABLES =======================
current_df = pd.DataFrame()  # DataFrame hiện tại
filtered_df = pd.DataFrame()  # DataFrame đã lọc

def handle_load_csv():
    """Hàm đọc file CSV và hiển thị lên Treeview"""
    global df, df_original, df_current, current_page  

    # Mở dialog chọn file
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if file_path:
        try:
            # Đọc file CSV và kiểm tra dữ liệu hợp lệ
            df = pd.read_csv(file_path)
            if df is None or df.empty:
                messagebox.showerror("Lỗi", "Không thể đọc file CSV hoặc file không có dữ liệu!")
                return

            # Đồng bộ dữ liệu gốc và hiện tại
            df_original = df.copy()
            df_current = df.copy()  
            current_page = 1  

            # Xóa dữ liệu cũ trong Treeview
            for item in tree.get_children():
                tree.delete(item)

            # Cấu hình lại cột nếu cần
            headers = list(df.columns)
            tree["columns"] = headers
            tree["show"] = "headings"

            for col in headers:
                tree.heading(col, text=f"▲ {col} ▼", command=lambda _col=col: handle_sort_column(_col))
                tree.column(col, width=120, anchor="center", stretch=tk.YES)

            # Thêm dữ liệu mới vào Treeview
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            messagebox.showinfo("Thành công", f"Đã tải {len(df)} bản ghi từ file {file_path}")

            # Tính toán số trang mới
            total_pages = get_total_pages(df_current, items_per_page)  

            # Cập nhật bảng hiển thị và trạng thái trang
            update_table_display(tree, page_label, df_current, current_page, items_per_page)  
            page_label.config(text=f"Trang {current_page}/{total_pages}")  

            # Hiển thị phần khung chức năng
            pagination_frame.pack(pady=5)
            button_frame.pack(pady=10)
            search_frame.grid(row=0, column=1, padx=20, sticky="e")

            # Cập nhật trạng thái nút chức năng
            for j, btnChuyenHuong in enumerate(function_buttons2):
                btnChuyenHuong.grid(row=0, column=j, padx=3)  

            for i, btn in enumerate(function_buttons):
                btn.grid(row=0, column=i, padx=5)  

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file CSV: {str(e)}")

def handle_add_data_wrapper():
    """Wrapper function cho CRUD add"""
    global df, df_original, df_current, current_page
    df, df_original, df_current, current_page = handle_add_data(
        root, df, df_original, df_current, current_page, items_per_page, tree, page_label
    )

def handle_update_data_wrapper():
    """Wrapper function cho CRUD update"""
    global df, df_original, df_current, current_page
    df, df_original, df_current, current_page = handle_update_data(
        root, df, df_original, df_current, current_page, items_per_page, tree, page_label
    )

def handle_delete_data_wrapper():
    """Wrapper function cho CRUD delete"""
    global df, df_original, df_current, current_page
    df, df_original, df_current, current_page = handle_delete_data(
        df, df_original, df_current, current_page, items_per_page, tree, page_label
    )

def handle_clean_data():
    """Wrapper function cho clean data"""
    global df_original, df_current  
    file_path = "dataset/country_wise_latest.csv"

    if df_original is None or df_original.empty:
        messagebox.showwarning("Warning", "Không có dữ liệu để làm sạch!")
        return

    try:
        df_cleaned = clean_data(df_original.copy())
        df_current = df_cleaned.copy()  
        df_original = df_cleaned.copy()

        # Ghi dữ liệu đã làm sạch vào file CSV với encoding UTF-8 và BOM
        df_cleaned.to_csv(file_path, index=False, encoding='utf-8-sig')

        updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
        messagebox.showinfo("Success", "Dữ liệu đã được làm sạch và lưu vào file thành công!")
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi lưu file: {str(e)}")
        print(f"Chi tiết lỗi: {e}")

def handle_sort_column(col):
    """Hàm sắp xếp cột sử dụng module sort"""
    global df_current, current_page
    
    if df_current is None or df_current.empty:
        return
    
    # Gọi hàm sort từ module và nhận về df đã sort và current_page mới
    df_current, current_page = sort.sort_column(col, tree, page_label, df_current, current_page, items_per_page)

def handle_search_data(keyword):
    """Wrapper function cho search"""
    global df_current, current_page
    df_current, current_page = search.handle_search_data(
        keyword, df_original, df_current, current_page, items_per_page, tree, page_label
    )

def handle_reset_search():
    """Wrapper function cho reset search"""
    global df, df_current, current_page
    df_current, current_page = search.handle_reset_search(
        df_original, current_page, items_per_page, tree, page_label, search_entry
    )
    # Cập nhật df để đồng bộ
    df = df_current.copy()


def handle_navigate_page(action_type):
    """Sử dụng module navigation để xử lý điều hướng trang"""
    global current_page, df_current

    if df_current is None or df_current.empty: 
        return  # Không làm gì nếu chưa có dữ liệu

    # Gọi điều hướng từ module navigation
    new_page = navigation.handle_page_navigation(df_current, current_page, items_per_page, action_type)  
    
    if new_page != current_page:  # Chỉ cập nhật nếu trang thay đổi
        current_page = new_page
        updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
        
        total_pages_filtered = navigation.get_total_pages(df_current, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages_filtered}") 

# Nút lọc dữ liệu
def handle_filter_click():
    """Nút lọc dữ liệu - gọi filter window từ module"""
    global df_original
    if df_original is None or df_original.empty:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return

    # Gọi hàm show_filter_window từ module filters
    show_filter_window(root, df_original)
# tiếp tục hàm export_data
def export_data():
    global df_current
    if df_current is None or df_current.empty:
        messagebox.showwarning("Không có dữ liệu", "Không có dữ liệu để xuất.")
        return
    # Mở hộp thoại lưu tệp
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    if file_path:
        try:
            df_current.to_csv(file_path, index=False)
            messagebox.showinfo("Thành công", f"Dữ liệu đã được xuất thành công vào {file_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xuất dữ liệu: {str(e)}")

# ======================= GUI SETUP =======================
# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("COVID-19 Data Analysis")
root.geometry("1000x700")
# Mở rộng cửa sổ nhưng vẫn giữ thanh tiêu đề và nút điều khiển
root.state("zoomed")  # Sử dụng `zoomed` thay vì `fullscreen`

# ======================= LOAD FILE BUTTON =======================
file_frame = tk.Frame(root)
file_frame.pack(fill="x", anchor="w", pady=10)

btn_load_file = tk.Button(file_frame, text="Tải File CSV", command=handle_load_csv,
                        bg="lightgreen", width=15, font=("Arial", 10))
# btn_load_file.pack(side="left", padx=5)
btn_load_file.grid(row=0, column=0, padx=5, sticky="w")

# ======================= SEARCH BUTTON =======================
# search_frame = tk.Frame(root)
# search_frame.pack(pady=10)
search_frame = tk.Frame(file_frame)  # Đặt search_frame vào file_frame để nằm chung hàng
search_frame.grid(row=0, column=1, padx=100, sticky="e")  # Đặt bên phải nút tải file


tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)
search_btn = tk.Button(search_frame, text="Search", width=10)
search_btn.grid(row=0, column=2, padx=5)
# Liên kết sự kiện nhấn nút với hàm tìm kiếm
search_btn.config(command=lambda: handle_search_data(search_entry.get()))

# ======================= TREEVIEW + SCROLLBAR =======================
table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True)

# Scrollbars
tree_scroll_y = tk.Scrollbar(table_frame, orient="vertical")
tree_scroll_y.pack(side="right", fill="y")

tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
tree_scroll_x.pack(side="bottom", fill="x")

tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
tree.pack(fill="both", expand=True)

tree_scroll_y.config(command=tree.yview)
tree_scroll_x.config(command=tree.xview)

# ======================= PAGINATION BUTTONS =======================
pagination_frame = tk.Frame(root)
pagination_frame.pack(pady=5)

btn_first = tk.Button(pagination_frame, text="Trang đầu", width=10, command=lambda: handle_navigate_page("first"))
btn_prev = tk.Button(pagination_frame, text="Trang trước", width=10, command=lambda: handle_navigate_page("prev"))
btn_next = tk.Button(pagination_frame, text="Trang sau", width=10, command=lambda: handle_navigate_page("next"))
btn_last = tk.Button(pagination_frame, text="Trang cuối", width=10, command=lambda: handle_navigate_page("last"))
page_label = tk.Label(pagination_frame, text="Trang", width=12)

# ======================= CONTROL BUTTONS =======================
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10, command=handle_add_data_wrapper)
btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10, command=handle_update_data_wrapper)
btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=handle_delete_data_wrapper)
btn_reset = tk.Button(button_frame, text="Reset", bg="gray", fg="white", width=10, command=handle_reset_search)
btn_chart = tk.Button(button_frame, text="Charts", bg="purple", fg="white", width=10, command= lambda :open_chart_window(root, df))
btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10, command=export_data)

# btn_create.grid(row=0, column=0, padx=5)
# btn_update.grid(row=0, column=1, padx=5)
# btn_delete.grid(row=0, column=2, padx=5)
# btn_reset.grid(row=0, column=3, padx=5)
# btn_chart.grid(row=0, column=4, padx=5)
# btn_export.grid(row=0, column=5, padx=5)

# # ======================= SEARCH BUTTON =======================
# search_frame = tk.Frame(root)
# search_frame.pack(pady=10)

# tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
# search_entry = tk.Entry(search_frame)
# search_entry.grid(row=0, column=1, padx=5)
# search_btn = tk.Button(search_frame, text="Search", width=10)
# search_btn.grid(row=0, column=2, padx=5)
# # Liên kết sự kiện nhấn nút với hàm tìm kiếm
# search_btn.config(command=lambda: handle_search_data(search_entry.get()))


# Ẩn tất cả các nút khi chương trình khởi động
function_buttons = [btn_create, btn_update, btn_delete, btn_reset, btn_chart, btn_export]
btn_reset = tk.Button(button_frame, text="Reset", bg="lightgray", width=10, command=handle_reset_search)
btn_chart = tk.Button(button_frame, text="Charts", bg="purple", fg="white", width=10, command=lambda: open_chart_window(root, df_current))
btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10, command=export_data)
btn_filter = tk.Button(button_frame, text="Filter", bg="yellow", width=10, command=handle_filter_click)
btn_clean = tk.Button(button_frame, text="Clean Data", bg="lightcoral", width=10, command=handle_clean_data)

# Ẩn tất cả các nút khi chương trình khởi động
function_buttons = [btn_create, btn_update, btn_delete, btn_reset, btn_chart, btn_export, btn_filter, btn_clean]
function_buttons2 = [btn_first, btn_prev, btn_next, btn_last, page_label]
for btn in function_buttons:
    btn.grid_remove()

for btnChuyenHuong in function_buttons2:
    btnChuyenHuong.grid_remove()

pagination_frame.pack_forget()
button_frame.pack_forget()
search_frame.grid_remove()  

root.mainloop()