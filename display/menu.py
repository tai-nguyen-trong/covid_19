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
from modules.crud import get_total_pages, read_data
from modules.filters import show_filter_window
from modules.navigation import handle_page_navigation

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

def load_csv_file():
    """Hàm đọc file CSV và hiển thị lên Treeview"""
    # global current_df, filtered_df, df, df_original, current_page
    global df_original, df_current, current_page

    # Mở dialog chọn file
    file_path = filedialog.askopenfilename(
        title="Chọn file CSV",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )

    if file_path:
        try:
            df = read_data(file_path)

            if df is None or df.empty:
                messagebox.showerror("Lỗi", "Không thể đọc file CSV hoặc file không có dữ liệu!")
                return

            # # Lưu dữ liệu gốc
            # df_original = df.copy()
            # current_df = df
            # filtered_df = df.copy()
            df_original = pd.read_csv(file_path)  # Đọc file CSV
            df_current = df_original.copy()  # Cập nhật dữ liệu hiện tại để điều hướng đúng
            current_page = 1  # Reset về trang đầu tiên


            # Xóa dữ liệu cũ trong Treeview
            for item in tree.get_children():
                tree.delete(item)

            # # Cấu hình cột của Treeview
            # headers = list(df.columns)
            # tree["columns"] = headers
            # tree["show"] = "headings"

            # for col in headers:
            #     tree.heading(col, text=col)
            #     tree.column(col, width=120, anchor="center", stretch=tk.YES)
            # tree.column("#0", width=0, stretch=tk.NO)  # Ẩn cột ID mặc định
             # ======================= TREEVIEW COLUMNS (Đặt đúng vị trí) =======================
            headers = list(df.columns)
            tree["columns"] = headers
            tree["show"] = "headings"


            for col in headers:
                tree.heading(col, text=f"▲ {col} ▼", command=lambda _col=col: sort_column(_col))
                tree.column(col, width=120, anchor="center", stretch=tk.YES)



            

            # Thêm dữ liệu mới vào Treeview
            for _, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            messagebox.showinfo("Thành công", f"Đã tải {len(df)} bản ghi từ file {file_path}")

            # current_page = 1
            # crud.update_table_display(tree, page_label, df, current_page, items_per_page)
            total_pages = get_total_pages(df_current, items_per_page)  # Tính số trang

            crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)  
            page_label.config(text=f"Trang {current_page}/{total_pages}")  # Hiển thị số trang đúng
        

            # Hiển thị phần khung chức năng và nút chức năng
            pagination_frame.pack(pady=5)
            button_frame.pack(pady=10)
            # search_frame.pack(pady=10)
            search_frame.grid(row=0, column=1, padx=20, sticky="e")

            for j, btnChuyenHuong in enumerate(function_buttons2):
                btnChuyenHuong.grid(row=0, column=j, padx=3) 

            for i, btn in enumerate(function_buttons):
                btn.grid(row=0, column=i, padx=5) 

        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi đọc file CSV: {str(e)}")

def handle_add_data():
    def on_submit(new_data):
        # global df, df_original
        global df, df_original, df_current, current_page 

        # 🔁 Đọc lại dữ liệu từ file để đảm bảo không bị mất dữ liệu cũ
        try:
            df_existing = pd.read_csv("dataset/country_wise_latest.csv")  
        except FileNotFoundError:
            df_existing = pd.DataFrame()  # Nếu file chưa tồn tại, tạo DataFrame rỗng

        # 🔁 Chuyển các trường rỗng thành NaN ngay lúc thêm dữ liệu
        new_data = {key: (val if val.strip() != "" else np.nan) for key, val in new_data.items()}



        # ➕ Thêm dòng mới vào dữ liệu hiện tại
        new_row = pd.DataFrame([new_data])
        df = pd.concat([df_existing, new_row], ignore_index=True)  # Giữ lại dữ liệu cũ và thêm mới
        df_original = df.copy()
        df_current = df.copy() 

        # Ghi lại vào file CSV
        df.to_csv("dataset/country_wise_latest.csv", index=False)

        # Cập nhật số trang sau khi thêm dữ liệu
        total_pages = get_total_pages(df_current, items_per_page)
        # current_page = 1  # Đặt về trang đầu tiên sau khi thêm dữ liệu
        current_page = total_pages  # Đặt về trang cuối sau khi thêm dữ liệu



        # Cập nhật bảng
        crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages}")  # Hiển thị số trang đúng

        # crud.update_table_display(tree, page_label, df, current_page, items_per_page)
        messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công.")

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
            crud.update_table_display(tree, page_label, df, current_page, items_per_page)
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
    crud.update_table_display(tree, page_label, df, current_page, items_per_page)

    messagebox.showinfo("Thành công", "Đã xóa thành công các dòng đã chọn.")

def sort_column(col):
    """Hàm sắp xếp cột tăng hoặc giảm dần khi nhấp vào tiêu đề"""
    global df_current, ascending_order  

    if df_current is None or df_current.empty:
        return  

    # Kiểm tra trạng thái sắp xếp ban đầu
    if col not in ascending_order:
        ascending_order[col] = True  

    # Đảo trạng thái sắp xếp mỗi lần nhấn
    ascending_order[col] = not ascending_order[col]

    # Sắp xếp dữ liệu hiện tại thay vì dữ liệu gốc
    df_current = df_current.sort_values(by=col, ascending=ascending_order[col])

    # Cập nhật tiêu đề **chỉ trên cột được nhấn**
    up_icon = "▲" if ascending_order[col] else "▲"
    down_icon = "▼" if not ascending_order[col] else "▼"
    tree.heading(col, text=f"{up_icon} {col} {down_icon}", command=lambda _col=col: sort_column(_col))

    # Cập nhật lại bảng hiển thị theo dữ liệu đã lọc
    crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)
def setup_treeview():
    headers = list(df.columns)
    tree["columns"] = headers
    tree["show"] = "headings"

    # Khởi tạo trạng thái sắp xếp của mỗi cột (None khi chưa có sắp xếp)
    for col in headers:
        ascending_order[col] = None  
        tree.heading(col, text=f"▲ {col} ▼", command=lambda _col=col: sort_column(_col))
        tree.column(col, width=120, anchor="center", stretch=tk.YES)



def handle_search_data(keyword):
    global df_original, df_current, current_page  # Thêm biến lưu trạng thái dữ liệu hiện tại

    if not keyword:
        return
    keyword = keyword.lower()

    # Lọc dữ liệu
    df_filtered = df_original[df_original.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]

    if df_filtered.empty:
        messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp!")
        return

    df_current = df_filtered  # Cập nhật dữ liệu hiện tại để phân trang đúng
    current_page = 1  # Đặt trang đầu tiên khi tìm kiếm mới
    total_pages_filtered = get_total_pages(df_current, items_per_page)



    # Hiển thị kết quả với số trang mới
    crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)

    page_label.config(text=f"Trang {current_page}/{total_pages_filtered}")
# def handle_search_data(keyword):
#     global df_original
#     if not keyword:
#         return
#     keyword = keyword.lower()
    
#     # Cải thiện hiệu suất tìm kiếm
#     df_filtered = df_original[df_original.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]

#     # Hiển thị kết quả nhưng không ghi đè lên df
#     crud.update_table_display(tree, page_label, df_filtered, 1, items_per_page, keyword)

#     search_btn.config(command=lambda: handle_search_data(search_entry.get()))

# def reset_search():
#     global df
#     df = df_original.copy()
#     search_entry.delete(0, tk.END)  # Xóa nội dung trong ô nhập tìm kiếm
#     crud.update_table_display(tree, page_label, df, 1, items_per_page)
def reset_search():
    global df, df_current, current_page  # Đảm bảo cập nhật biến đúng

    df = df_original.copy()
    df_current = df_original.copy()  # Cập nhật dữ liệu hiện tại để phân trang chính xác
    current_page = 1  # Reset về trang đầu tiên

    search_entry.delete(0, tk.END)  # Xóa nội dung trong ô nhập tìm kiếm
    total_pages = get_total_pages(df_current, items_per_page)  # Tính số trang theo dataset gốc

    crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")  # Hiển thị số trang đúng

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


# # Hàm xử lý điều hướng trang
# def navigate_page(action_type):
#     global current_page
#     if df is None: return # Không làm gì nếu chưa có dữ liệu

#     # app_logic.handle_page_navigation sẽ trả về số trang mới
#     new_page = handle_page_navigation(df, current_page, items_per_page, action_type)
    
#     if new_page != current_page: # Chỉ cập nhật và hiển thị nếu trang thay đổi
#         current_page = new_page
#         crud.update_table_display(tree, page_label, df, current_page, items_per_page)
def navigate_page(action_type):
    global current_page, df_current  # Đảm bảo đang dùng dữ liệu hiện tại, không quay về df gốc

    if df_current is None or df_current.empty: 
        return  # Không làm gì nếu chưa có dữ liệu

    # Gọi điều hướng trên dữ liệu hiện tại
    new_page = handle_page_navigation(df_current, current_page, items_per_page, action_type)  
    
    if new_page != current_page:  # Chỉ cập nhật nếu trang thay đổi
        current_page = new_page
        crud.update_table_display(tree, page_label, df_current, current_page, items_per_page)
        
        
        total_pages_filtered = get_total_pages(df_current, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages_filtered}")  

# Nút lọc dữ liệu
def handle_filter_click():
    if df_original is None:
        messagebox.showwarning("Warning", "Chưa tải dữ liệu để lọc!")
        return
    # Truyền root và df_original vào hàm lọc để app_logic có thể dùng
    show_filter_window(root, df_original)

# ======================= GUI SETUP =======================
# Khởi tạo cửa sổ chính
root = tk.Tk()
root.title("COVID-19 Data Analysis")
root.geometry("1000x700")
# Mở rộng cửa sổ nhưng vẫn giữ thanh tiêu đề và nút điều khiển
root.state("zoomed")  # Sử dụng `zoomed` thay vì `fullscreen`

# root.resizable(False, False)

# ======================= LOAD FILE BUTTON =======================
file_frame = tk.Frame(root)
file_frame.pack(fill="x", anchor="w", pady=10)

btn_load_file = tk.Button(file_frame, text="Tải File CSV", command=load_csv_file,
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

btn_first = tk.Button(pagination_frame, text="Trang đầu", width=10, command=lambda: navigate_page("first"))
btn_prev = tk.Button(pagination_frame, text="Trang trước", width=10, command=lambda: navigate_page("prev"))
btn_next = tk.Button(pagination_frame, text="Trang sau", width=10, command=lambda: navigate_page("next"))
btn_last = tk.Button(pagination_frame, text="Trang cuối", width=10, command=lambda: navigate_page("last"))
page_label = tk.Label(pagination_frame, text="Trang", width=12)

# btn_first.grid(row=0, column=0, padx=3)
# btn_prev.grid(row=0, column=1, padx=3)
# btn_next.grid(row=0, column=2, padx=3)
# btn_last.grid(row=0, column=3, padx=3)
# page_label.grid(row=0, column=4, padx=3)

# ======================= CONTROL BUTTONS =======================
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10, command=handle_add_data)
btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10, command=handle_update_data)
btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10, command=handle_delete_data)
btn_reset = tk.Button(button_frame, text="Reset", bg="lightgray", width=10, command=reset_search)
btn_chart = tk.Button(button_frame, text="Charts", bg="purple", fg="white", width=10, command=open_chart_window)
btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10)

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
function_buttons2 = [btn_first, btn_prev, btn_next, btn_last, page_label]
for btn in function_buttons:
    btn.grid_remove()

for btnChuyenHuong in function_buttons2:
    btnChuyenHuong.grid_remove()

pagination_frame.pack_forget()
button_frame.pack_forget()
# search_frame.pack_forget()
search_frame.grid_remove()  # Ẩn search_frame




root.mainloop()