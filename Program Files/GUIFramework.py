import datetime
import PySimpleGUI as sg

#Changing the default theme to a darker one
sg.theme('DarkAmber')

#Left hand column, contains all the buttons
ButtonSelectColumn = [
    [sg.CalendarButton(button_text='date from', key='dateToBtn', target='dateToTxt', format="%Y-%m-%d"),
     sg.Text(text=datetime.date.today(), key='dateToTxt')],
    [sg.Text('to')],
    [sg.CalendarButton(button_text='date to', key='dateFromBtn', target='dateFromTxt', format="%Y-%m-%d"),
     sg.Text(text=datetime.date.today(), key='dateFromTxt')],
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
    [sg.Button(button_text='by Price')]
]

# Right hand column, will contain the generated chart images
ImageColumn = [
    [sg.Text('Test text 1')],
    [sg.Text('Test text 2')]
]

# Window layout, left column, vertical separator and right column
layout = [
    [
        sg.Column(ButtonSelectColumn),
        sg.VSeparator(),
        sg.Column(ImageColumn)
    ]
]

# Creating new window
window = sg.Window('DigiBird Eyeview v0.01', layout)

# Loop to process events while application is running
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window
        print('Application exited')
        break


window.close()