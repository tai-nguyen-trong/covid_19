# modules/search.py
import pandas as pd
from tkinter import messagebox
from modules.navigation import get_total_pages
from modules.updateTable import update_table_display

def handle_search_data(keyword, df_original, df_current, current_page, items_per_page, tree, page_label):
    """Hàm tìm kiếm dữ liệu theo tên nước"""
    if not keyword or df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Dữ liệu gốc không hợp lệ hoặc từ khóa tìm kiếm trống!")
        return df_current, current_page

    keyword = keyword.lower().strip()

    # Tìm cột chứa tên nước (thử các tên cột phổ biến)
    country_columns = []
    for col in df_original.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['country', 'nation', 'region']):
            country_columns.append(col)
    
    # Nếu không tìm thấy cột nước, tìm kiếm trong tất cả cột
    if not country_columns:
        df_filtered = df_original[df_original.astype(str).apply(
            lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)]
    else:
        # Tìm kiếm ưu tiên trong cột tên nước
        mask = pd.Series([False] * len(df_original))
        for col in country_columns:
            mask |= df_original[col].astype(str).str.contains(keyword, case=False, na=False)
        
        # Nếu không tìm thấy trong cột nước, mở rộng tìm kiếm
        if not mask.any():
            mask = df_original.astype(str).apply(
                lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)
        
        df_filtered = df_original[mask]

    if df_filtered.empty:
        messagebox.showinfo("Thông báo", f"Không tìm thấy nước nào phù hợp với từ khóa '{keyword}'!")

        # Khôi phục dữ liệu gốc để tránh lỗi hiển thị
        df_current = df_original.copy()
        current_page = 1

        total_pages = get_total_pages(df_current, items_per_page)

        update_table_display(tree, page_label, df_current, current_page, items_per_page)
        page_label.config(text=f"Trang {current_page}/{total_pages}")
        return df_current, current_page

    # Cập nhật dữ liệu tìm kiếm
    df_current = df_filtered
    current_page = 1
    total_pages_filtered = get_total_pages(df_current, items_per_page)

    # Hiển thị kết quả tìm kiếm với số trang mới
    update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages_filtered}")
    
    # Thông báo số kết quả tìm thấy
    messagebox.showinfo("Kết quả tìm kiếm", f"Tìm thấy {len(df_filtered)} nước phù hợp với từ khóa '{keyword}'")

    return df_current, current_page

def search_by_country_name(country_name, df_original):
    """Hàm tìm kiếm cụ thể theo tên nước (hỗ trợ tìm kiếm chính xác)"""
    if not country_name or df_original is None or df_original.empty:
        return pd.DataFrame()
    
    country_name = country_name.strip()
    
    # Tìm cột chứa tên nước
    country_columns = []
    for col in df_original.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['country', 'nation', 'region']):
            country_columns.append(col)
    
    if not country_columns:
        return pd.DataFrame()
    
    # Tìm kiếm chính xác trước
    for col in country_columns:
        exact_match = df_original[df_original[col].astype(str).str.lower() == country_name.lower()]
        if not exact_match.empty:
            return exact_match
    
    # Nếu không có kết quả chính xác, tìm kiếm gần đúng
    for col in country_columns:
        partial_match = df_original[df_original[col].astype(str).str.contains(
            country_name, case=False, na=False)]
        if not partial_match.empty:
            return partial_match
    
    return pd.DataFrame()

def get_country_suggestions(partial_name, df_original, limit=5):
    """Hàm gợi ý tên nước khi người dùng gõ"""
    if not partial_name or df_original is None or df_original.empty:
        return []
    
    partial_name = partial_name.lower().strip()
    suggestions = []
    
    # Tìm cột chứa tên nước
    for col in df_original.columns:
        col_lower = col.lower()
        if any(term in col_lower for term in ['country', 'nation', 'region']):
            # Lấy danh sách tên nước duy nhất
            countries = df_original[col].dropna().astype(str).unique()
            
            # Tìm các nước phù hợp
            for country in countries:
                if partial_name in country.lower() and country not in suggestions:
                    suggestions.append(country)
                    if len(suggestions) >= limit:
                        break
            
            if len(suggestions) >= limit:
                break
    
    return sorted(suggestions)[:limit]

def handle_reset_search(df_original, current_page, items_per_page, tree, page_label, search_entry):
    """Hàm reset tìm kiếm về dữ liệu gốc"""
    if df_original is None or df_original.empty:
        messagebox.showerror("Lỗi", "Không có dữ liệu gốc để reset!")
        return df_original, current_page

    # Khôi phục dữ liệu về trạng thái ban đầu
    df_current = df_original.copy()
    current_page = 1

    # Xóa nội dung ô tìm kiếm để đảm bảo reset hoàn toàn
    search_entry.delete(0, 'end')

    # Tính lại số trang sau khi reset
    total_pages = get_total_pages(df_current, items_per_page)

    # Cập nhật lại bảng hiển thị
    update_table_display(tree, page_label, df_current, current_page, items_per_page)
    page_label.config(text=f"Trang {current_page}/{total_pages}")

    messagebox.showinfo("Thông báo", "Đã reset tìm kiếm về dữ liệu gốc!")

    return df_current, current_page