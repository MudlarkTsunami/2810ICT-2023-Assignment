import datetime
import os.path

import PySimpleGUI as sg

# Changing the default theme to a darker one
sg.theme('DarkAmber')
# Default value of the chart image points to an error image
chartImage = 'img/Dizzy.png'

# Left hand column, contains all the buttons
ButtonSelectColumn = [
    [sg.CalendarButton(button_text='date from', key='dateToBtn', target='dateFromTxt', format="%Y-%m-%d"),
     sg.Text(text=datetime.date.today(), key='dateFromTxt')],
    [sg.Text('to')],
    [sg.CalendarButton(button_text='date to', key='dateFromBtn', target='dateToTxt', format="%Y-%m-%d"),
     sg.Text(text=datetime.date.today(), key='dateToTxt')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Suburb')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Cleanliness')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Keyword')],
    [sg.InputText()],
    [sg.HSeparator()],
    [sg.Button(button_text='by Name')],
    [sg.InputText()],
    [sg.HSeparator()],
    [sg.Button(button_text='by Price', key='priceBtn')]
]

# Right hand column, will contain the generated chart images
ImageColumn = [
    [sg.Text('Test text 1')],
    [sg.Text('Test text 2')]
]

# Main window layout, left column, vertical separator and right column
mainLayout = [
    [
        sg.Column(ButtonSelectColumn),
        sg.VSeparator(),
        sg.Column(ImageColumn)
    ]
]


# Creating new window
mainWindow = sg.Window('DigiBird Eyeview v0.01', mainLayout)

def SetChartImage(dateFrom, dateUntil):
    print(dateFrom, dateUntil)
    global chartImage
    # setting the desired path to find the chart image
    chartImage = ('img/' + mainWindow['dateFromTxt'].get() + '-' + mainWindow['dateToTxt'].get() + 'Price.png')
    # Checking if that image exists, if it doesn't, defaulting to an error image
    if not os.path.isfile(chartImage):
        chartImage = "img/Dizzy.png"

# Loop to process events while application is running
while True:
    event, values = mainWindow.read()
    if event == "priceBtn":
        SetChartImage('ok', 'hello')
        sg.popup('meowdy', image=chartImage)
    if event == sg.WIN_CLOSED: # if user closes window
        print('Application exited')
        break


mainWindow.close()