import datetime
import os.path
import numpy
import Customer_Reviews as custrev
import Suburb_Listings as suburbs
import Keyword as listingKey
import Price_Distribution as priceDist
import Cleanliness as cleans
import pandas as pd
import PySimpleGUI as sg
from PIL import Image

# Changing the default theme to a darker one
sg.theme('DarkAmber')
# Default value of the chart image points to an error image
chartImage = 'img/Dizzy.png'
# Lists of table headers
# Clean looking headers for each of the data sets
reviewsHeaders = ['listing id','id','date','reviewer id','reviewer name','comments']
suburbHeaders = ['id','listing_url','scrape_id','last_scraped','name','summary','space','description',
                  'experiences_offered','neighborhood_overview','notes','transit','access',
                  'interaction','house_rules','thumbnail_url','medium_url','picture_url',
                  'xl_picture_url','host_id','host_url','host_name','host_since','host_location',
                  'host_about','host_response_time','host_response_rate','host_acceptance_rate',
                  'host_is_superhost','host_thumbnail_url','host_picture_url','host_neighbourhood',
                  'host_listings_count','host_total_listings_count','host_verifications',
                  'host_has_profile_pic','host_identity_verified','street','neighbourhood',
                  'neighbourhood_cleansed','neighbourhood_group_cleansed','city','state',
                  'zipcode','market','smart_location','country_code','country','latitude',
                  'longitude','is_location_exact','property_type','room_type','accommodates',
                  'bathrooms','bedrooms','beds','bed_type','amenities','square_feet','price',
                  'weekly_price','monthly_price','security_deposit','cleaning_fee','guests_included',
                  'extra_people','minimum_nights','maximum_nights','calendar_updated','has_availability',
                  'availability_30','availability_60','availability_90','availability_365',
                  'calendar_last_scraped','number_of_reviews','first_review','last_review',
                  'review_scores_rating','review_scores_accuracy','review_scores_cleanliness',
                  'review_scores_checkin','review_scores_communication','review_scores_location',
                  'review_scores_value','requires_license','license','jurisdiction_names',
                  'instant_bookable','is_business_travel_ready','cancellation_policy',
                  'require_guest_profile_picture','require_guest_phone_verification',
                  'reviews_per_month','date','available']
keywordHeaders = ['id','summary','space','description','date', 'available', 'price']
cleanlinessHeaders = ['listing id','positive keywords','negative keywords','positive keyword %']
blankHeaders = list(range(1,100))

# sample table data for testing, to be removed
sampleTable = [['1', 2, '5', '6','ok','whatever you want dude'], ['3', '4'], ['5', '6']]

id_reviews_df = pd.read_csv("Data/reviews_dec18.csv")
listings_df = pd.read_csv("Data/listings_dec18.csv")
calendar_df = pd.read_csv("Data/calendar_dec18.csv")



# Left hand column, contains all the buttons
ButtonSelectColumn = [
    [sg.CalendarButton(button_text='date from', key='dateToBtn', target='dateFromTxt', format="%d/%m/%Y"),
     sg.Text(text=datetime.date.today().strftime("%d/%m/%Y"), key='dateFromTxt')],
    [sg.Text('to')],
    [sg.CalendarButton(button_text='date to', key='dateFromBtn', target='dateToTxt', format="%d/%m/%Y"),
     sg.Text(text=datetime.date.today().strftime("%d/%m/%Y"), key='dateToTxt')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Suburb',key='suburbBtn')],
    [sg.InputText(key='bySuburbInput')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Cleanliness',key='byCleanBtn')],
    [sg.HSeparator()],
    [sg.Button(button_text='by Keyword', key='byKeywordBtn')],
    [sg.InputText(key='byKeywordInput')],
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
[sg.Table(values=sampleTable, headings=blankHeaders, def_col_width=15,
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
    priceDist.generate_date_distribution(calendar_df,dateFrom,dateUntil)
    global chartImage
    # setting the desired path to find the chart image
    chartImage = 'img/price_distributionlive.png'
    im = Image.open(chartImage)
    width, height = im.size
    im.thumbnail((1200,1200), Image.Resampling.LANCZOS)
    im.save(chartImage)
    # Checking if that image exists, if it doesn't, defaulting to an error image
    if not os.path.isfile(chartImage):
        chartImage = "img/Dizzy.png"


def ListByName(nameGiven):
    # Getting the dataframe filtered by name
    temporaryTableDataFrame = custrev.reviews_by_name(id_reviews_df, nameGiven)
    # Converting the dataframe to a numpy array
    temporaryTableArray = (pd.DataFrame.to_numpy(temporaryTableDataFrame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporaryTableArray = numpy.ndarray.tolist(temporaryTableArray)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporaryTableArray.insert(0, reviewsHeaders)
    return temporaryTableArray


def ListByCleanliness():
    # Getting the dataframe filtered by name
    temporaryTableDataFrame = cleans.find_by_cleanliness(id_reviews_df)
    # Converting the dataframe to a numpy array
    temporaryTableArray = (pd.DataFrame.to_numpy(temporaryTableDataFrame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporaryTableArray = numpy.ndarray.tolist(temporaryTableArray)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporaryTableArray.insert(0, cleanlinessHeaders)
    return temporaryTableArray


def ListBySuburb(suburbGiven, startDate, endDate):
    # Getting the dataframe filtered by suburb and dates
    temporaryTableDataFrame = suburbs.find_suburb_listings(listings_df,calendar_df,suburbGiven,startDate,endDate)
    # Converting the dataframe to a numpy array
    temporaryTableArray = (pd.DataFrame.to_numpy(temporaryTableDataFrame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporaryTableArray = numpy.ndarray.tolist(temporaryTableArray)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporaryTableArray.insert(0, suburbHeaders)
    return temporaryTableArray


def ListByKeyword(keywordGiven, startDate, endDate):
    # Getting the dataframe filtered by keyword and dates
    temporaryTableDataFrame = listingKey.find_keyword_listings(listings_df,calendar_df,keywordGiven,startDate,endDate)
    # Converting the dataframe to a numpy array
    temporaryTableArray = (pd.DataFrame.to_numpy(temporaryTableDataFrame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporaryTableArray = numpy.ndarray.tolist(temporaryTableArray)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporaryTableArray.insert(0, keywordHeaders)
    return temporaryTableArray


# Loop to process events while application is running
while True:
    event, values = mainWindow.read()
    if event == "priceBtn":
        SetChartImage(mainWindow['dateFromTxt'].get(), mainWindow['dateToTxt'].get())
        sg.popup('Price Chart', image=chartImage)

    if event == "byNameBtn":
        mainWindow['dataTable'].update(values=ListByName(values['byNameInput']))

    if event == "byCleanBtn":
        mainWindow['dataTable'].update(values=ListByCleanliness())

    if event == "suburbBtn":
        print('start date' + mainWindow['dateFromTxt'].get())
        print('end date' + mainWindow['dateToTxt'].get())
        mainWindow['dataTable'].update(values=ListBySuburb(values['bySuburbInput'], mainWindow['dateFromTxt'].get(), mainWindow['dateToTxt'].get()))

    if event == "byKeywordBtn":
        print('start date' + mainWindow['dateFromTxt'].get())
        print('end date' + mainWindow['dateToTxt'].get())
        mainWindow['dataTable'].update(values=ListByKeyword(values['byKeywordInput'], mainWindow['dateFromTxt'].get(), mainWindow['dateToTxt'].get()))

    if event == sg.WIN_CLOSED: # if user closes window
        print('Application exited')
        break


mainWindow.close()