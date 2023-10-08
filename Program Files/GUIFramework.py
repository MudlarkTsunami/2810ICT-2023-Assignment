import datetime
import os.path
import numpy
import Customer_Reviews as custrev
import pandas as pd
import PySimpleGUI as sg

# Changing the default theme to a darker one
sg.theme('DarkAmber')
# Default value of the chart image points to an error image
chartImage = 'img/Dizzy.png'
# Lists of table headers
# REMOVE This list may no longer be required
tableHeaders = ['id', 'name', 'host id', 'host name', 'neighbourhood', 'latitude', 'longitude', 'room type', 'price',
                'minimum nights', 'number of reviews', 'last review', 'reviews per month', 'availability 365',
                'date', 'available']
# Clean looking headers for each of the data sets
reviewsHeaders = ['listing id','id','date','reviewer id','reviewer name','comments']



# sample table data for testing, to be removed
sampleTable = [['1', 2, '5', '6','ok','whatever you want dude'], ['3', '4'], ['5', '6']]

id_reviews_df = pd.read_csv("Data/reviews_dec18.csv")




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
    [sg.Button(button_text='by Name', key='byNameBtn')],
    [sg.InputText(key='byNameInput')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Price', key='priceBtn')]
]



# Right hand column, will contain the table information
ImageColumn = [
    # REMOVE Planned to use one set of data and therefore only one set of headers, this may not be possible due to how the other files are structured
    # [sg.Table(headings=tableHeaders, values= sampleTable, def_col_width=15, auto_size_columns=False, vertical_scroll_only=False, key='dataTable')]
[sg.Table(values=sampleTable, headings=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], def_col_width=15,
          num_rows=15, auto_size_columns=False, vertical_scroll_only=False, key='dataTable')]
]

# Main window layout, left column, vertical separator and right column
mainLayout = [
    [
        sg.Column(ButtonSelectColumn, size=(150,600)),
        sg.VSeparator(),
        sg.Column(ImageColumn)
    ]
]


# Creating new window
mainWindow = sg.Window('DigiBird Eyeview v0.1', mainLayout, size=(800, 600))


def SetChartImage(dateFrom, dateUntil):
    print(dateFrom, dateUntil)
    global chartImage
    # setting the desired path to find the chart image
    chartImage = ('img/' + mainWindow['dateFromTxt'].get() + ',' + mainWindow['dateToTxt'].get() + ',Price.png')
    # Checking if that image exists, if it doesn't, defaulting to an error image
    if not os.path.isfile(chartImage):
        chartImage = "img/Dizzy.png"


def ListByName(nameGiven):
    temporaryTableDataFrame = custrev.reviews_by_name(id_reviews_df, nameGiven)
    temporaryTableArray = (pd.DataFrame.to_numpy(temporaryTableDataFrame))
    temporaryTableArray = numpy.ndarray.tolist(temporaryTableArray)
    temporaryTableArray.insert(0, reviewsHeaders)
    return temporaryTableArray

# Loop to process events while application is running
while True:
    event, values = mainWindow.read()
    if event == "priceBtn":
        SetChartImage('ok', 'hello')
        sg.popup('meowdy', image=chartImage)

    if event == "byNameBtn":
        mainWindow['dataTable'].update(values=ListByName(values['byNameInput']))

    if event == sg.WIN_CLOSED: # if user closes window
        print('Application exited')
        break


mainWindow.close()