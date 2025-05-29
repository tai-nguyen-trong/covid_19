
# Điều hướng phân trang
from tkinter import messagebox
from modules import crud


# def handle_page_navigation(df_current, current_page_num, items_per_pg, action_type):
#     """
#     Xử lý điều hướng trang.
#     Trả về số trang mới.
#     """
#     if df_current is None: return current_page_num # Không làm gì nếu df rỗng

#     total_pages = crud.get_total_pages(df_current, items_per_pg)
#     new_page = current_page_num

#     if action_type == "next":
#         if current_page_num < total_pages:
#             new_page += 1
#         else:
#             messagebox.showinfo("Thông báo", "Đây là trang cuối cùng.")
#     elif action_type == "prev":
#         if current_page_num > 1:
#             new_page -= 1
#         else:
#             messagebox.showinfo("Thông báo", "Đây là trang đầu tiên.")
#     elif action_type == "first":
#         new_page = 1
#     elif action_type == "last":
#         new_page = total_pages
    
#     return new_page
def handle_page_navigation(df_current, current_page_num, items_per_pg, action_type):
    """Xử lý điều hướng trang với dữ liệu hiện tại."""
    if df_current is None or df_current.empty:
        return current_page_num

    total_pages = crud.get_total_pages(df_current, items_per_pg)  # Lấy số trang từ dữ liệu hiện tại

    # # Điều hướng trang
    # if action_type == "next" and current_page_num < total_pages:
    #     current_page_num += 1
    # elif action_type == "prev" and current_page_num > 1:
    #     current_page_num -= 1
    # elif action_type == "first":
    #     current_page_num = 1
    # elif action_type == "last":
    #     current_page_num = total_pages
    if action_type == "next":
        if current_page_num < total_pages:
            current_page_num += 1
        else:
            messagebox.showinfo("Thông báo", "Bạn đang ở trang cuối cùng!")  # Thông báo khi cố bấm tiếp
    elif action_type == "prev":
        if current_page_num > 1:
            current_page_num -= 1
        else:
            messagebox.showinfo("Thông báo", "Bạn đang ở trang đầu tiên!")  # Thông báo khi cố quay lại trước
    elif action_type == "first":
        current_page_num = 1
    elif action_type == "last":
        current_page_num = total_pages

    return current_page_num  # Trả về số trang mới