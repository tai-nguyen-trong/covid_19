"""
Module làm sạch dữ liệu đơn giản
"""
import pandas as pd
import numpy as np
from tkinter import messagebox

def clean_data(df):
    """
    Hàm làm sạch dữ liệu cơ bản
    
    Args:
        df: DataFrame cần làm sạch
    
    Returns:
        DataFrame đã được làm sạch
    """
    if df is None or df.empty:
        return df
    
    df_cleaned = df.copy()
    
    try:
        # 1. Xóa hàng trùng lặp
        before_rows = len(df_cleaned)
        df_cleaned = df_cleaned.drop_duplicates()
        duplicates_removed = before_rows - len(df_cleaned)
        
        # 2. Xử lý giá trị thiếu
        # Cột số: điền bằng 0 hoặc trung bình
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype in ['int64', 'float64']:
                df_cleaned[col].fillna(0, inplace=True)
            else:
                # Cột text: điền bằng "Unknown"
                df_cleaned[col].fillna("Unknown", inplace=True)
        
        # 3. Xóa khoảng trắng thừa trong cột text (GIỮ NGUYÊN KÝ TỰ ĐẶC BIỆT)
        for col in df_cleaned.columns:
            if df_cleaned[col].dtype == 'object':
                # Chỉ xóa khoảng trắng thừa, KHÔNG xóa ký tự đặc biệt
                df_cleaned[col] = df_cleaned[col].astype(str).str.strip()
        
        # 4. Reset index
        df_cleaned = df_cleaned.reset_index(drop=True)
        
        print(f"Đã xóa {duplicates_removed} hàng trùng lặp")
        print(f"Còn lại {len(df_cleaned)} hàng sau khi làm sạch")
        
        return df_cleaned
        
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi làm sạch dữ liệu: {str(e)}")
        return df