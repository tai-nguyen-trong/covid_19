# modules/filters.py
import pandas as pd

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