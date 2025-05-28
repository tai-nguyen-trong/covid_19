import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import math
from tkinter import filedialog

# ======================= CRUD FUNCTIONS =======================
def read_data(file_path):
    """Đọc dữ liệu từ file CSV và trả về DataFrame."""
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error reading CSV: {e}") 
        return None
    
def add_record(df, new_record: dict):
    return df.append(new_record, ignore_index=True)

def update_record(df, index: int, updated_record: dict):
    if 0 <= index < len(df):
        for key, value in updated_record.items():
            df.at[index, key] = value
    return df

def delete_record(df, index):
    if 0 <= index < len(df):
        df.drop(index, inplace=True)
        df.reset_index(drop=True, inplace=True)
    return df

def search_record(df, query):
    query = query.lower()
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)
    return df[mask]

def sort_record(df, column, ascending=True):
    if column in df.columns:
        return df.sort_values(by=column, ascending=ascending).reset_index(drop=True)
    return df

def paginate_data(df, page_number, items_per_page):
    """Phân trang dữ liệu."""
    if df is None or df.empty:
        return pd.DataFrame() # Trả về DataFrame rỗng nếu không có dữ liệu

    start_index = (page_number - 1) * items_per_page
    end_index = start_index + items_per_page
    return df.iloc[start_index:end_index]

def get_total_pages(df, items_per_page):
    """Tính tổng số trang dựa trên DataFrame và số mục trên mỗi trang."""
    if df is None or df.empty:
        return 1 # Trả về 1 trang nếu không có dữ liệu
    total_items = len(df)
    return math.ceil(total_items / items_per_page)

# ======================= GLOBAL VARIABLES =======================
current_df = pd.DataFrame()  # DataFrame hiện tại
filtered_df = pd.DataFrame()  # DataFrame đã lọc

# ======================= FILE thực hiện load =======================
# def load_csv_file():
#     """Hàm đọc file CSV và hiển thị lên Treeview"""
#     global current_df, filtered_df
    

    
#     # Mở dialog chọn file
#     file_path = filedialog.askopenfilename(
#         title="Chọn file CSV",
#         filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
#     )
    
#     if file_path:  # Nếu user chọn file
#         try:
#             # Đọc file CSV
#             df = read_data(file_path)
            
#             if df is not None:
#                 current_df = df
#                 filtered_df = df.copy()

#                 # Lấy tên cột từ DataFrame
#                 headers = list(df.columns)
 
#                 # Xóa dữ liệu cũ trong Treeview
#                 for item in tree.get_children():
#                     tree.delete(item)
                
#                 # thêm dữ liệu header vào 
#                 tree["columns"] = headers
#                 tree["show"] = "headings"

#                 for col in headers:
#                     tree.heading(col, text=col) 
#                     tree.column(col, width=100)

#                 # Thêm dữ liệu mới vào Treeview
#                 for index, row in df.iterrows():
#                     tree.insert("", "end", values=list(row))

                
#                 messagebox.showinfo("Thành công", f"Đã tải {len(df)} bản ghi từ file {file_path}")
                
#             else:
#                 messagebox.showerror("Lỗi", "Không thể đọc file CSV!")
                
#         except Exception as e:
#             messagebox.showerror("Lỗi", f"Lỗi khi đọc file: {str(e)}")

# # ======================= GUI SETUP =======================
# root = tk.Tk()
# root.title("Phân tích dữ liệu COVID-19")
# root.geometry("1000x600")
# root.resizable(False, False)

# # ======================= LOAD FILE BUTTON =======================
# file_frame = tk.Frame(root)
# file_frame.pack(fill="x", anchor="w",pady=10)

# btn_load_file = tk.Button(file_frame, text="Tải File CSV", command=load_csv_file, 
#                          bg="lightgreen", width=15, font=("Arial", 10))
# btn_load_file.pack(side="left", padx =5)

# # ======================= TREEVIEW (TABLE) bỏ vì sẽ hiện các header từ bảng của file =======================
# # columns = ("ID", "Name", "Platform", "Year", "Genre", "Publisher", "NA Sales", "EU Sales", "JP Sales", "Other Sales", "Global Sales")
# # tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
# tree = ttk.Treeview(root)
# tree.pack(fill="both", expand=True)
# # for col in columns:
# #     tree.heading(col, text=col)
# #     tree.column(col, width=90, anchor="center")

# # tree.pack(pady=10)

# # # Dummy data (thêm vài dòng mẫu)
# # sample_data = [

# # ]
# # for row in sample_data:
# #     tree.insert("", "end", values=row)

# # ======================= CONTROL BUTTONS =======================
# button_frame = tk.Frame(root)
# button_frame.pack(pady=10)

# btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10)
# btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10)
# btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10)
# btn_reset = tk.Button(button_frame, text="Reset", bg="gray", width=10)
# btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10)

# btn_create.grid(row=0, column=0, padx=5)
# btn_update.grid(row=0, column=1, padx=5)
# btn_delete.grid(row=0, column=2, padx=5)
# btn_reset.grid(row=0, column=3, padx=5)
# btn_export.grid(row=0, column=4, padx=5)

# # ======================= SEARCH BAR =======================
# search_frame = tk.Frame(root)
# search_frame.pack(pady=10)

# tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
# search_entry = tk.Entry(search_frame)
# search_entry.grid(row=0, column=1, padx=5)
# search_btn = tk.Button(search_frame, text="Search", width=10)
# search_btn.grid(row=0, column=2, padx=5)

# # ======================= MESSAGE EXAMPLE =======================
# def show_info():
#     messagebox.showinfo("Info", "No item selected!")

# msg_btn = tk.Button(root, text="Test Popup", command=show_info)
# msg_btn.pack(pady=5)

# # ======================= MAIN LOOP =======================
# root.mainloop()







# # ======================= GUI SETUP =======================
# root = tk.Tk()
# root.title("Phân tích dữ liệu COVID-19")
# root.geometry("1000x600")
# # root.resizable(False, False)

# # ======================= LOAD FILE BUTTON =======================
# file_frame = tk.Frame(root)
# file_frame.pack(fill="x", anchor="w", pady=10)

# btn_load_file = tk.Button(file_frame, text="Tải File CSV", command=load_csv_file,
#                           bg="lightgreen", width=15, font=("Arial", 10))
# btn_load_file.pack(side="left", padx=5)

# # ======================= TREEVIEW + SCROLLBAR =======================
# table_frame = tk.Frame(root)
# table_frame.pack(fill="both", expand=True)

# # Scrollbars
# tree_scroll_y = tk.Scrollbar(table_frame, orient="vertical")
# tree_scroll_y.pack(side="right", fill="y")

# tree_scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
# tree_scroll_x.pack(side="bottom", fill="x")

# tree = ttk.Treeview(table_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)
# tree.pack(fill="both", expand=True)

# tree_scroll_y.config(command=tree.yview)
# tree_scroll_x.config(command=tree.xview)

# # ======================= PAGINATION BUTTONS =======================
# pagination_frame = tk.Frame(root)
# pagination_frame.pack(pady=5)

# btn_first = tk.Button(pagination_frame, text="Trang đầu", width=10)
# btn_prev = tk.Button(pagination_frame, text="Trang trước", width=10)
# btn_next = tk.Button(pagination_frame, text="Trang sau", width=10)
# btn_last = tk.Button(pagination_frame, text="Trang cuối", width=10)
# page_label = tk.Label(pagination_frame, text="Trang 1/1", width=12)

# btn_first.grid(row=0, column=0, padx=3)
# btn_prev.grid(row=0, column=1, padx=3)
# btn_next.grid(row=0, column=2, padx=3)
# btn_last.grid(row=0, column=3, padx=3)
# page_label.grid(row=0, column=4, padx=3)

# # ======================= CONTROL BUTTONS =======================
# button_frame = tk.Frame(root)
# button_frame.pack(pady=10)

# btn_create = tk.Button(button_frame, text="Create", bg="orange", width=10)
# btn_update = tk.Button(button_frame, text="Update", bg="lightblue", width=10)
# btn_delete = tk.Button(button_frame, text="Delete", bg="red", fg="white", width=10)
# btn_reset = tk.Button(button_frame, text="Reset", bg="gray", width=10)
# btn_export = tk.Button(button_frame, text="Export", bg="green", fg="white", width=10)

# btn_create.grid(row=0, column=0, padx=5)
# btn_update.grid(row=0, column=1, padx=5)
# btn_delete.grid(row=0, column=2, padx=5)
# btn_reset.grid(row=0, column=3, padx=5)
# btn_export.grid(row=0, column=4, padx=5)

# # ======================= SEARCH BAR =======================
# search_frame = tk.Frame(root)
# search_frame.pack(pady=10)

# tk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5)
# search_entry = tk.Entry(search_frame)
# search_entry.grid(row=0, column=1, padx=5)
# search_btn = tk.Button(search_frame, text="Search", width=10)
# search_btn.grid(row=0, column=2, padx=5)

# # ======================= MESSAGE EXAMPLE =======================
# def show_info():
#     messagebox.showinfo("Info", "No item selected!")

# msg_btn = tk.Button(root, text="Test Popup", command=show_info)
# msg_btn.pack(pady=5)

# # ======================= MAIN LOOP =======================
# root.mainloop()
