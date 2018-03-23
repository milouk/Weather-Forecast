import requests
import datetime
import pytemperature
import tkinter as tk
import io
from PIL import Image, ImageTk
from urllib.request import urlopen

date = {}
days = {}
buttons = {}

def getWeekDay(day):
    return {
       -1 : 'Sunday',
        0 : 'Monday',
        1 : 'Tuesday',
        2 : 'Wednesday',
        3 : 'Thursday',
        4 : 'Friday',
        5 : 'Saturday',
        6 : 'Sunday'
    }[day]

def start(event = None):
    window.geometry("500x500")
    country_code_label.pack_forget()
    country_code.pack_forget()
    city_name_label.pack_forget()
    city_name.pack_forget()
    show_forecast.pack_forget()
    error_label.pack()
    error_label.pack_forget()
    api_key = "9286d1d64052c5ea55e0a13f7eba1d4a"
    try:
        req = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=" + city_name.get() + "," + country_code.get() + "&appid=" + api_key)
        for i in range(0, len(req.json()["list"])):
            full_date = req.json()["list"][i]["dt_txt"]
            year = full_date.split(" ")[0].split("-")[0]
            month = full_date.split(" ")[0].split("-")[1]
            day = full_date.split(" ")[0].split("-")[2]
            tmp = req.json()["list"][i]["main"]["temp"]
            max_tmp = req.json()["list"][i]["main"]["temp_max"]
            min_tmp = req.json()["list"][i]["main"]["temp_min"]
            weather_des = req.json()["list"][i]["weather"][0]["description"]
            icon = req.json()["list"][i]["weather"][0]["icon"]
            if getWeekDay(datetime.datetime(int(year), int(month), int(day)).weekday()) not in days.keys():
                days[getWeekDay(datetime.datetime(int(year), int(month), int(day)).weekday())] = day + " - " + month
            if not day + " - " + month in date.keys():
                    date[day + " - " + month] = []
            if str(int(full_date.split(" ")[1].split(":")[0])) == '0':
                list = "21:00 - " + str(full_date.split(" ")[1].split(":")[0]) + ":00"
                day = getWeekDay(datetime.datetime(int(year), int(month), int(day)).weekday() - 1)
                date[days[day]].append([list, round(pytemperature.k2c(tmp), 1), round(pytemperature.k2c(max_tmp), 1), round(pytemperature.k2c(min_tmp), 1), weather_des, icon])
            else:
                list = str(int(full_date.split(" ")[1].split(":")[0]) - 3) + ":00 - " + str(full_date.split(" ")[1].split(":")[0]) + ":00"
                date[day + ' - ' + month].append([list, round(pytemperature.k2c(tmp), 1), round(pytemperature.k2c(max_tmp), 1), round(pytemperature.k2c(min_tmp), 1), weather_des, icon])
    except Exception:
        country_code_label.pack(pady = '10')
        country_code.pack()
        country_code.focus_set()
        city_name_label.pack(pady = '10')
        city_name.pack()
        show_forecast.pack(pady = '10')
        error_label.pack(pady = '10')
    for i in days.keys():
        var = str(i)
        var = tk.Button(window, text = i + '\n' +  days[i], font = 'bold', default='active', bg='white', fg = 'black', width = '20', pady = '0')
        buttons[var] = i
        var.configure(command = lambda button = var : showForecast(button))
        var.pack(pady = '10')
def showForecast(button):
    day = days[buttons[button]]
    for button in buttons.keys():
        button.pack_forget();
    if len(date[day]) == 8 or len(date[day]) == 7:
        window.geometry("1150x450")
    elif len(date[day]) == 6 or len(date[day]) == 5:
        window.geometry("850x450")
    elif len(date[day]) == 4 or len(date[day]) == 3:
        window.geometry("700x450")
    elif len(date[day]) == 2 or len(date[day]) == 1:
        window.geometry("280x450")

    j = 0
    for i in range(0, len(date[day])):
        weather_label = tk.Label(window, image = "", bg = 'black')
        weather_icon_url = "http://openweathermap.org/img/w/" + str(date[day][i][5]) + ".png"
        open_url = urlopen(weather_icon_url)
        weather_icon = io.BytesIO(open_url.read())
        pil_img = Image.open(weather_icon)
        weath_icon = ImageTk.PhotoImage(pil_img)
        weather_label.config(image = weath_icon)
        weather_label.image = weath_icon
        if i >= (len(date[day]) / 2):
            tk.Label(window, text = date[day][i][0] ,font = 'verdana 15 bold', bg='black', fg = 'white').grid(row = 7, column = j, ipadx = '30', pady = '10')
            weather_label.grid(row = 8, column = j, ipadx = '30')
            tk.Label(window, text = 'Weather Description : ' + str(date[day][i][4]) ,font = 'verdana 10', bg='black', fg = 'white').grid(row = 9, column = j, ipadx = '30')
            tk.Label(window, text = 'Current Temperature : ' + str(date[day][i][1]) + ' °C' ,font = 'verdana 10', bg='black', fg = 'white').grid(row = 10, column = j, ipadx = '30')
            tk.Label(window, text = 'Maximum Temperature : ' + str(date[day][i][2]) + ' °C',font = 'verdana 10', bg='black', fg = 'white').grid(row = 11, column = j, ipadx = '30')
            tk.Label(window, text = 'Minimum Temperature : ' + str(date[day][i][3]) + ' °C',font = 'verdana 10', bg='black', fg = 'white').grid(row = 12, column = j, ipadx = '30' )
            j += 1
        else:
            tk.Label(window, text = date[day][i][0] ,font = 'verdana 15 bold', bg='black', fg = 'white').grid(row = 0, column = i, ipadx = '30')
            weather_label.grid(row = 1, column = i, ipadx = '30')
            tk.Label(window, text = 'Weather Description : ' + str(date[day][i][4]) ,font = 'verdana 10', bg='black', fg = 'white').grid(row = 2, column = i, ipadx = '30')
            tk.Label(window, text = 'Current Temperature : ' + str(date[day][i][1]) + ' °C' ,font = 'verdana 10', bg='black', fg = 'white').grid(row = 3, column = i, ipadx = '30')
            tk.Label(window, text = 'Maximum Temperature : ' + str(date[day][i][2]) + ' °C',font = 'verdana 10', bg='black', fg = 'white').grid(row = 4, column = i, ipadx = '30')
            tk.Label(window, text = 'Minimum Temperature : ' + str(date[day][i][3]) + ' °C',font = 'verdana 10', bg='black', fg = 'white').grid(row = 5, column = i, ipadx = '30')



#GUI
window = tk.Tk()
window.title("Weather")
window.geometry("500x300")
window.configure(background = 'black')
window.resizable(0, 0)

country_code_label = tk.Label(window, text = "Enter Country Code",font = 'verdana 10', bg='black', fg = 'white')
country_code_label.pack(pady = '10')
country_code = tk.Entry(window, width = 40)
country_code.pack()
country_code.focus_set()
city_name_label = tk.Label(window, text = "Enter City Name", font = 'verdana 10', bg='black', fg = 'white')
city_name_label.pack(pady = '10')
city_name = tk.Entry(window, width =  40)
city_name.pack()
window.bind('<Return>', start)
weather_label = tk.Label(window, image = "", bg = 'black')
city_label = tk.Label(window, text = "", font = 'bold', bg='black', fg = 'white')
c_tmp_label = tk.Label(window, text = "", bg='black', fg = 'white')
min_tmp_label = tk.Label(window, text = "", bg='black', fg = 'white')
max_tmp_label = tk.Label(window, text = "", bg='black', fg = 'white')
weath_desc_label = tk.Label(window, text = "", bg='black', fg = 'white')
error_label = tk.Label(window, text = "Wrong Country Code or City Name, Please try again!", bg = 'black', fg = 'red', font = 'bold')
show_forecast = tk.Button(window, text = "Show Weather Forecast", font = 'monospace 10 bold', command = start, default='active', bg='white', fg = 'black', width = '20', pady = '8')
show_forecast.pack(pady = '30')
window.mainloop()
