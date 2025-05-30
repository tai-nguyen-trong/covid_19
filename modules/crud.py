# import pandas as pd
# import numpy as np
# from tkinter import messagebox, filedialog
# import tkinter as tk
# from modules.navigation import get_total_pages
# from modules.updateTable import update_table_display

# # Biến toàn cục để quản lý dữ liệu
# df = None
# df_original = None
# df_current = None

# def load_csv_file(tree, page_label, pagination_frame, button_frame, search_frame, function_buttons, function_buttons2, sort_column, get_total_pages, items_per_page):
#     """Hàm đọc file CSV và cập nhật dữ liệu."""

#     # Mở dialog chọn file
#     file_path = filedialog.askopenfilename(
#         title="Chọn file CSV",
#         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
#     )

#     if file_path:
#         try:
#             df = pd.read_csv(file_path)
#             if df is None or df.empty:
#                 messagebox.showerror("Lỗi", "Không thể đọc file CSV hoặc file không có dữ liệu!")
#                 return

#             df_original = df.copy()
#             df_current = df.copy() 
#             current_page = 1  # Đặt lại trang hiện tại về 1 

#             # Xóa dữ liệu cũ trong Treeview
#             for item in tree.get_children():
#                 tree.delete(item)

#             # Cấu hình lại cột nếu cần
#             headers = list(df.columns)
#             tree["columns"] = headers
#             tree["show"] = "headings"

#             for col in headers:
#                 tree.heading(col, text=f"▲ {col} ▼", command=lambda _col=col: sort_column(_col))
#                 tree.column(col, width=120, anchor="center", stretch=tk.YES)

#             # Thêm dữ liệu mới vào Treeview
#             for _, row in df.iterrows():
#                 tree.insert("", "end", values=list(row))

#             messagebox.showinfo("Thành công", f"Đã tải {len(df)} bản ghi từ file {file_path}")

#             # Tính toán số trang mới
#             total_pages = get_total_pages(df_current, items_per_page)  

#             # Cập nhật bảng hiển thị và trạng thái trang
#             update_table_display(tree, page_label, df_current, current_page, items_per_page)
#             page_label.config(text=f"Trang {current_page}/{total_pages}")

#             # Hiển thị phần khung chức năng
#             pagination_frame.pack(pady=5)
#             button_frame.pack(pady=10)
#             search_frame.grid(row=0, column=1, padx=20, sticky="e")

#             # Cập nhật trạng thái nút chức năng
#             for j, btnChuyenHuong in enumerate(function_buttons2):
#                 btnChuyenHuong.grid(row=0, column=j, padx=3)  

#             for i, btn in enumerate(function_buttons):
#                 btn.grid(row=0, column=i, padx=5)  

#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi khi đọc file CSV: {str(e)}")

# def add_data(new_data, file_path="dataset/country_wise_latest.csv"):
#     """Xử lý thêm dữ liệu vào DataFrame và cập nhật file CSV."""
#     global df, df_original, df_current, current_page  

#     try:
#         df_existing = pd.read_csv(file_path, dtype=str)
#     except FileNotFoundError:
#         df_existing = pd.DataFrame()

#     # 🔁 Chuyển các trường rỗng thành NaN
#     new_data = {key: (val if val.strip() != "" else np.nan) for key, val in new_data.items()}

#     # ➕ Thêm dòng mới vào dữ liệu hiện tại
#     new_row = pd.DataFrame([new_data])
#     df = pd.concat([df_existing, new_row], ignore_index=True)  
#     df_original = df.copy()
#     df_current = df.copy()  

#     # Ghi lại file CSV
#     df.to_csv(file_path, index=False)

#     return df_current  # Trả về DataFrame cập nhật để hiển thị trên giao diện

# def update_data(selected_items, tree, page_label, current_page, items_per_page, file_path="dataset/country_wise_latest.csv"):
#     """Xử lý cập nhật dữ liệu từ Treeview."""
#     global df, df_original, df_current  

#     if df is None or df_original is None:
#         messagebox.showerror("Lỗi", "Dữ liệu không khả dụng để cập nhật!")
#         return None, None

#     df = df_original.copy()

#     index = tree.index(selected_items[0]) + (current_page - 1) * items_per_page

#     if index >= len(df):
#         messagebox.showerror("Lỗi", "Chỉ mục cập nhật vượt quá kích thước dữ liệu!")
#         return None, None

#     current_data = df.iloc[index].to_dict()

#     def on_submit(updated_data):
#         global df, df_original, df_current, current_page  # 🔥 Đảm bảo biến toàn cục hoạt động đúng

#         try:
#             for key in updated_data:
#                 if key in df.columns:
#                     if df[key].dtype in ["int64", "float64"]:  
#                         try:
#                             updated_data[key] = float(updated_data.get(key, 0))  # ✅ Tránh lỗi `NoneType`
#                         except ValueError:
#                             messagebox.showerror("Lỗi", f"Giá trị '{updated_data[key]}' không hợp lệ cho cột {key}. Vui lòng nhập số.")
#                             return
                    
#                     # 🔥 Đảm bảo giá trị số không bị chuyển thành NaN
#                     df.at[index, key] = updated_data[key] if isinstance(updated_data[key], (int, float)) or str(updated_data.get(key, "")).strip() != "" else np.nan  

#             df_original = df.copy()
#             df_current = df.copy()  # 🔥 Đồng bộ dữ liệu ngay sau khi cập nhật

#             df.to_csv(file_path, index=False)

#             if df_current is not None and not df_current.empty:
#                 total_pages = get_total_pages(df_current, items_per_page)  
#                 current_page = total_pages 
#             else:
#                 current_page = 1  # Nếu dữ liệu rỗng, đặt lại `current_page`

#             update_table_display(tree, page_label, df_current, current_page, items_per_page)  # 🔥 Hiển thị dữ liệu mới ngay lập tức
#             page_label.config(text=f"Trang {current_page}/{total_pages}")

#             messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công.")
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi cập nhật dữ liệu: {str(e)}")

#     return current_data, on_submit  # ✅ Trả về cả dữ liệu và hàm xử lý

# def delete_data(selected_items, tree, page_label, current_page, items_per_page, file_path="dataset/country_wise_latest.csv"):
#     """Xóa dữ liệu từ Treeview và cập nhật file CSV."""
#     global df, df_original, df_current  

#     if df is None or df.empty:
#         messagebox.showerror("Lỗi", "Dữ liệu hiện tại không hợp lệ để xóa!")
#         return

#     if not selected_items:
#         messagebox.showwarning("Chưa chọn", "Hãy chọn ít nhất một dòng để xóa.")
#         return

#     if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa các dòng đã chọn?"):
#         return

#     # Lấy chỉ mục chính xác của dòng cần xóa
#     indexes_to_delete = [tree.index(item) + (current_page - 1) * items_per_page for item in selected_items]

#     # Kiểm tra chỉ mục hợp lệ
#     valid_indexes = [i for i in indexes_to_delete if i < len(df)]

#     if not valid_indexes:
#         messagebox.showerror("Lỗi", "Không có chỉ mục hợp lệ để xóa!")
#         return

#     # Xóa các dòng hợp lệ
#     df = df.drop(df.index[valid_indexes]).reset_index(drop=True)
#     df_original = df.copy()
#     df_current = df.copy()  

#     # 🔥 Nếu tất cả dữ liệu bị xóa, đặt lại `df_current` thành DataFrame rỗng
#     if df_current.empty:
#         current_page = 1
#         page_label.config(text="Trang -/-")
#     else:
#         total_pages = get_total_pages(df_current, items_per_page)
#         current_page = min(current_page, total_pages)

#     # Lưu lại dữ liệu
#     df.to_csv(file_path, index=False)

#     # Cập nhật giao diện
#     update_table_display(tree, page_label, df_current, current_page, items_per_page)

#     messagebox.showinfo("Thành công", "Đã xóa thành công các dòng đã chọn.")

import pandas as pd

def clean_data(df):
    """Làm sạch dữ liệu: Xóa hàng trống hoặc sai định dạng cho tất cả cột."""
    if df is None or df.empty:
        print("Không có dữ liệu để làm sạch.")
        return df

    print("Trước khi làm sạch:")
    print(df.info())

    # 🔥 Loại bỏ hàng có bất kỳ giá trị nào bị trống
    df_cleaned = df.dropna()

    # 🔥 Lấy danh sách tất cả các cột
    all_columns = df_cleaned.columns.tolist()
    print(f"Các cột trong dataset: {all_columns}")

    # 🔥 Chuẩn hóa dữ liệu dạng chuỗi: Loại bỏ khoảng trắng dư và ký tự không hợp lệ
    for col in df_cleaned.select_dtypes(include=['object']).columns:
        df_cleaned[col] = df_cleaned[col].str.strip()  # Xóa khoảng trắng dư

    # 🔥 Chuyển đổi kiểu dữ liệu cho tất cả cột số
    for col in df_cleaned.select_dtypes(include=['number']).columns:
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')

    # 🔥 Loại bỏ hàng chứa giá trị NaN sau khi chuẩn hóa
    df_cleaned = df_cleaned.dropna()

    print("Sau khi làm sạch:")
    print(df_cleaned.info())

    return df_cleaned


