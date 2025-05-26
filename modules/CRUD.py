# modules/crud.py

import pandas as pd
import math # Cần import math để sử dụng math.ceil

def read_data(file_path):
    """Đọc dữ liệu từ file CSV và trả về DataFrame."""
    return pd.read_csv(file_path)

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

def filter_data(df, column, min_value, max_value):
    """Lọc dữ liệu theo khoảng giá trị cho một cột cụ thể."""
    if df is None or df.empty:
        return pd.DataFrame()

    if column not in df.columns:
        # Nếu cột không tồn tại, bạn có thể muốn xử lý lỗi hoặc trả về df rỗng
        raise ValueError(f"Cột '{column}' không tồn tại trong dữ liệu.")
    
    # Tạo một bản sao để tránh cảnh báo SettingWithCopyWarning
    df_copy = df.copy()

    # Đảm bảo cột là kiểu số để lọc, chuyển đổi lỗi thành NaN
    df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
    
    # Loại bỏ các hàng có giá trị NaN trong cột đang lọc
    filtered_df = df_copy.dropna(subset=[column])

    # Lọc dữ liệu
    filtered_df = filtered_df[(filtered_df[column] >= min_value) & (filtered_df[column] <= max_value)]
    return filtered_df