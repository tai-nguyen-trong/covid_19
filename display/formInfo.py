# # display/form_dialog.py

# import tkinter as tk

# def show_form_window(root, data=None, on_submit=None):
#     form = tk.Toplevel(root)
#     form.title("Nhập hoặc sửa dữ liệu")
#     form.geometry("450x700")
#     form.grab_set()

#     fields = [
#         "Country/Region", "Confirmed", "Deaths", "Recovered", "Active",
#         "New cases", "New deaths", "New recovered",
#         "Deaths / 100 Cases", "Recovered / 100 Cases", "Deaths / 100 Recovered",
#         "1 week % increase", "1 week change", "WHO Region"
#     ]

#     entries = {}

#     for idx, field in enumerate(fields):
#         label = tk.Label(form, text=field)
#         label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

#         entry = tk.Entry(form, width=30)
#         entry.grid(row=idx, column=1, padx=10, pady=5)

#         if data and field in data:
#             entry.insert(0, str(data[field]))
#         entries[field] = entry

#     def submit_action():
#         result = {field: entry.get() for field, entry in entries.items()}
#         if on_submit:
#             on_submit(result)
#         form.destroy()

#     submit_btn = tk.Button(form, text="Lưu", command=submit_action)
#     submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)

#     # form.mainloop()


import tkinter as tk

def show_form_window(root, data=None, on_submit=None):
    form = tk.Toplevel(root)
    form.title("Nhập hoặc sửa dữ liệu")
    # form.geometry("500x750")  # Điều chỉnh kích thước cho thoáng hơn
    # form.grab_set()


    # Lấy kích thước màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Kích thước của form
    form_width = 500
    form_height = 650

    # Tính toán vị trí trung tâm
    x_position = (screen_width - form_width) // 2
    y_position = (screen_height - form_height) // 2

    # Đặt cửa sổ form ở giữa màn hình
    form.geometry(f"{form_width}x{form_height}+{x_position}+{y_position}")
    form.grab_set()


    fields = [
        "Country/Region", "Confirmed", "Deaths", "Recovered", "Active",
        "New cases", "New deaths", "New recovered",
        "Deaths / 100 Cases", "Recovered / 100 Cases", "Deaths / 100 Recovered",
        "1 week % increase", "1 week change", "WHO Region"
    ]

    entries = {}

    # ==================== KHUNG NHẬP DỮ LIỆU ====================
    form_frame = tk.LabelFrame(form, text="Thông tin COVID-19", font=("Arial", 12, "bold"), padx=15, pady=10)
    form_frame.pack(padx=20, pady=20, fill="both", expand=True)

    for idx, field in enumerate(fields):
        label = tk.Label(form_frame, text=field, font=("Arial", 10))
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(form_frame, width=35, font=("Arial", 10))  # Tăng độ rộng
        entry.grid(row=idx, column=1, padx=10, pady=5)

        if data and field in data:
            entry.insert(0, str(data[field]))
        entries[field] = entry

    # ==================== NÚT LƯU DỮ LIỆU ====================
    def submit_action():
        result = {field: entry.get() for field, entry in entries.items()}
        if on_submit:
            on_submit(result)
        form.destroy()

    submit_btn = tk.Button(form, text="💾 Lưu", bg="lightblue", font=("Arial", 11, "bold"), width=15, command=submit_action)
    submit_btn.pack(pady=15)