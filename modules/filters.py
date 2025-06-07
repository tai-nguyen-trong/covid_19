# modules/filters.py
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from modules.updateTable import update_table_display
from modules.navigation import get_total_pages

def show_filter_window(parent, df_original):
    """Hiển thị cửa sổ lọc dữ liệu đơn giản"""
    if df_original is None or df_original.empty:
        messagebox.showwarning("Warning", "Không có dữ liệu để lọc!")
        return
    
    # Tạo cửa sổ filter
    filter_window = tk.Toplevel(parent)
    filter_window.title("Lọc Dữ Liệu")
    filter_window.geometry("400x350")
    filter_window.resizable(False, False)
    
    # Title
    title_label = tk.Label(filter_window, text="Lọc Dữ Liệu", font=("Arial", 14, "bold"))
    title_label.pack(pady=10)
    
    # Frame chọn cột
    col_frame = tk.Frame(filter_window)
    col_frame.pack(pady=10, fill="x", padx=20)
    
    tk.Label(col_frame, text="Chọn cột:").pack(anchor="w")
    col_combo = ttk.Combobox(col_frame, values=list(df_original.columns), state="readonly")
    col_combo.pack(fill="x", pady=5)
    if len(df_original.columns) > 0:
        col_combo.set(df_original.columns[0])
    
    # Frame điều kiện
    condition_frame = tk.Frame(filter_window)
    condition_frame.pack(pady=10, fill="x", padx=20)
    
    tk.Label(condition_frame, text="Điều kiện:").pack(anchor="w")
    condition_combo = ttk.Combobox(condition_frame, values=["Chứa", "Bằng", "Lớn hơn", "Nhỏ hơn"], state="readonly")
    condition_combo.pack(fill="x", pady=5)
    condition_combo.set("Chứa")
    
    # Frame giá trị
    value_frame = tk.Frame(filter_window)
    value_frame.pack(pady=10, fill="x", padx=20)
    
    tk.Label(value_frame, text="Giá trị:").pack(anchor="w")
    value_entry = tk.Entry(value_frame)
    value_entry.pack(fill="x", pady=5)
    
    def apply_filter():
        """Áp dụng bộ lọc"""
        try:
            col = col_combo.get()
            condition = condition_combo.get()
            value = value_entry.get().strip()
            
            if not col or not condition or not value:
                messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            filtered_df = df_original.copy()
            
            if condition == "Chứa":
                filtered_df = filtered_df[filtered_df[col].astype(str).str.contains(value, case=False, na=False)]
            elif condition == "Bằng":
                filtered_df = filtered_df[filtered_df[col].astype(str) == value]
            elif condition == "Lớn hơn":
                try:
                    filtered_df = filtered_df[pd.to_numeric(filtered_df[col], errors='coerce') > float(value)]
                except ValueError:
                    messagebox.showerror("Lỗi", "Giá trị phải là số!")
                    return
            elif condition == "Nhỏ hơn":
                try:
                    filtered_df = filtered_df[pd.to_numeric(filtered_df[col], errors='coerce') < float(value)]
                except ValueError:
                    messagebox.showerror("Lỗi", "Giá trị phải là số!")
                    return
            
            # Cập nhật dữ liệu trong main window
            import display.menu as menu
            menu.df_current = filtered_df.copy()
            menu.current_page = 1
            
            # Cập nhật bảng hiển thị
            update_table_display(menu.tree, menu.page_label, menu.df_current, 
                               menu.current_page, menu.items_per_page)
            
            # Cập nhật label trang
            total_pages = get_total_pages(menu.df_current, menu.items_per_page)
            menu.page_label.config(text=f"Trang {menu.current_page}/{total_pages}")
            
            messagebox.showinfo("Thành công", f"Đã lọc được {len(filtered_df)} bản ghi từ {len(df_original)} bản ghi ban đầu.")
            filter_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi áp dụng bộ lọc: {str(e)}")
    
    def reset_filter():
        """Reset về dữ liệu gốc"""
        import display.menu as menu
        menu.df_current = df_original.copy()
        menu.current_page = 1
        
        # Cập nhật bảng hiển thị
        update_table_display(menu.tree, menu.page_label, menu.df_current, 
                           menu.current_page, menu.items_per_page)
        
        # Cập nhật label trang
        total_pages = get_total_pages(menu.df_current, menu.items_per_page)
        menu.page_label.config(text=f"Trang {menu.current_page}/{total_pages}")
        
        messagebox.showinfo("Thành công", "Đã reset về dữ liệu ban đầu.")
        filter_window.destroy()
    
    # Buttons
    button_frame = tk.Frame(filter_window)
    button_frame.pack(pady=20)
    
    apply_btn = tk.Button(button_frame, text="Áp Dụng", command=apply_filter, 
                         bg="lightgreen", width=12)
    apply_btn.pack(side="left", padx=5)
    
    reset_btn = tk.Button(button_frame, text="Reset", command=reset_filter, 
                         bg="orange", width=12)
    reset_btn.pack(side="left", padx=5)
    
    close_btn = tk.Button(button_frame, text="Đóng", command=filter_window.destroy, 
                         bg="lightgray", width=12)
    close_btn.pack(side="left", padx=5)