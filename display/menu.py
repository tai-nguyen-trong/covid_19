# display/menu.py=
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import messagebox 
from display.formInfo import show_form_window
from modules import crud
from modules import sort
from modules import updateTable
from modules import navigation
from modules.chart import open_chart_window
from modules.filters import show_filter_window
from modules.navigation import get_total_pages, handle_page_navigation
# from modules.sort import sort_column
from modules.updateTable import update_table_display

# Biến toàn cục cho ứng dụng (QUẢN LÝ DỮ LIỆU TẠI ĐÂY)
df = None # df hiện tại đang hiển thị trên bảng chính (có thể là original hoặc đã lọc trước đó)
df_original = None # Luôn là dữ liệu gốc sau khi tải file
df_current = None
current_page = 1
items_per_page = 30
ascending_order = {}  # Dictionary để lưu trạng thái sắp xếp từng cột

# ======================= GLOBAL VARIABLES =======================
current_df = pd.DataFrame()  # DataFrame hiện tại
filtered_df = pd.DataFrame()  # DataFrame đã lọc

# def handle_load_csv():
#     """Hàm đọc file CSV và hiển thị lên Treeview"""
#     global df, df_original, df_current, current_page  

#     # Mở dialog chọn file
#     file_path = filedialog.askopenfilename(
#         title="Chọn file CSV",
#         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
#     )

#     if file_path:
#         try:
#             # Đọc file CSV và kiểm tra dữ liệu hợp lệ
#             df = pd.read_csv(file_path)
#             if df is None or df.empty:
#                 messagebox.showerror("Lỗi", "Không thể đọc file CSV hoặc file không có dữ liệu!")
#                 return

#             # Đồng bộ dữ liệu gốc và hiện tại
#             df_original = df.copy()
#             df_current = df.copy()  
#             current_page = 1  

#             # Xóa dữ liệu cũ trong Treeview
#             for item in tree.get_children():
#                 tree.delete(item)

#             # Cấu hình lại cột nếu cần
#             headers = list(df.columns)
#             tree["columns"] = headers
#             tree["show"] = "headings"

#             for col in headers:
#                 tree.heading(col, text=f"▲ {col} ▼", command=lambda _col=col: handle_sort_column(_col))
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
def handle_load_csv():
    """Gọi chức năng load CSV từ module `crud.py`"""
    global df_current
    df_current = crud.load_csv_file(tree, page_label, pagination_frame, button_frame, search_frame, function_buttons, function_buttons2, handle_sort_column, get_total_pages, items_per_page)
    print("df_current menu", df_current)  # 🔥 Kiểm tra dữ liệu hiện tại trước khi tải file

# def handle_add_data():
#     def on_submit(new_data):
#         global df, df_original, df_current, current_page  

#         try:
#             df_existing = pd.read_csv("dataset/country_wise_latest.csv", dtype=str)  # Đọc dữ liệu dưới dạng chuỗi để tránh lỗi NaN
#         except FileNotFoundError:
#             df_existing = pd.DataFrame()

#         # 🔁 Chuyển các trường rỗng thành NaN ngay lúc thêm dữ liệu
#         new_data = {key: (val if val.strip() != "" else np.nan) for key, val in new_data.items()}

#         # ➕ Thêm dòng mới vào dữ liệu hiện tại
#         new_row = pd.DataFrame([new_data])
#         df = pd.concat([df_existing, new_row], ignore_index=True)  
#         df_original = df.copy()
#         df_current = df.copy()  

#         # Ghi lại vào file CSV
#         df.to_csv("dataset/country_wise_latest.csv", index=False)  

#         # Cập nhật số trang sau khi thêm dữ liệu
#         total_pages = get_total_pages(df_current, items_per_page)
#         current_page = max(1, total_pages)  # ✅ Đảm bảo luôn có trang hợp lệ

#         # Cập nhật bảng hiển thị
#         update_table_display(tree, page_label, df_current, current_page, items_per_page)
#         page_label.config(text=f"Trang {current_page}/{total_pages}")  

#         messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công.")

#     show_form_window(root, data=None, on_submit=on_submit)
def handle_add_data():
    def on_submit(new_data):
        global df_current, current_page  

        df_current = crud.add_data(new_data)  # Gọi chức năng xử lý từ `crud.py`

        # Cập nhật số trang sau khi thêm dữ liệu
        total_pages = get_total_pages(df_current, items_per_page)
        current_page = total_pages

        # Cập nhật bảng hiển thị
        update_table_display(tree, page_label, df_current, current_page, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages}")  

        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công.")

    show_form_window(root, data=None, on_submit=on_submit)


# def handle_update_data():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showwarning("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
#         return

#     global df, df_original, df_current, current_page  

#     if df is None or df_original is None:
#         messagebox.showerror("Lỗi", "Dữ liệu không khả dụng để cập nhật!")
#         return
#     df = df_original.copy()

#     index = tree.index(selected[0]) + (current_page - 1) * items_per_page

#     if index >= len(df):
#         messagebox.showerror("Lỗi", "Chỉ mục cập nhật vượt quá kích thước dữ liệu!")
#         return

#     current_data = df.iloc[index].to_dict()

#     def on_submit(updated_data):
#         global df, df_original, df_current, current_page  # 🔥 Khai báo `current_page` là biến toàn cục

#         try:
#             for key in updated_data:
#                 if key in df.columns:
#                     if df[key].dtype in ["int64", "float64"]:  
#                         try:
#                             updated_data[key] = float(updated_data[key])  # Giữ nguyên kiểu số
#                         except ValueError:
#                             messagebox.showerror("Lỗi", f"Giá trị '{updated_data[key]}' không hợp lệ cho cột {key}. Vui lòng nhập số.")
#                             return

#                     # 🔥 Đảm bảo giá trị số không bị chuyển thành NaN
#                     df.at[index, key] = updated_data[key] if isinstance(updated_data[key], (int, float)) or updated_data[key].strip() != "" else np.nan  

#             df_original = df.copy()
#             df_current = df.copy()  

#             df.to_csv("dataset/country_wise_latest.csv", index=False)

#             total_pages = get_total_pages(df_current, items_per_page)  
#             current_page = min(current_page, total_pages)  

#             update_table_display(tree, page_label, df_current, current_page, items_per_page)
#             page_label.config(text=f"Trang {current_page}/{total_pages}")

#             messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công.")
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi cập nhật dữ liệu: {str(e)}")

#     show_form_window(root, data=current_data, on_submit=on_submit)
def handle_update_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
        return

    current_data, on_submit = crud.update_data(selected, tree, page_label, current_page, items_per_page)

    if current_data:
        show_form_window(root, data=current_data, on_submit=on_submit)

# def handle_delete_data():
#     selected = tree.selection()
#     if not selected:
#         messagebox.showwarning("Chưa chọn", "Hãy chọn ít nhất một dòng để xóa.")
#         return

#     if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa các dòng đã chọn?"):
#         return

#     global df, df_original, df_current, current_page  

#     # 🔥 Kiểm tra nếu `df` là None hoặc rỗng
#     if df is None or df.empty:
#         messagebox.showerror("Lỗi", "Dữ liệu hiện tại không hợp lệ để xóa!")
#         return

#     # Lấy chỉ mục chính xác của dòng cần xóa
#     indexes_to_delete = [tree.index(item) + (current_page - 1) * items_per_page for item in selected]

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
#     df.to_csv("dataset/country_wise_latest.csv", index=False)
    
#     # Cập nhật giao diện
#     update_table_display(tree, page_label, df_current, current_page, items_per_page)

#     messagebox.showinfo("Thành công", "Đã xóa thành công các dòng đã chọn.")
def handle_delete_data():
    selected = tree.selection()
    crud.delete_data(selected, tree, page_label, current_page, items_per_page)


# def handle_sort_column(col):
#     """Hàm sắp xếp cột tăng hoặc giảm dần khi nhấp vào tiêu đề"""
#     global df_current, ascending_order, current_page  

#     if df_current is None or df_current.empty:
#         return  

#     # Kiểm tra trạng thái sắp xếp ban đầu
#     if col not in ascending_order:
#         ascending_order[col] = True  

#     # Đảo trạng thái sắp xếp mỗi lần nhấn
#     ascending_order[col] = not ascending_order[col]

#     # Sắp xếp dữ liệu hiện tại thay vì dữ liệu gốc
#     df_current = df_current.sort_values(by=col, ascending=ascending_order[col])

#     # 🛠 Cập nhật tiêu đề **đúng biểu tượng**
#     up_icon = "▲"
#     down_icon = "▼"
#     icon = up_icon if ascending_order[col] else down_icon
#     tree.heading(col, text=f"{col} {icon}", command=lambda _col=col: handle_sort_column(_col))

#     # 🔥 Tính lại số trang sau khi sắp xếp
#     total_pages = get_total_pages(df_current, items_per_page)
#     current_page = min(current_page, total_pages)

#     # Cập nhật lại bảng hiển thị theo dữ liệu đã lọc
#     updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
#     page_label.config(text=f"Trang {current_page}/{total_pages}")
def handle_sort_column(col):
    """Hàm sắp xếp cột tăng hoặc giảm dần khi nhấp vào tiêu đề."""
    global df_current, ascending_order, current_page  

    if df_current is None or df_current.empty:
        return  

    # 🔥 Kiểm tra kiểu dữ liệu
    print(f"Kiểu dữ liệu của cột {col}: {df_current[col].dtype}")


    # Nếu cột là số, chuyển đổi kiểu dữ liệu đúng
    if pd.api.types.is_numeric_dtype(df_current[col]):
        df_current[col] = pd.to_numeric(df_current[col], errors='coerce')
        df_current = df_current.dropna(subset=[col])  # Xóa giá trị NaN (nếu có)
    else:
        df_current[col] = df_current[col].astype(str).str.strip()  # Loại bỏ khoảng trắng đầu/cuối


    # Kiểm tra trạng thái sắp xếp ban đầu
    if col not in ascending_order:
        ascending_order[col] = True  

    # Đảo trạng thái sắp xếp mỗi lần nhấn
    ascending_order[col] = not ascending_order[col]

    # 🔥 Sắp xếp dữ liệu đúng cách
    df_current = df_current.sort_values(by=col, ascending=ascending_order[col])

    # 🛠 Cập nhật tiêu đề **đúng biểu tượng**
    up_icon = "▲"
    down_icon = "▼"
    icon = up_icon if ascending_order[col] else down_icon
    tree.heading(col, text=f"{col} {icon}", command=lambda _col=col: handle_sort_column(_col))

    # 🔥 Tính lại số trang sau khi sắp xếp
    total_pages = get_total_pages(df_current, items_per_page)
    current_page = min(current_page, total_pages)

    # Cập nhật lại bảng hiển thị theo dữ liệu đã lọc
    updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")
# def handle_sort_column(col):
#     sort.sort_column(col, tree, page_label, current_page, items_per_page, get_total_pages, update_table_display)


def handle_setup_treeview():
    global df_current, ascending_order  

    if df_current is None or df_current.empty:
        return  

    headers = list(df_current.columns)
    tree["columns"] = headers
    tree["show"] = "headings"

    # Khởi tạo trạng thái sắp xếp của mỗi cột
    for col in headers:
        ascending_order[col] = False  # ✅ Đặt mặc định là giảm dần
        tree.heading(col, text=f"{col} ▼", command=lambda _col=col: sort.sort_column(_col))
        tree.column(col, width=120, anchor="center", stretch=tk.YES)

# def handle_setup_treeview():
#     """Gọi chức năng setup Treeview từ module `crud.py`"""
#     sort.setup_treeview(tree)


def handle_search_data(keyword):
    global df_original, df_current, current_page  

    if not keyword or df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Dữ liệu gốc không hợp lệ hoặc từ khóa tìm kiếm trống!")
        return

    keyword = keyword.lower()

    # 🔍 Lọc dữ liệu
    df_filtered = df_original[df_original.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]

    if df_filtered.empty:
        messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp!")

        # 🔥 Khôi phục dữ liệu gốc để tránh lỗi hiển thị
        df_current = df_original.copy()
        current_page = 1  

        total_pages = get_total_pages(df_current, items_per_page)

        update_table_display(tree, page_label, df_current, current_page, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages}")
        return

    # 🛠 Cập nhật dữ liệu tìm kiếm
    df_current = df_filtered  
    current_page = 1  
    total_pages_filtered = get_total_pages(df_current, items_per_page)

    # Hiển thị kết quả tìm kiếm với số trang mới
    update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages_filtered}")
# def handle_search_data(keyword):
#     """Gọi chức năng tìm kiếm từ module `crud.py`"""
#     search.search_data(keyword, tree, page_label, current_page, items_per_page, get_total_pages, update_table_display)


def handle_reset_search():
    global df, df_current, current_page  

    # 🔥 Kiểm tra nếu `df_original` bị None hoặc rỗng
    if df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Không có dữ liệu gốc để reset!")
        return

    # 🔄 Khôi phục dữ liệu về trạng thái ban đầu
    df = df_original.copy()
    df_current = df_original.copy()
    current_page = 1  

    # 🛠 Xóa nội dung ô tìm kiếm để đảm bảo reset hoàn toàn
    search_entry.delete(0, tk.END)  

    # 📊 Tính lại số trang sau khi reset
    total_pages = navigation.get_total_pages(df_current, items_per_page)

    # 🔄 Cập nhật lại bảng hiển thị
    updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")

    messagebox.showinfo("Thông báo", "Đã reset tìm kiếm về dữ liệu gốc!")
# def handle_reset_search():
#     """Gọi chức năng reset tìm kiếm từ module `crud.py`"""
#     search.reset_search(tree, page_label, current_page, items_per_page, get_total_pages, update_table_display, search_entry)

def handle_clean_data():
    global df_original, df_current

    if df_original is None or df_original.empty:
        messagebox.showwarning("Warning", "Không có dữ liệu để làm sạch!")
        return

    df_cleaned = crud.clean_data(df_original.copy())  # 🔥 Áp dụng làm sạch dữ liệu
    df_current = df_cleaned.copy()

    updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
    messagebox.showinfo("Success", "Dữ liệu đã được làm sạch thành công!")

def handle_navigate_page(action_type):
    global current_page, df_current  # Đảm bảo đang dùng dữ liệu hiện tại, không quay về df gốc

    if df_current is None or df_current.empty: 
        return  # Không làm gì nếu chưa có dữ liệu

    # Gọi điều hướng trên dữ liệu hiện tại
    new_page = navigation.handle_page_navigation(df_current, current_page, items_per_page, action_type)  
    
    if new_page != current_page:  # Chỉ cập nhật nếu trang thay đổi
        current_page = new_page
        updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
        
        
        total_pages_filtered = navigation.get_total_pages(df_current, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages_filtered}") 


# def handle_navigate_page(action_type):
#     global current_page, df_current  # 🔥 Đảm bảo `df_current` được cập nhật đúng

#     if df_current is None or df_current.empty:
#         messagebox.showerror("Lỗi", "Không có dữ liệu để điều hướng!")
#         return

#     current_page = navigation.navigate_page(action_type, tree, page_label, items_per_page, update_table_display, get_total_pages, navigation.handle_page_navigation)

#     df_current = navigation.paginate_data(df_current, current_page, items_per_page)  # 🔥 Cập nhật dữ liệu theo trang mới

#     updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)  # 🔥 Hiển thị dữ liệu mới ngay

# Nút lọc dữ liệu
def handle_filter_click():
    global df_original
    if df_original is None or df_original.empty:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return

    # Truyền root và df_original vào hàm lọc để app_logic có thể dùng
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

btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10, command=handle_add_data)
btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10, command=handle_update_data)
btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=handle_delete_data)
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