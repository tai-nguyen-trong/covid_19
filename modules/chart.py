import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt

# Hàm mở cửa sổ chứa các nút chọn biểu đồ
def open_chart_window():
    chart_window = tk.Toplevel(root)
    chart_window.title("Chọn biểu đồ")
    chart_window.geometry("300x300")
    chart_window.grab_set()

    # Nạp dữ liệu từ tệp CSV
    df = pd.read_csv("dataset/country_wise_latest.csv")

    # Các nút để chọn biểu đồ
    tk.Button(chart_window, text="Ca nhiễm nhiều nhất", command=lambda: draw_chart1(df)).pack(pady=5)
    tk.Button(chart_window, text="Tử vong cao nhất", command=lambda: draw_chart2(df)).pack(pady=5)
    tk.Button(chart_window, text="Tỷ lệ tử vong theo WHO", command=lambda: draw_chart3(df)).pack(pady=5)
    tk.Button(chart_window, text="Tăng trưởng ca nhiễm", command=lambda: draw_chart4(df)).pack(pady=5)
    tk.Button(chart_window, text="Tỷ lệ hồi phục", command=lambda: draw_chart5(df)).pack(pady=5)

def draw_chart1(df):
    plt.figure(figsize=(8, 5))
    top_confirmed = df.sort_values("Confirmed", ascending=False).head(10)
    plt.bar(top_confirmed["Country/Region"], top_confirmed["Confirmed"], color='orange')
    plt.title("Top 10 quốc gia có số ca nhiễm COVID-19 cao nhất")
    plt.ylabel("Số ca nhiễm")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart2(df):
    plt.figure(figsize=(8, 5))
    top_deaths = df.sort_values("Deaths", ascending=False).head(10)
    plt.bar(top_deaths["Country/Region"], top_deaths["Deaths"], color='red')
    plt.title("Top 10 quốc gia có số ca tử vong cao nhất")
    plt.ylabel("Số ca tử vong")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart3(df):
    plt.figure(figsize=(8, 5))
    region_deaths = df.groupby("WHO Region")["Deaths"].sum()
    plt.pie(region_deaths, labels=region_deaths.index, autopct='%1.1f%%', startangle=140)
    plt.title("Tỷ lệ tử vong theo khu vực WHO")
    plt.show()

def draw_chart4(df):
    plt.figure(figsize=(8, 5))
    top_growth = df.sort_values("1 week % increase", ascending=False).head(10)
    plt.bar(top_growth["Country/Region"], top_growth["1 week % increase"], color='purple')
    plt.title("Top 10 quốc gia có tỷ lệ tăng trưởng ca nhiễm trong 1 tuần cao nhất")
    plt.ylabel("Tỷ lệ tăng trưởng (%)")
    plt.xticks(rotation=45)
    plt.show()

def draw_chart5(df):
    plt.figure(figsize=(8, 5))
    top_recovered_ratio = df.sort_values("Recovered / 100 Cases", ascending=False).head(10)
    plt.bar(top_recovered_ratio["Country/Region"], top_recovered_ratio["Recovered / 100 Cases"], color='green')
    plt.title("Top 10 quốc gia có tỷ lệ hồi phục cao nhất")
    plt.ylabel("Tỷ lệ hồi phục trên 100 ca (%)")
    plt.xticks(rotation=45)
    plt.show()


