# main.py
import display.menu
import pandas as pd
from modules.crud import read_data

if __name__ == "__main__":
    display.menu.root.mainloop()  # Khởi chạy giao diện Tkinter
