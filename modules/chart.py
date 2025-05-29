import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Hàm mở cửa sổ chứa các nút chọn biểu đồ
def open_chart_window(root, df):
    chart_window = tk.Toplevel(root)
    chart_window.title("Chọn biểu đồ")
    chart_window.geometry("300x300")
    chart_window.grab_set()

    # Các nút để chọn biểu đồ
    tk.Button(chart_window, text="10 quốc gia có Ca nhiễm nhiều nhất", command=lambda: draw_chart1(df)).pack(pady=5)
    tk.Button(chart_window, text="Phân Bố Ca Nhiễm Theo Khu Vực WHO", command=lambda: draw_chart2(df)).pack(pady=5)
    tk.Button(chart_window, text="top 5 Tỷ lệ tử vong theo WHO ", command=lambda: draw_chart3(df)).pack(pady=5)
    tk.Button(chart_window, text="Top 10 quốc gia có tỉ lệ gia tăng hàng tuần", command=lambda: draw_chart4(df)).pack(pady=5)
    tk.Button(chart_window, text="Confirmed, Deaths, Recovered của top 8 quốc gia", command=lambda: draw_chart5(df)).pack(pady=5)

    #nut để đóng cửa sổ
    tk.Button(chart_window, text="Đóng", bg="red", fg="white", width=10,command=chart_window.destroy).pack(pady=10)

def show_chart(title, figsize=(12, 6)):
    """Hàm tiện ích để tạo và hiển thị biểu đồ"""
    plt.figure(figsize=figsize)
    plt.title(title, fontsize=14, fontweight='bold')


def draw_chart1(df):
   
    show_chart("Top 10 Quốc Gia - Ca Nhiễm Cao Nhất")
    data = df.nlargest(10, 'Confirmed')
    plt.bar(range(len(data)), data['Confirmed'], color='skyblue')
    plt.xticks(range(len(data)), data['Country/Region'], rotation=45)
    plt.ylabel('Số ca nhiễm')
    
    plt.tight_layout()
    plt.show()

def draw_chart2(df):
    """Biểu đồ tròn - Phân bố theo khu vực WHO"""
    show_chart("Phân Bố Ca Nhiễm Theo Khu Vực WHO", (10, 8))   
    region_data = df.groupby('WHO Region')['Confirmed'].sum()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0']
    plt.pie(region_data.values, labels=region_data.index, autopct='%1.1f%%', colors=colors)
    
    plt.show()

def draw_chart3(df):
    """Biểu đồ đường - Top 5 tỷ lệ tử vong"""
    show_chart("Top 5 Quốc Gia - Tỷ Lệ Tử Vong Cao Nhất", (10, 6))
    
    data = df.nlargest(5, 'Deaths / 100 Cases')
    plt.plot(range(len(data)), data['Deaths / 100 Cases'], marker='o', linewidth=2, markersize=8, color='red')
    plt.xticks(range(len(data)), data['Country/Region'], rotation=45)
    plt.ylabel('Tỷ lệ tử vong / 100 ca')
    plt.grid(True, alpha=0.3)
    
    # Thêm giá trị
    for i, v in enumerate(data['Deaths / 100 Cases']):
        plt.text(i, v + max(data['Deaths / 100 Cases']) * 0.02, f'{v:.1f}%', ha='center')
    
    plt.tight_layout()
    plt.show()
def draw_chart4(df):
    """Biểu đồ cột ngang - Top 10 tăng trưởng tuần"""
    show_chart("Top 10 Quốc Gia - Tăng Trưởng Tuần (%)", (10, 8))
    
    data = df.nlargest(10, '1 week % increase')
    plt.barh(range(len(data)), data['1 week % increase'], color='orange')
    plt.yticks(range(len(data)), data['Country/Region'])
    plt.xlabel('Tỷ lệ tăng trưởng (%)')
    
    plt.tight_layout()
    plt.show()

def draw_chart5(df):
    """Biểu đồ cột nhóm - So sánh 3 chỉ số"""
    show_chart("So Sánh 3 Chỉ Số - Top 8 Quốc Gia", (14, 8))
    
    data = df.nlargest(8, 'Confirmed')
    x = np.arange(len(data))
    width = 0.25
    
    plt.bar(x - width, data['Confirmed'], width, label='Ca nhiễm', color='lightblue')
    plt.bar(x, data['Deaths'], width, label='Ca tử vong', color='red', alpha=0.7)
    plt.bar(x + width, data['Recovered'], width, label='Ca khỏi bệnh', color='green', alpha=0.7)
    
    plt.xlabel('Quốc gia')
    plt.ylabel('Số ca')
    plt.xticks(x, data['Country/Region'], rotation=45)
    plt.legend()
    
    plt.tight_layout()
    plt.show()