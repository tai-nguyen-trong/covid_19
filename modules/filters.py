# modules/filters.py
import math
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from modules import updateTable
from modules.navigation import handle_page_navigation, paginate_data

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

    # def apply_filter_and_show_results():
    #     column = column_combobox.get()
    #     if not column:
    #         messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để lọc.")
    #         return

    #     try:
    #         min_value = float(min_value_entry.get())
    #         max_value = float(max_value_entry.get())

    #         # Luôn lọc trên bản gốc để reset các bộ lọc trước đó
    #         filtered_df = filter_data(df_original_data.copy(), column, min_value, max_value)

    #         if not filtered_df.empty:
    #             messagebox.showinfo("Success", "Dữ liệu đã được lọc và hiển thị trong cửa sổ mới!")
    #             filter_input_window.destroy() # Đóng cửa sổ nhập điều kiện
                
    #             # Mở cửa sổ mới để hiển thị kết quả
    #             display_filtered_data_window(root_window, filtered_df)
    #         else:
    #             messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu phù hợp với điều kiện lọc.")
    #             # Nếu không tìm thấy, cửa sổ nhập điều kiện vẫn mở để người dùng thử lại
                
    #     except ValueError:
    #         messagebox.showerror("Lỗi", "Giá trị nhập không hợp lệ! Vui lòng nhập số.")
    #     except Exception as e:
    #         messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình lọc: {e}")
    def apply_filter_and_show_results():
        column = column_combobox.get()
        if not column:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn cột để lọc.")
            return

        try:
            min_value = float(min_value_entry.get())
            max_value = float(max_value_entry.get())

            print(f"Đang lọc dữ liệu trên cột: {column}, min_value: {min_value}, max_value: {max_value}")  # 🔥 Kiểm tra giá trị

            # Luôn lọc trên bản gốc để reset các bộ lọc trước đó
            filtered_df = filter_data(df_original_data.copy(), column, min_value, max_value)

            print(f"Số dòng sau khi lọc: {len(filtered_df)}")  # 🔥 Kiểm tra kết quả lọc

            if not filtered_df.empty:
                messagebox.showinfo("Success", "Dữ liệu đã được lọc và hiển thị trong cửa sổ mới!")
                filter_input_window.destroy()  # Đóng cửa sổ nhập điều kiện

                # Mở cửa sổ mới để hiển thị kết quả
                display_filtered_data_window(root_window, filtered_df)
            else:
                messagebox.showwarning("Thông báo", "Không tìm thấy dữ liệu phù hợp với điều kiện lọc.")
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị nhập không hợp lệ! Vui lòng nhập số.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra trong quá trình lọc: {e}")

    tk.Button(filter_input_window, text="Lọc dữ liệu", command=apply_filter_and_show_results).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    # # Khi cửa sổ input đóng, nhả grab_set() để tương tác lại với cửa sổ chính
    # filter_input_window.protocol("WM_DELETE_WINDOW", lambda: (filter_input_window.destroy(), root_window.grab_release()))
    # root_window.wait_window(filter_input_window) # Chờ cho đến khi cửa sổ input đóng


def display_filtered_data_window(root_window, filtered_df):
    """Hiển thị dữ liệu đã lọc trong cửa sổ mới với phân trang và thanh cuộn."""
    if filtered_df is None or filtered_df.empty:
        messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị trong cửa sổ lọc.")
        return

    print(f"Số dòng đã lọc: {len(filtered_df)}")  # 🔥 Kiểm tra số dòng sau khi lọc

    result_window = tk.Toplevel(root_window)
    result_window.title("Kết quả lọc dữ liệu")
    result_window.geometry("800x500")
    result_window.transient(root_window)

    result_table = ttk.Treeview(result_window, show="headings")
    result_table.pack(fill="both", expand=True)

    result_table["columns"] = list(filtered_df.columns)  # 🔥 Đảm bảo cột đúng

    for col in filtered_df.columns:
        result_table.heading(col, text=col)
        result_table.column(col, anchor="center", width=120)

    result_page_label = tk.Label(result_window, text="Trang 1/-")
    result_page_label.pack()

    # 🔥 Tính toán phân trang
    current_filtered_page = [1]  
    items_per_page_filtered = 20  
    total_pages = math.ceil(len(filtered_df) / items_per_page_filtered)  # 🔥 Tính đúng số trang
    paginated_df = paginate_data(filtered_df, current_filtered_page[0], items_per_page_filtered)

    print(f"Số trang: {total_pages}, Số dòng sau phân trang: {len(paginated_df)}")  # 🔥 Kiểm tra dữ liệu phân trang

    result_page_label.config(text=f"Trang {current_filtered_page[0]}/{total_pages}")  # 🔥 Hiển thị số trang đúng
    updateTable.update_table_display(result_table, result_page_label, paginated_df, current_filtered_page[0], items_per_page_filtered)

    # 🔥 Thêm nút phân trang
    button_frame = tk.Frame(result_window)
    button_frame.pack()

    def navigate_filtered_page(action_type):
        new_page = handle_page_navigation(filtered_df, current_filtered_page[0], items_per_page_filtered, action_type)
        if new_page != current_filtered_page[0]:
            current_filtered_page[0] = new_page
            paginated_df = paginate_data(filtered_df, current_filtered_page[0], items_per_page_filtered)
            updateTable.update_table_display(result_table, result_page_label, paginated_df, current_filtered_page[0], items_per_page_filtered)

            result_page_label.config(text=f"Trang {current_filtered_page[0]}/{total_pages}")  # 🔥 Cập nhật số trang

    tk.Button(button_frame, text="Trang đầu", command=lambda: navigate_filtered_page("first")).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Trang trước", command=lambda: navigate_filtered_page("prev")).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Trang sau", command=lambda: navigate_filtered_page("next")).pack(side=tk.LEFT)
    tk.Button(button_frame, text="Trang cuối", command=lambda: navigate_filtered_page("last")).pack(side=tk.LEFT)
def navigate_filtered_page(action_type):
    global filtered_df, current_filtered_page, items_per_page_filtered, result_table, result_page_label  # 🔥 Đảm bảo biến toàn cục hoạt động đúng

    new_page = handle_page_navigation(filtered_df, current_filtered_page[0], items_per_page_filtered, action_type)
    
    if new_page != current_filtered_page[0]:
        current_filtered_page[0] = new_page
        paginated_df = paginate_data(filtered_df, current_filtered_page[0], items_per_page_filtered)
        updateTable.update_table_display(result_table, result_page_label, paginated_df, current_filtered_page[0], items_per_page_filtered)
        
        # 🔥 Cập nhật lại số trang hiển thị
        total_pages = math.ceil(len(filtered_df) / items_per_page_filtered)
        result_page_label.config(text=f"Trang {current_filtered_page[0]}/{total_pages}")