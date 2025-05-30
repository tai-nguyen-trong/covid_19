# from numpy import sort
# import pandas as pd
# import tkinter as tk
# from modules import updateTable

# df_current = None
# ascending_order = {}

# def sort_column(col, tree, page_label, current_page, items_per_page, get_total_pages, update_table_display):
#     """Hàm sắp xếp cột tăng hoặc giảm dần khi nhấp vào tiêu đề."""
#     global df_current, ascending_order  

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
#     tree.heading(col, text=f"{col} {icon}", command=lambda _col=col: sort_column(_col, tree, page_label, current_page, items_per_page, get_total_pages, update_table_display))

#     # 🔥 Tính lại số trang sau khi sắp xếp
#     total_pages = get_total_pages(df_current, items_per_page)
#     current_page = min(current_page, total_pages)

#     # Cập nhật lại bảng hiển thị theo dữ liệu đã lọc
#     updateTable.update_table_display(tree, page_label, df_current, current_page, items_per_page)
#     page_label.config(text=f"Trang {current_page}/{total_pages}")


# def setup_treeview(tree):
#     """Cấu hình Treeview với các cột dữ liệu."""
#     global df_current, ascending_order  

#     if df_current is None or df_current.empty:
#         return  

#     headers = list(df_current.columns)
#     tree["columns"] = headers
#     tree["show"] = "headings"

#     # Khởi tạo trạng thái sắp xếp của mỗi cột
#     for col in headers:
#         ascending_order[col] = False  # ✅ Đặt mặc định là giảm dần
#         tree.heading(col, text=f"{col} ▼", command=lambda _col=col: sort.sort_column(_col, tree))
#         tree.column(col, width=120, anchor="center", stretch=tk.YES)