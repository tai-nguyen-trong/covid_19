# modules/crud.py
import pandas as pd
import numpy as np
from tkinter import messagebox
from display.formInfo import show_form_window
from .navigation import get_total_pages
from .updateTable import update_table_display
import os

class CRUDManager:
    """Class quản lý các thao tác CRUD"""
    
    def __init__(self):
        self.file_path = "dataset/country_wise_latest.csv"
    
    def ensure_directory_exists(self):
        """Đảm bảo thư mục tồn tại"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
    
    def save_to_file(self, df):
        """Lưu DataFrame vào file"""
        try:
            self.ensure_directory_exists()
            df.to_csv(self.file_path, index=False)
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
            return False
    
    def validate_data(self, data, df_columns, is_update=False):
        """Validate dữ liệu"""
        errors = []
        
        # Kiểm tra các trường bắt buộc
        required_fields = ['Country/Region']
        for field in required_fields:
            if field in df_columns and field in data:
                if isinstance(data[field], str) and not data[field].strip():
                    errors.append(f"Trường '{field}' không được để trống")
        
        # Kiểm tra dữ liệu số
        numeric_fields = ['Confirmed', 'Deaths', 'Recovered', 'Active']
        for field in numeric_fields:
            if field in df_columns and field in data:
                if isinstance(data[field], str) and data[field].strip():
                    try:
                        value = float(data[field])
                        if value < 0:
                            errors.append(f"Trường '{field}' không được âm")
                    except ValueError:
                        errors.append(f"Trường '{field}' phải là số")
        
        return errors
    
    def process_data_types(self, data, df_working):
        """Xử lý kiểu dữ liệu"""
        processed_data = {}
        
        for key, val in data.items():
            if key in df_working.columns:
                # Xử lý giá trị trống
                if isinstance(val, str) and val.strip() == "":
                    processed_data[key] = np.nan
                else:
                    # Chuyển đổi kiểu dữ liệu phù hợp
                    if df_working[key].dtype in ['int64', 'float64']:
                        try:
                            processed_data[key] = pd.to_numeric(val, errors='coerce')
                        except:
                            processed_data[key] = np.nan
                    else:
                        processed_data[key] = val
            else:
                processed_data[key] = val
        
        return processed_data
    
    def handle_add_data(self, root, df, df_original, df_current, current_page, items_per_page, tree, page_label):
        """Hàm thêm dữ liệu mới"""
        
        # Kiểm tra xem đã có dữ liệu chưa
        if df is None or df.empty:
            messagebox.showwarning("Cảnh báo", "Vui lòng tải file CSV trước khi thêm dữ liệu!")
            return df, df_original, df_current, current_page
        
        def on_submit(new_data):
            nonlocal df, df_original, df_current, current_page
            
            try:
                # Validate dữ liệu
                errors = self.validate_data(new_data, df_original.columns)
                if errors:
                    messagebox.showerror("Lỗi validation", "\n".join(errors))
                    return
                
                # Sử dụng df_original làm base
                df_working = df_original.copy()
                
                # Xử lý dữ liệu mới
                processed_data = self.process_data_types(new_data, df_working)
                
                # Thêm dòng mới
                new_row = pd.DataFrame([processed_data])
                df = pd.concat([df_working, new_row], ignore_index=True)
                
                # Cập nhật tất cả DataFrame
                df_original = df.copy()
                df_current = df.copy()
                
                # Lưu vào file
                if self.save_to_file(df):
                    # Cập nhật giao diện
                    total_pages = get_total_pages(df_current, items_per_page)
                    current_page = total_pages  # Chuyển đến trang cuối
                    
                    update_table_display(tree, page_label, df_current, current_page, items_per_page)
                    page_label.config(text=f"Trang {current_page}/{total_pages}")
                    
                    messagebox.showinfo("Thành công", "Dữ liệu đã được thêm thành công!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm dữ liệu: {str(e)}")
        
        # Hiển thị form
        show_form_window(root, data=None, on_submit=on_submit)
        return df, df_original, df_current, current_page
    
    def handle_update_data(self, root, df, df_original, df_current, current_page, items_per_page, tree, page_label):
        """Hàm cập nhật dữ liệu"""
        
        # Kiểm tra có dòng nào được chọn
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một dòng để cập nhật.")
            return df, df_original, df_current, current_page
        
        # Kiểm tra dữ liệu có tồn tại
        if df_original is None or df_original.empty:
            messagebox.showerror("Lỗi", "Không có dữ liệu để cập nhật!")
            return df, df_original, df_current, current_page
        
        # Tính chỉ mục thực tế
        tree_index = tree.index(selected[0])
        actual_index = tree_index + (current_page - 1) * items_per_page
        
        # Kiểm tra chỉ mục hợp lệ
        if actual_index >= len(df_original):
            messagebox.showerror("Lỗi", "Chỉ mục không hợp lệ!")
            return df, df_original, df_current, current_page
        
        # Lấy dữ liệu hiện tại
        current_data = df_original.iloc[actual_index].to_dict()
        
        def on_submit(updated_data):
            nonlocal df, df_original, df_current, current_page
            
            try:
                # Validate dữ liệu
                errors = self.validate_data(updated_data, df_original.columns, is_update=True)
                if errors:
                    messagebox.showerror("Lỗi validation", "\n".join(errors))
                    return
                
                # Tạo bản sao để làm việc
                df_working = df_original.copy()
                
                # Xử lý và cập nhật dữ liệu
                processed_data = self.process_data_types(updated_data, df_working)
                
                # Cập nhật từng trường
                for key, val in processed_data.items():
                    if key in df_working.columns:
                        df_working.at[actual_index, key] = val
                
                # Cập nhật tất cả DataFrame
                df = df_working.copy()
                df_original = df_working.copy()
                df_current = df_working.copy()
                
                # Lưu vào file
                if self.save_to_file(df):
                    # Cập nhật giao diện
                    total_pages = get_total_pages(df_current, items_per_page)
                    current_page = min(current_page, max(1, total_pages))
                    
                    update_table_display(tree, page_label, df_current, current_page, items_per_page)
                    page_label.config(text=f"Trang {current_page}/{total_pages}")
                    
                    messagebox.showinfo("Thành công", "Dữ liệu đã được cập nhật thành công!")
                
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật dữ liệu: {str(e)}")
        
        # Hiển thị form với dữ liệu hiện tại
        show_form_window(root, data=current_data, on_submit=on_submit)
        return df, df_original, df_current, current_page
    
    def handle_delete_data(self, df, df_original, df_current, current_page, items_per_page, tree, page_label):
        """Hàm xóa dữ liệu"""
        
        # Kiểm tra có dòng nào được chọn
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn ít nhất một dòng để xóa.")
            return df, df_original, df_current, current_page
        
        # Xác nhận xóa
        if not messagebox.askyesno("Xác nhận", f"Bạn chắc chắn muốn xóa {len(selected)} dòng đã chọn?"):
            return df, df_original, df_current, current_page
        
        # Kiểm tra dữ liệu có tồn tại
        if df_original is None or df_original.empty:
            messagebox.showerror("Lỗi", "Không có dữ liệu để xóa!")
            return df, df_original, df_current, current_page
        
        try:
            # Tạo bản sao để làm việc
            df_working = df_original.copy()
            
            # Tính chỉ mục thực tế trong DataFrame
            indexes_to_delete = []
            for item in selected:
                tree_index = tree.index(item)
                actual_index = tree_index + (current_page - 1) * items_per_page
                if actual_index < len(df_working):
                    indexes_to_delete.append(actual_index)
            
            if not indexes_to_delete:
                messagebox.showwarning("Cảnh báo", "Không có dòng hợp lệ để xóa!")
                return df, df_original, df_current, current_page
            
            # Xóa các dòng (sắp xếp theo thứ tự giảm dần)
            indexes_to_delete.sort(reverse=True)
            for idx in indexes_to_delete:
                df_working = df_working.drop(df_working.index[idx]).reset_index(drop=True)
            
            # Cập nhật tất cả DataFrame
            df = df_working.copy()
            df_original = df_working.copy()
            df_current = df_working.copy()
            
            # Lưu vào file
            if self.save_to_file(df):
                # Cập nhật giao diện
                if df_current.empty:
                    current_page = 1
                    page_label.config(text="Trang -/-")
                    # Xóa tất cả items trong tree
                    for item in tree.get_children():
                        tree.delete(item)
                else:
                    total_pages = get_total_pages(df_current, items_per_page)
                    current_page = min(current_page, max(1, total_pages))
                    
                    update_table_display(tree, page_label, df_current, current_page, items_per_page)
                    page_label.config(text=f"Trang {current_page}/{total_pages}")
                
                messagebox.showinfo("Thành công", f"Đã xóa thành công {len(indexes_to_delete)} dòng!")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa dữ liệu: {str(e)}")
        
        return df, df_original, df_current, current_page
    
    
# Tạo instance global để sử dụng
crud_manager = CRUDManager()

# Các hàm wrapper để tương thích với code cũ
def handle_add_data(root, df, df_original, df_current, current_page, items_per_page, tree, page_label):
    return crud_manager.handle_add_data(root, df, df_original, df_current, current_page, items_per_page, tree, page_label)

def handle_update_data(root, df, df_original, df_current, current_page, items_per_page, tree, page_label):
    return crud_manager.handle_update_data(root, df, df_original, df_current, current_page, items_per_page, tree, page_label)

def handle_delete_data(df, df_original, df_current, current_page, items_per_page, tree, page_label):
    return crud_manager.handle_delete_data(df, df_original, df_current, current_page, items_per_page, tree, page_label)
