# modules/app_logic.py

import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os

from modules import crud
from modules import filters # Import module filters đã tách

# app_logic sẽ không lưu trữ các DataFrame hoặc biến phân trang là global ở đây.
# Thay vào đó, chúng sẽ được truyền vào các hàm khi cần xử lý.

def init_logic():
    """
    Khởi tạo bất kỳ thiết lập ban đầu nào cho module app_logic.
    Hiện tại không cần thiết lập gì đặc biệt ở đây.
    """
    pass

def open_file_action():
    """
    Hàm mở file CSV.
    Trả về DataFrame gốc đã đọc hoặc None nếu có lỗi/không chọn file.
    """
    file_path = filedialog.askopenfilename(
        title="Open Data File",
        filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")),
        initialdir=os.path.join(os.getcwd(), "dataset")
    )
    if file_path:
        try:
            temp_df = crud.read_data(file_path)
            if temp_df is not None and not temp_df.empty:
                messagebox.showinfo("Success", "Tải dữ liệu lên thành công!")
                return temp_df # Trả về DataFrame đã đọc
            else:
                messagebox.showwarning("Warning", "File dữ liệu rỗng hoặc không đọc được.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi hệ thống: {e}")
            return None
    return None

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

    page_data = crud.paginate_data(df_to_display, current_page_num, items_per_pg)

    for row in target_table.get_children():
        target_table.delete(row)

    # Cập nhật các cột của Treeview nếu chưa được thiết lập (hoặc thay đổi)
    # Đây là bước quan trọng để đảm bảo bảng có đúng cột khi dữ liệu thay đổi
    if not target_table["columns"]: # Nếu chưa có cột nào được định nghĩa
        target_table["columns"] = list(df_to_display.columns)
        for col_name in df_to_display.columns:
            target_table.heading(col_name, text=col_name)
            target_table.column(col_name, width=120, anchor="center", stretch=tk.YES)
        target_table.column("#0", width=0, stretch=tk.NO) # Ẩn cột ID mặc định
    
    # Kiểm tra xem số lượng cột có khớp không, nếu không thì reset cột
    elif list(target_table["columns"]) != list(df_to_display.columns):
        target_table["columns"] = list(df_to_display.columns)
        for col_name in df_to_display.columns:
            target_table.heading(col_name, text=col_name)
            target_table.column(col_name, width=120, anchor="center", stretch=tk.YES)
        target_table.column("#0", width=0, stretch=tk.NO)


    for _, row in page_data.iterrows():
        target_table.insert("", "end", values=list(row))

    total_pages = crud.get_total_pages(df_to_display, items_per_pg)
    target_page_label.config(text=f"Trang {current_page_num}/{total_pages}")

def handle_page_navigation(df_current, current_page_num, items_per_pg, action_type):
    """
    Xử lý điều hướng trang.
    Trả về số trang mới.
    """
    if df_current is None: return current_page_num # Không làm gì nếu df rỗng

    total_pages = crud.get_total_pages(df_current, items_per_pg)
    new_page = current_page_num

    if action_type == "next":
        if current_page_num < total_pages:
            new_page += 1
        else:
            messagebox.showinfo("Thông báo", "Đây là trang cuối cùng.")
    elif action_type == "prev":
        if current_page_num > 1:
            new_page -= 1
        else:
            messagebox.showinfo("Thông báo", "Đây là trang đầu tiên.")
    elif action_type == "first":
        new_page = 1
    elif action_type == "last":
        new_page = total_pages
    
    return new_page

def show_filter_window(root_window, df_original_data):
    """
    Mở cửa sổ nhập điều kiện lọc. Sau khi lọc, hiển thị kết quả trong một bảng mới.
    root_window: cửa sổ cha để Toplevel được liên kết.
    df_original_data: DataFrame gốc để lọc.
    """
    if df_original_data is None:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return

    filter_input_window = tk.Toplevel(root_window) # Cửa sổ nhập điều kiện lọc
    filter_input_window.title("Nhập điều kiện lọc")
    filter_input_window.transient(root_window) # Làm cho cửa sổ này luôn nằm trên cửa sổ chính
    filter_input_window.grab_set() # Chặn tương tác với cửa sổ chính cho đến khi đóng cửa sổ này

    tk.Label(filter_input_window, text="Chọn cột:").grid(row=0, column=0, padx=10, pady=10)
    columns = df_original_data.columns.tolist()
    column_combobox = ttk.Combobox(filter_input_window, values=columns, state="readonly")
    column_combobox.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(filter_input_window, text="Giá trị nhỏ nhất:").grid(row=1, column=0, padx=10, pady=10)
    min_value_entry = tk.Entry(filter_input_window)
    min_value_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(filter_input_window, text="Giá trị lớn nhất:").grid(row=2, column=0, padx=10, pady=10)
    max_value_entry = tk.Entry(filter_input_window)
    max_value_entry.grid(row=2, column=1, padx=10, pady=10)

    def apply_filter_and_show_results():
        column = column_combobox.get()
        if not column:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để lọc.")
            return

        try:
            min_value = float(min_value_entry.get())
            max_value = float(max_value_entry.get())

            # Luôn lọc trên bản gốc để reset các bộ lọc trước đó
            filtered_df = filters.filter_data(df_original_data.copy(), column, min_value, max_value)

            if not filtered_df.empty:
                messagebox.showinfo("Success", "Dữ liệu đã được lọc và hiển thị trong cửa sổ mới!")
                filter_input_window.destroy() # Đóng cửa sổ nhập điều kiện
                
                # Mở cửa sổ mới để hiển thị kết quả
                display_filtered_data_window(root_window, filtered_df)
            else:
                messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu phù hợp với điều kiện lọc.")
                # Nếu không tìm thấy, cửa sổ nhập điều kiện vẫn mở để người dùng thử lại
                
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập không hợp lệ! Vui lòng nhập số.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình lọc: {e}")

    tk.Button(filter_input_window, text="Lọc dữ liệu", command=apply_filter_and_show_results).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    # # Khi cửa sổ input đóng, nhả grab_set() để tương tác lại với cửa sổ chính
    # filter_input_window.protocol("WM_DELETE_WINDOW", lambda: (filter_input_window.destroy(), root_window.grab_release()))
    # root_window.wait_window(filter_input_window) # Chờ cho đến khi cửa sổ input đóng


def display_filtered_data_window(root_window, filtered_df):
    """
    Tạo một cửa sổ Toplevel mới để hiển thị DataFrame đã lọc.
    """
    if filtered_df is None or filtered_df.empty:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị trong cửa sổ lọc.")
        return

    result_window = tk.Toplevel(root_window)
    result_window.title("Kết quả lọc dữ liệu")
    result_window.geometry("800x500")
    result_window.transient(root_window) # Làm cho cửa sổ này luôn nằm trên cửa sổ chính

    result_window.grid_columnconfigure(0, weight=1)
    result_window.grid_rowconfigure(0, weight=1) # Cho bảng
    result_window.grid_rowconfigure(1, weight=0) # Cho label phân trang
    result_window.grid_rowconfigure(2, weight=0) # Cho nút phân trang

    # Frame chứa bảng và scrollbar
    result_table_frame = tk.Frame(result_window)
    result_table_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    result_table_frame.grid_columnconfigure(0, weight=1)
    result_table_frame.grid_rowconfigure(0, weight=1)

    result_v_scrollbar = ttk.Scrollbar(result_table_frame, orient="vertical")
    result_v_scrollbar.grid(row=0, column=1, sticky="ns")

    result_h_scrollbar = ttk.Scrollbar(result_table_frame, orient="horizontal")
    result_h_scrollbar.grid(row=1, column=0, sticky="ew")

    result_table = ttk.Treeview(result_table_frame, show="headings",
                                yscrollcommand=result_v_scrollbar.set,
                                xscrollcommand=result_h_scrollbar.set)
    result_table.grid(row=0, column=0, sticky="nsew")

    result_v_scrollbar.config(command=result_table.yview)
    result_h_scrollbar.config(command=result_table.xview)

    result_page_label = tk.Label(result_window, text="Trang -/-")
    result_page_label.grid(row=1, column=0, padx=5, pady=5)

    # --- Điều khiển phân trang cho cửa sổ mới ---
    # Sử dụng một danh sách để giữ trạng thái trang hiện tại một cách mutable
    current_filtered_page = [1] 
    items_per_page_filtered = 20 

    def navigate_filtered_page_internal(action_type):
        nonlocal current_filtered_page
        new_page = handle_page_navigation(filtered_df, current_filtered_page[0], items_per_page_filtered, action_type)
        if new_page != current_filtered_page[0]:
            current_filtered_page[0] = new_page
            update_table_display(result_table, result_page_label, filtered_df, current_filtered_page[0], items_per_page_filtered)

    # Các nút cho phân trang của cửa sổ mới
    button_frame = tk.Frame(result_window)
    button_frame.grid(row=2, column=0, pady=5)

    tk.Button(button_frame, text="Trang đầu", command=lambda: navigate_filtered_page_internal("first")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang trước", command=lambda: navigate_filtered_page_internal("prev")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang sau", command=lambda: navigate_filtered_page_internal("next")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang cuối", command=lambda: navigate_filtered_page_internal("last")).pack(side=tk.LEFT, padx=5)


    # Ban đầu hiển thị dữ liệu đã lọc
    update_table_display(result_table, result_page_label, filtered_df, current_filtered_page[0], items_per_page_filtered)