import sys
import tkinter as tk
import requests
import ttkbootstrap
import threading 
from tkinter import messagebox
from PIL import Image, ImageTk

# Function to get weather information
def get_weather(city):
    api_key = "188dfa71cbef2a9cf227415c4a717878"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    res = requests.get(url)
    if res.status_code == 404:
        messagebox.showerror("Error", "City not found")
        return None
    
    # Parse the response JSON to get information
    weather = res.json()
    icon_id = weather["weather"][0]["icon"]
    temp = weather["main"]["temp"] - 273.15
    description = weather["weather"][0]["description"]
    city = weather["name"]
    country = weather["sys"]["country"]

    # get icon url and return weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return (icon_url, temp, description, city, country)

# function to update ui
def update_ui(icon_url, temp, description, city, country):
    location_label.configure(text = f"{city}, {country}")

    image = Image.open(requests.get(icon_url, stream = True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image = icon)
    icon_label.image = icon

    temp_label.configure(text = f"Temperature: {temp:.2f}°C")

    desc_label.configure(text = f"Description: {description}")


# Function to fetch weather in background
def fetch_weather(city):
    result = get_weather(city)
    if result is None:
        return
    icon_url, temp, description, city, country = result
    root.after(0, lambda: update_ui(icon_url, temp, description, city, country, ))

# Function to search city
def search():
    city = city_entry.get()
    if city.strip() == "":
        messagebox.showwarning("Warning", "Pleas enter a city name.")
        return
    threading.Thread(target = fetch_weather, args = (city,), daemon = True).start()


root = ttkbootstrap.Window(themename =  "morph")
root.title("Weather APP")
root.geometry("700x500")

# entry widget to enter city name
city_entry = ttkbootstrap.Entry(root, font = "Helvetica, 18")
city_entry.pack(pady = 10)

city_entry.bind("<Return>", lambda event:search())

# button to search for the weather information
search_buttom = ttkbootstrap.Button(root, text="Search", command = search, bootstyle="warning")
search_buttom.pack(pady = 10)

# label to show city/country name
location_label = tk.Label(root, font = "Helvetica, 25")
location_label.pack(pady = 20)

# label to show weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label to show temp
temp_label = tk.Label(root, font = "Helvetica, 20")
temp_label.pack()

# Label to show weather description
desc_label = tk.Label(root, font = "Helvetica, 20")
desc_label.pack()

root.mainloop()

