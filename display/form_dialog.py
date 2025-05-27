# display/form_dialog.py

import tkinter as tk

def show_form_window(root, data=None, on_submit=None):
    form = tk.Toplevel(root)
    form.title("Nhập hoặc sửa dữ liệu")
    form.geometry("450x700")
    form.grab_set()

    fields = [
        "Country/Region", "Confirmed", "Deaths", "Recovered", "Active",
        "New cases", "New deaths", "New recovered",
        "Deaths / 100 Cases", "Recovered / 100 Cases", "Deaths / 100 Recovered",
        "1 week % increase", "1 week change", "WHO Region"
    ]

    entries = {}

    for idx, field in enumerate(fields):
        label = tk.Label(form, text=field)
        label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

        entry = tk.Entry(form, width=30)
        entry.grid(row=idx, column=1, padx=10, pady=5)

        if data and field in data:
            entry.insert(0, str(data[field]))
        entries[field] = entry

    def submit_action():
        result = {field: entry.get() for field, entry in entries.items()}
        if on_submit:
            on_submit(result)
        form.destroy()

    submit_btn = tk.Button(form, text="Lưu", command=submit_action)
    submit_btn.grid(row=len(fields), column=0, columnspan=2, pady=15)

    form.mainloop()
