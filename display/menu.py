# display/menu.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox # Cần để hiển thị cảnh báo trực tiếp từ menu.py

from modules import app_logic # Chỉ import app_logic
from display.form_dialog import show_form_window
from modules.crud import read_data

# Biến toàn cục cho ứng dụng (QUẢN LÝ DỮ LIỆU TẠI ĐÂY)
df = None # df hiện tại đang hiển thị trên bảng chính (có thể là original hoặc đã lọc trước đó)
df_original = None # Luôn là dữ liệu gốc sau khi tải file
current_page = 1
items_per_page = 20


# ======================= GLOBAL VARIABLES =======================
current_df = pd.DataFrame()  # DataFrame hiện tại
filtered_df = pd.DataFrame()  # DataFrame đã lọc
def load_csv_file():
    """Hàm đọc file CSV và hiển thị lên Treeview"""
    global current_df, filtered_df

########################
    global df, df_original
    
    # Mở dialog chọn file
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if file_path:  # Nếu user chọn file
        try:
            # Đọc file CSV
            df = read_data(file_path)

            
            if df is not None:
                # current_df = df
                # filtered_df = df.copy()
                df_original = df.copy()  # Lưu lại dữ liệu gốc
                current_df = df
                filtered_df = df.copy()



                # Lấy tên cột từ DataFrame
                headers = list(df.columns)
 
                # Xóa dữ liệu cũ trong Treeview
                for item in tree.get_children():
                    tree.delete(item)
                
                # thêm dữ liệu header vào 
                tree["columns"] = headers
                tree["show"] = "headings"

                for col in headers:
                    tree.heading(col, text=col) 
                    tree.column(col, width=100)

                # Thêm dữ liệu mới vào Treeview
                for index, row in df.iterrows():
                    tree.insert("", "end", values=list(row))

                
                messagebox.showinfo("Thành công", f"Đã tải {len(df)} bản ghi từ file {file_path}")
                
            else:
                messagebox.showerror("Lỗi", "Không thể đọc file CSV!")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file: {str(e)}")

# def handle_open_file():
#     global df, df_original, current_page
#     # app_logic.open_file_action sẽ trả về DataFrame đã đọc
#     new_df_read = app_logic.open_file_action()
#     print("Tat Ca Data trong csv:", new_df_read)
#     if new_df_read is not None:
#         df_original = new_df_read.copy() # Cập nhật df_original của menu.py
#         df = new_df_read.copy() # Bảng chính hiển thị dữ liệu gốc ban đầu
        
#         # Cấu hình cột Treeview sau khi có df
#         for row in table.get_children():
#             table.delete(row)
#         table["columns"] = list(df.columns)
#         for col_name in df.columns:
#             table.heading(col_name, text=col_name)
#             table.column(col_name, width=120, anchor="center", stretch=tk.YES)
#         table.column("#0", width=0, stretch=tk.NO) # Ẩn cột ID mặc định

#         current_page = 1 # Về trang đầu sau khi tải
#         app_logic.update_table_display(table, page_label, df, current_page, items_per_page)

def handle_add_data():
    def on_submit(new_data):
        global df, df_original

        # 🔁 Đọc lại dữ liệu từ file để đảm bảo không bị mất dữ liệu cũ
        df = read_data("dataset/country_wise_latest.csv")
        if df is None:
            df = pd.DataFrame()  # Nếu file chưa tồn tại

        # ➕ Thêm dòng mới
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df, new_row], ignore_index=True)
        df_original = df.copy()

        # Ghi lại vào file CSV
        df.to_csv("dataset/country_wise_latest.csv", index=False)

        # Cập nhật bảng
        app_logic.update_table_display(tree, page_label, df, current_page, items_per_page)

    show_form_window(root, data=None, on_submit=on_submit)

def handle_update_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
        return

    global df, df_original

    index = tree.index(selected[0]) + (current_page - 1) * items_per_page

    # Kiểm tra chỉ mục hợp lệ
    if index >= len(df):
        messagebox.showerror("Lỗi", "Chỉ mục cập nhật vượt quá kích thước dữ liệu!")
        return

    current_data = df.iloc[index].to_dict()

    def on_submit(updated_data):
        global df, df_original
        try:
            for key in updated_data:
                if key in df.columns:  # Kiểm tra nếu key tồn tại trong DataFrame
                    if df[key].dtype in ["int64", "float64"]:  # Kiểm tra nếu cột yêu cầu số
                        try:
                            updated_data[key] = float(updated_data[key])  # Chuyển đổi thành số
                        except ValueError:
                            messagebox.showerror("Lỗi", f"Giá trị '{updated_data[key]}' không hợp lệ cho cột {key}. Vui lòng nhập số.")
                            return
                    
                    df.at[index, key] = updated_data[key]  # Cập nhật dữ liệu
            df_original = df.copy()
            df.to_csv("dataset/country_wise_latest.csv", index=False)
            app_logic.update_table_display(tree, page_label, df, current_page, items_per_page)
            messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi cập nhật dữ liệu: {str(e)}")

    show_form_window(root, data=current_data, on_submit=on_submit)

def handle_delete_data():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn ít nhất một dòng để xóa.")
        return

    if not messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa các dòng đã chọn?"):
        return

    global df, df_original

    # Lấy chỉ mục chính xác của dòng cần xóa
    indexes_to_delete = [tree.index(item) + (current_page - 1) * items_per_page for item in selected]

    # Kiểm tra chỉ mục hợp lệ
    valid_indexes = [i for i in indexes_to_delete if i < len(df)]

    if not valid_indexes:
        messagebox.showerror("Lỗi", "Không có chỉ mục hợp lệ để xóa!")
        return

    # Xóa các dòng hợp lệ
    df = df.drop(df.index[valid_indexes]).reset_index(drop=True)
    df_original = df.copy()

    # Lưu lại dữ liệu
    df.to_csv("dataset/country_wise_latest.csv", index=False)

    # Cập nhật giao diện
    app_logic.update_table_display(tree, page_label, df, current_page, items_per_page)

    messagebox.showinfo("Thành công", "Đã xóa thành công các dòng đã chọn.")

def sort_column(col):
    global df, df_original
    df = df.sort_values(by=col, ascending=True if not hasattr(sort_column, "desc") or sort_column.desc else False)
    sort_column.desc = not getattr(sort_column, "desc", False)
    df_original = df.copy()
    app_logic.update_table_display(tree, page_label, df, current_page, items_per_page)


def handle_search_data(keyword):
    global df_original
    if not keyword:
        return
    keyword = keyword.lower()
    
    # Cải thiện hiệu suất tìm kiếm
    df_filtered = df_original[df_original.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]

    # Hiển thị kết quả nhưng không ghi đè lên df
    app_logic.update_table_display(tree, page_label, df_filtered, 1, items_per_page)

    search_btn.config(command=lambda: handle_search_data(search_entry.get()))

def reset_search():
    global df
    df = df_original.copy()
    app_logic.update_table_display(tree, page_label, df, 1, items_per_page)

#========================= CHART FUNCTIONS =========================
def draw_chart1(df):
    plt.figure(figsize=(8, 5))
    top_confirmed = df.sort_values("Confirmed", ascending=False).head(10)
    plt.bar(top_confirmed["Country/Region"], top_confirmed["Confirmed"], color='orange')
    plt.title("Top 10 quốc gia có số ca nhiễm COVID-19 cao nhất")
    plt.ylabel("Số ca nhiễm")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart2(df):
    plt.figure(figsize=(8, 5))
    top_deaths = df.sort_values("Deaths", ascending=False).head(10)
    plt.bar(top_deaths["Country/Region"], top_deaths["Deaths"], color='red')
    plt.title("Top 10 quốc gia có số ca tử vong cao nhất")
    plt.ylabel("Số ca tử vong")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart3(df):
    plt.figure(figsize=(8, 5))
    region_deaths = df.groupby("WHO Region")["Deaths"].sum()
    plt.pie(region_deaths, labels=region_deaths.index, autopct='%1.1f%%', startangle=140)
    plt.title("Tỷ lệ tử vong theo khu vực WHO")
    plt.show()

def draw_chart4(df):
    plt.figure(figsize=(8, 5))
    top_growth = df.sort_values("1 week % increase", ascending=False).head(10)
    plt.bar(top_growth["Country/Region"], top_growth["1 week % increase"], color='purple')
    plt.title("Top 10 quốc gia có tỷ lệ tăng trưởng ca nhiễm trong 1 tuần cao nhất")
    plt.ylabel("Tỷ lệ tăng trưởng (%)")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart5(df):
    plt.figure(figsize=(8, 5))
    top_recovered_ratio = df.sort_values("Recovered / 100 Cases", ascending=False).head(10)
    plt.bar(top_recovered_ratio["Country/Region"], top_recovered_ratio["Recovered / 100 Cases"], color='green')
    plt.title("Top 10 quốc gia có tỷ lệ hồi phục cao nhất")
    plt.ylabel("Tỷ lệ hồi phục trên 100 ca (%)")
    plt.xticks(rotation=45)
    plt.show()

# Hàm mở cửa sổ chứa các nút chọn biểu đồ
def open_chart_window():
    chart_window = tk.Toplevel(root)
    chart_window.title("Chọn biểu đồ")
    chart_window.geometry("300x300")
    chart_window.grab_set()

    # Nạp dữ liệu từ tệp CSV
    df = pd.read_csv("dataset/country_wise_latest.csv")

    # Các nút để chọn biểu đồ
    tk.Button(chart_window, text="Ca nhiễm nhiều nhất", command=lambda: draw_chart1(df)).pack(pady=5)
    tk.Button(chart_window, text="Tử vong cao nhất", command=lambda: draw_chart2(df)).pack(pady=5)
    tk.Button(chart_window, text="Tỷ lệ tử vong theo WHO", command=lambda: draw_chart3(df)).pack(pady=5)
    tk.Button(chart_window, text="Tăng trưởng ca nhiễm", command=lambda: draw_chart4(df)).pack(pady=5)
    tk.Button(chart_window, text="Tỷ lệ hồi phục", command=lambda: draw_chart5(df)).pack(pady=5)


# Hàm xử lý điều hướng trang (gọi app_logic.handle_page_navigation)
def navigate_page(action_type):
    global current_page
    if df is None: return # Không làm gì nếu chưa có dữ liệu

    # app_logic.handle_page_navigation sẽ trả về số trang mới
    new_page = app_logic.handle_page_navigation(df, current_page, items_per_page, action_type)
    
    if new_page != current_page: # Chỉ cập nhật và hiển thị nếu trang thay đổi
        current_page = new_page
        app_logic.update_table_display(tree, page_label, df, current_page, items_per_page)

# Nút lọc dữ liệu
def handle_filter_click():
    if df_original is None:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return
    # Truyền root và df_original vào hàm lọc để app_logic có thể dùng
    app_logic.show_filter_window(root, df_original)

# ======================= GUI SETUP =======================
# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("COVID-19 Data Analysis")
root.geometry("1000x700")
# root.resizable(False, False)

# ======================= LOAD FILE BUTTON =======================
file_frame = tk.Frame(root)
file_frame.pack(fill="x", anchor="w", pady=10)

btn_load_file = tk.Button(file_frame, text="Tải File CSV", command=load_csv_file,
                          bg="lightgreen", width=15, font=("Arial", 10))
btn_load_file.pack(side="left", padx=5)

# # Tạo menu bar
# menu_bar = tk.Menu(root)
# file_menu = tk.Menu(menu_bar, tearoff=0)

# file_menu.add_command(label="Open File", command=handle_open_file)
# file_menu.add_command(label="Exit", command=root.quit)
# menu_bar.add_cascade(label="File", menu=file_menu)
# root.config(menu=menu_bar)

# # Cấu hình grid cho cửa sổ chính
# root.grid_columnconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=3) # Hàng chứa bảng
# root.grid_rowconfigure(2, weight=1) # Hàng chứa nút phân trang
# root.grid_rowconfigure(3, weight=1) # Hàng chứa nút lọc




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
# # Tạo Frame để chứa Treeview và Scrollbar
# table_frame = tk.Frame(root)
# table_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# table_frame.grid_columnconfigure(0, weight=1)
# table_frame.grid_rowconfigure(0, weight=1)

# # Tạo Scrollbar dọc
# v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
# v_scrollbar.grid(row=0, column=1, sticky="ns")

# # Tạo Scrollbar ngang
# h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal")
# h_scrollbar.grid(row=1, column=0, sticky="ew")

# # Tạo Treeview bên trong table_frame và liên kết với scrollbars
# table = ttk.Treeview(table_frame, show="headings",
#                      yscrollcommand=v_scrollbar.set,
#                      xscrollcommand=h_scrollbar.set)
# table.grid(row=0, column=0, sticky="nsew")

# v_scrollbar.config(command=table.yview)
# h_scrollbar.config(command=table.xview)


# ======================= PAGINATION BUTTONS =======================
pagination_frame = tk.Frame(root)
pagination_frame.pack(pady=5)

btn_first = tk.Button(pagination_frame, text="Trang đầu", width=10, command=lambda: navigate_page("first"))
btn_prev = tk.Button(pagination_frame, text="Trang trước", width=10, command=lambda: navigate_page("prev"))
btn_next = tk.Button(pagination_frame, text="Trang sau", width=10, command=lambda: navigate_page("next"))
btn_last = tk.Button(pagination_frame, text="Trang cuối", width=10, command=lambda: navigate_page("last"))
page_label = tk.Label(pagination_frame, text="Trang 1/2", width=12)

btn_first.grid(row=0, column=0, padx=3)
btn_prev.grid(row=0, column=1, padx=3)
btn_next.grid(row=0, column=2, padx=3)
btn_last.grid(row=0, column=3, padx=3)
page_label.grid(row=0, column=4, padx=3)

# # Nút điều hướng phân trang
# first_page_button = tk.Button(root, text="Trang đầu", command=lambda: navigate_page("first"))
# first_page_button.grid(row=2, column=0, padx=5, pady=5)

# prev_page_button = tk.Button(root, text="Trang trước", command=lambda: navigate_page("prev"))
# prev_page_button.grid(row=2, column=1, padx=5, pady=5)

# next_page_button = tk.Button(root, text="Trang sau", command=lambda: navigate_page("next"))
# next_page_button.grid(row=2, column=2, padx=5, pady=5)

# last_page_button = tk.Button(root, text="Trang cuối", command=lambda: navigate_page("last"))
# last_page_button.grid(row=2, column=3, padx=5, pady=5)

# page_label = tk.Label(root, text="Trang -/-")
# page_label.grid(row=2, column=4, padx=5, pady=5)



# ======================= CONTROL BUTTONS =======================
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10, command=handle_add_data)
btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10, command=handle_update_data)
btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=handle_delete_data)
btn_reset = tk.Button(button_frame, text="Reset", bg="gray", width=10)
btn_chart = tk.Button(button_frame, text="Charts", bg="purple", fg="white", width=10, command=open_chart_window)
btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10)

btn_create.grid(row=0, column=0, padx=5)
btn_update.grid(row=0, column=1, padx=5)
btn_delete.grid(row=0, column=2, padx=5)
btn_reset.grid(row=0, column=3, padx=5)
btn_chart.grid(row=0, column=4, padx=5)
btn_export.grid(row=0, column=5, padx=5)
# filter_button = tk.Button(root, text="Lọc dữ liệu", command=handle_filter_click)
# filter_button.grid(row=3, column=0, columnspan=5, padx=10, pady=10)



# add_button = tk.Button(root, text="Thêm dữ liệu", command=handle_add_data)
# add_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# edit_button = tk.Button(root, text="Sửa dòng đã chọn", command=handle_edit_data)
# edit_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")


# ======================= SEARCH BAR =======================
# search_var = tk.StringVar()
# search_entry = tk.Entry(button_frame, textvariable=search_var, width=30)
# search_entry.pack(side="left", padx=5)

# btn_search = tk.Button(button_frame, text="Tìm kiếm", command=lambda: handle_search_data(search_var.get()))
# btn_search.pack(side="left", padx=5)

# btn_reset = tk.Button(button_frame, text="Reset", command=lambda: reset_search())
# btn_reset.pack(side="left", padx=5)

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame)
search_entry.grid(row=0, column=1, padx=5)
search_btn = tk.Button(search_frame, text="Search", width=10)
search_btn.grid(row=0, column=2, padx=5)

# Liên kết sự kiện nhấn nút với hàm tìm kiếm
search_btn.config(command=lambda: handle_search_data(search_entry.get()))

# ======================= MESSAGE EXAMPLE =======================
def show_info():
    messagebox.showinfo("Info", "No item selected!")

msg_btn = tk.Button(root, text="Test Popup", command=show_info)
msg_btn.pack(pady=5)

# --- KHỞI TẠO LOGIC ỨNG DỤNG ---
# app_logic không còn cần các biến toàn cục nữa.
app_logic.init_logic()

# Chạy giao diện Tkinter
root.mainloop()