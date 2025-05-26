# display/menu.py

import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import pandas as pd # Import pandas để có thể dùng pd.DataFrame()

from modules import crud  # Import các chức năng xử lý dữ liệu từ crud.py

# Biến toàn cục
df = None  # Dữ liệu sẽ được lưu ở đây
current_page = 1
items_per_page = 20

# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("COVID-19 Data Analysis")
root.geometry("1000x700")

# --- ĐIỀU CHỈNH CẤU HÌNH grid_rowconfigure và grid_columnconfigure CHO ROOT ---
# Cột 0 (chứa hầu hết các widget) sẽ mở rộng theo chiều ngang
root.grid_columnconfigure(0, weight=1)

# Định nghĩa các hàng và trọng số của chúng:
# Hàng 0: menu bar (không cần cấu hình grid_rowconfigure trực tiếp vì nó không chiếm không gian grid)
# Hàng 1: table_frame (chứa bảng và scrollbar) - cho nó chiếm 3/4 không gian dọc
root.grid_rowconfigure(1, weight=3) # Bảng nằm ở hàng 1
# Hàng 2: Nút điều hướng phân trang - chiếm 1/4 không gian dọc
root.grid_rowconfigure(2, weight=1)
# Hàng 3: Nút lọc dữ liệu - chiếm 1/4 không gian dọc
root.grid_rowconfigure(3, weight=1)
# --- KẾT THÚC CẤU HÌNH ---


# Hàm mở file CSV (giữ nguyên như bản đã hoạt động)
def open_file():
    global df
    file_path = filedialog.askopenfilename(
        title="Open Data File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
        initialdir=os.path.join(os.getcwd(), "dataset")
    )
    if file_path:
        try:
            df = crud.read_data(file_path)
            messagebox.showinfo("Success", "Tải dữ liệu lên thành công!")

            if df is not None:
                # Xóa các hàng hiện có trong bảng
                for row in table.get_children():
                    table.delete(row)

                # Cập nhật các cột cho Treeview dựa trên DataFrame
                table["columns"] = list(df.columns)

                # Cấu hình tiêu đề và độ rộng cho từng cột
                for col_name in df.columns:
                    table.heading(col_name, text=col_name)
                    # Giảm width một chút hoặc giữ nguyên 150, quan trọng là stretch=tk.YES
                    table.column(col_name, width=120, anchor="center", stretch=tk.YES)

                table.column("#0", width=0, stretch=tk.NO) # Ẩn cột mặc định "#0"

            update_table()
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi hệ thống: {e}")

# Hàm cập nhật bảng dữ liệu (giữ nguyên)
def update_table():
    global df
    if df is None:
        # Xóa hết dữ liệu cũ nếu df là None (ví dụ: sau khi lọc không có kết quả và ta reset df)
        for row in table.get_children():
            table.delete(row)
        page_label.config(text="Trang -/-") # Reset hiển thị trang
        messagebox.showwarning("Warning", "Chưa tải dữ liệu!")
        return

    page_data = crud.paginate_data(df, current_page, items_per_page)

    for row in table.get_children():
        table.delete(row)

    for _, row in page_data.iterrows():
        table.insert("", "end", values=list(row))

    page_label.config(text=f"Trang {current_page}/{crud.get_total_pages(df, items_per_page)}")

# Các hàm next_page, prev_page, first_page, last_page (giữ nguyên, chúng đã hoạt động sau khi sửa crud.py)
def next_page():
    global current_page
    if df is None: return # Tránh lỗi nếu df rỗng
    total_pages = crud.get_total_pages(df, items_per_page)
    if current_page < total_pages:
        current_page += 1
        update_table()
    else:
        messagebox.showinfo("Thông báo", "Đây là trang cuối cùng.")

def prev_page():
    global current_page
    if df is None: return # Tránh lỗi nếu df rỗng
    if current_page > 1:
        current_page -= 1
        update_table()
    else:
        messagebox.showinfo("Thông báo", "Đây là trang đầu tiên.")

def first_page():
    global current_page
    if df is None: return # Tránh lỗi nếu df rỗng
    if current_page != 1:
        current_page = 1
        update_table()

def last_page():
    global current_page
    if df is None: return # Tránh lỗi nếu df rỗng
    total_pages = crud.get_total_pages(df, items_per_page)
    if current_page != total_pages:
        current_page = total_pages
        update_table()

# Hàm lọc theo khoảng giới hạn (đã sửa ở phiên bản trước, giữ nguyên)
def filter_data():
    global df
    if df is None:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu!")
        return

    filter_window = tk.Toplevel(root)
    filter_window.title("Lọc theo khoảng giới hạn")

    tk.Label(filter_window, text="Chọn cột:").grid(row=0, column=0, padx=10, pady=10)
    columns = df.columns.tolist()
    column_combobox = ttk.Combobox(filter_window, values=columns, state="readonly")
    column_combobox.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(filter_window, text="Giá trị nhỏ nhất:").grid(row=1, column=0, padx=10, pady=10)
    min_value_entry = tk.Entry(filter_window)
    min_value_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(filter_window, text="Giá trị lớn nhất:").grid(row=2, column=0, padx=10, pady=10)
    max_value_entry = tk.Entry(filter_window)
    max_value_entry.grid(row=2, column=1, padx=10, pady=10)

    def apply_filter():
        column = column_combobox.get()
        if not column:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để lọc.")
            return

        try:
            min_value = float(min_value_entry.get())
            max_value = float(max_value_entry.get())

            global df
            original_df_copy = df.copy()
            filtered_df = crud.filter_data(original_df_copy, column, min_value, max_value)

            if not filtered_df.empty:
                messagebox.showinfo("Success", "Dữ liệu đã được lọc!")
                df = filtered_df
                filter_window.destroy()
                first_page()
            else:
                messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu phù hợp với điều kiện lọc.")
                filter_window.destroy()

        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập không hợp lệ! Vui lòng nhập số.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình lọc: {e}")

    tk.Button(filter_window, text="Lọc dữ liệu", command=apply_filter).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Tạo menu bar (giữ nguyên)
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)


# --- PHẦN TẠO BẢNG DỮ LIỆU VÀ SCROLLBAR (ĐÃ CHỈNH SỬA CHÍNH XÁC DÙNG GRID) ---
# Tạo Frame để chứa Treeview và Scrollbar
table_frame = tk.Frame(root)
# Đặt table_frame vào grid của root, cho nó mở rộng theo mọi hướng
table_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Cấu hình grid của table_frame để các widget bên trong nó cũng mở rộng
table_frame.grid_columnconfigure(0, weight=1) # Cột chứa Treeview
table_frame.grid_rowconfigure(0, weight=1)   # Hàng chứa Treeview

# Tạo Scrollbar dọc
v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
v_scrollbar.grid(row=0, column=1, sticky="ns") # Đặt scrollbar vào cột 1 của table_frame

# Tạo Scrollbar ngang
h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
h_scrollbar.grid(row=1, column=0, sticky="ew") # Đặt scrollbar vào hàng 1 của table_frame

# Tạo Treeview bên trong table_frame và liên kết với scrollbars
table = ttk.Treeview(table_frame, show="headings",
                     yscrollcommand=v_scrollbar.set,
                     xscrollcommand=h_scrollbar.set)
# Đặt Treeview vào cột 0, hàng 0 của table_frame, cho nó mở rộng
table.grid(row=0, column=0, sticky="nsew")

# Cấu hình command cho scrollbars
v_scrollbar.config(command=table.yview)
h_scrollbar.config(command=table.xview)
# --- KẾT THÚC PHẦN TẠO BẢNG DỮ LIỆU VÀ SCROLLBAR ---


# Nút điều hướng phân trang (giữ nguyên vị trí grid cũ trên root)
first_page_button = tk.Button(root, text="Trang đầu", command=first_page)
first_page_button.grid(row=2, column=0, padx=5, pady=5)

prev_page_button = tk.Button(root, text="Trang trước", command=prev_page)
prev_page_button.grid(row=2, column=1, padx=5, pady=5)

next_page_button = tk.Button(root, text="Trang sau", command=next_page)
next_page_button.grid(row=2, column=2, padx=5, pady=5)

last_page_button = tk.Button(root, text="Trang cuối", command=last_page)
last_page_button.grid(row=2, column=3, padx=5, pady=5)

page_label = tk.Label(root, text="Trang 1")
page_label.grid(row=2, column=4, padx=5, pady=5)

# Nút lọc dữ liệu (giữ nguyên vị trí grid cũ trên root)
filter_button = tk.Button(root, text="Lọc dữ liệu", command=filter_data)
filter_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

# Chạy giao diện Tkinter
root.mainloop()