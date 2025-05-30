# cập nhật bảng dữ liệu (Treeview) trên giao diện bằng cách xóa dữ liệu cũ và hiển thị dữ liệu theo trang hiện tại.
# from modules.navigation import get_total_pages


def update_table_display(target_table, target_page_label, df_to_display, current_page_num, items_per_pg):
    from modules.navigation import get_total_pages  # 🔥 Import tại chỗ tránh vòng lặp

    """
    Hàm cập nhật một bảng dữ liệu (Treeview) trên giao diện.
    Nhận target_table (Treeview), target_page_label (Label), DataFrame cần hiển thị,
    số trang hiện tại và số mục trên trang làm đối số.
    """
    if df_to_display is None or df_to_display.empty:
        for row in target_table.get_children():
            target_table.delete(row)
        target_page_label.config(text="Trang -/-")
        return
    
    total_pages = get_total_pages(df_to_display, items_per_pg)

    # Phân trang dữ liệu
    start_idx = (current_page_num - 1) * items_per_pg
    end_idx = start_idx + items_per_pg
    page_data = df_to_display.iloc[start_idx:end_idx]

    # Xóa dữ liệu cũ trong bảng
    for row in target_table.get_children():
        target_table.delete(row)

    # Cập nhật dữ liệu vào bảng
    for _, row in page_data.iterrows():

        target_table.insert("", "end", values=list(row))

    target_page_label.config(text=f"Trang {current_page_num}/{total_pages}")