# modules/filters.py
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from modules import crud
from modules.navigation import handle_page_navigation

def filter_data(df, column, min_value, max_value):
    """Lọc dữ liệu theo khoảng giá trị cho một cột cụ thể."""
    if df is None or df.empty:
        return pd.DataFrame()

    if column not in df.columns:
        raise ValueError(f"Cột '{column}' không tồn tại trong dữ liệu.")

    df_copy = df.copy() # Tạo một bản sao để tránh cảnh báo SettingWithCopyWarning

    # Đảm bảo cột là kiểu số để lọc, chuyển đổi lỗi thành NaN
    df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
    
    # Loại bỏ các hàng có giá trị NaN trong cột đang lọc
    filtered_df = df_copy.dropna(subset=[column])

    # Lọc dữ liệu
    filtered_df = filtered_df[(filtered_df[column] >= min_value) & (filtered_df[column] <= max_value)]
    return filtered_df

# mở cửa sổ nhập điều kiện lọc và hiển thị kết quả lọc trong một bảng mới.
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
            filtered_df = filter_data(df_original_data.copy(), column, min_value, max_value)

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


# tạo một cửa sổ mới (Toplevel) để hiển thị dữ liệu đã lọc
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
            crud.update_table_display(result_table, result_page_label, filtered_df, current_filtered_page[0], items_per_page_filtered)

    # Các nút cho phân trang của cửa sổ mới
    button_frame = tk.Frame(result_window)
    button_frame.grid(row=2, column=0, pady=5)

    tk.Button(button_frame, text="Trang đầu", command=lambda: navigate_filtered_page_internal("first")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang trước", command=lambda: navigate_filtered_page_internal("prev")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang sau", command=lambda: navigate_filtered_page_internal("next")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Trang cuối", command=lambda: navigate_filtered_page_internal("last")).pack(side=tk.LEFT, padx=5)


    # Ban đầu hiển thị dữ liệu đã lọc
    crud.update_table_display(result_table, result_page_label, filtered_df, current_filtered_page[0], items_per_page_filtered)