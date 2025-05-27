# modules/crud.py

import pandas as pd
import math # Cần import math để sử dụng math.ceil

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

