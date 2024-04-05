import random
import os
import calendar
import requests
import datetime
from win10toast import ToastNotifier
import psutil 
import ctypes

# List of fortunes
fortunes = [
    "A journey of a thousand miles begins with a single step.",
    "You will find happiness in the most unexpected places.",
    "All your hard work will soon pay off.",
    "Good things come to those who wait.",
    "A friend's frown is better than a fool's smile.",
    "The fortune you seek is in another cookie.",
    "Don't pursue happiness - create it.",
    "The smart thing is to prepare for the unexpected.",
    "An inch of time is an inch of gold.",
    "The joyfulness of a man prolongeth his days.",
    "Your luck is about to change."
]

def set_wallpaper(path):
    SPI_SETDESKWALLPAPER = 0x0014
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 3)

def change_wallpaper():
    # Path to the directory containing your wallpaper images
    wallpaper_dir = r"C:\Users\Admin\Pictures\Saved Pictures"

    # Get a list of all files in the directory
    wallpapers = os.listdir(wallpaper_dir)

    # Select a random wallpaper from the list
    random_wallpaper = random.choice(wallpapers)

    # Construct the full path to the selected wallpaper
    wallpaper_path = os.path.join(wallpaper_dir, random_wallpaper)

    # Change the wallpaper
    set_wallpaper(wallpaper_path)

    print("Wallpaper changed!")

def get_fortune():
    """Returns a random fortune from the list."""
    return random.choice(fortunes)

def weather(city):
    api_key = "Replace with your actual API key" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "weather" in data and "main" in data:
            weather = data["weather"][0]["description"]
            temp_kelvin = data["main"]["temp"]
            temp_celsius = temp_kelvin - 273.15
            return f"Weather in {city}: {weather}, Temperature: {temp_celsius}°C"
        else:
            return "Weather information not available."
    else:
        return "Error fetching weather information."

def check_battery_status():
    battery_percentage = psutil.sensors_battery()
    percentage = battery_percentage.percent
    charging = battery_percentage.power_plugged

    if charging:
        if percentage == 100:
            charging_message = "Unplug your Charger"
        else:
            charging_message = "Charging"
    else:
        charging_message = "Not Charging"
    message = str(percentage)+ "% Charged\n" + charging_message

    notify = ToastNotifier()
    notify.show_toast("Battery", message, icon_path=" ",duration=10,threaded=False)

def display_calendar(year, month):
    cal = calendar.month(year, month)
    print(cal)

def calendar_cli(year=None, month=None):
    if year is None or month is None:
        now = datetime.datetime.now()
        year = now.year
        month = now.month

    display_calendar(year, month)

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')
    
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Disk Usage: {disk_info.percent}%")

def list_processes():
    for proc in psutil.process_iter(['pid', 'name']):
        print(proc.info)

def kill_process(pid):
    p = psutil.Process(pid)
    p.terminate()

while True:
    user_input = input("$ ")

    command = user_input.strip().lower()

    if command == "fortune":
        print(get_fortune())
    elif command.startswith("weather"):
        args = command.split()
        if len(args) > 1:
           city = args[1]
           print(weather(city))
        else:
           print("Please provide a city name. Example: weather London")
    elif command == "battery":
        check_battery_status()
    elif command.startswith("calendar"):
        args = command.split()
        if len(args) > 1:
            year, month = map(int, args[1:])
            calendar_cli(year, month)
        else:
            calendar_cli()
    elif command == "change wallpaper":
        change_wallpaper()
    elif command == "system info":
        get_system_info()
    elif command.startswith("list processes"):
        list_processes()
    elif command.startswith("kill process"):
        pid = int(command.split()[2])
        kill_process(pid)
    elif command == "exit":
        break
    else:
        print(f"Unknown command: {command}")
