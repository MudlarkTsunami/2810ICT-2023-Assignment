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
reviewsHeaders = ['listing id', 'id', 'date', 'reviewer id', 'reviewer name', 'comments']
suburbHeaders = ['id', 'listing_url', 'scrape_id', 'last_scraped', 'name', 'summary', 'space', 'description',
                 'experiences_offered', 'neighborhood_overview', 'notes', 'transit', 'access',
                 'interaction', 'house_rules', 'thumbnail_url', 'medium_url', 'picture_url',
                 'xl_picture_url', 'host_id', 'host_url', 'host_name', 'host_since', 'host_location',
                 'host_about', 'host_response_time', 'host_response_rate', 'host_acceptance_rate',
                 'host_is_superhost', 'host_thumbnail_url', 'host_picture_url', 'host_neighbourhood',
                 'host_listings_count', 'host_total_listings_count', 'host_verifications',
                 'host_has_profile_pic', 'host_identity_verified', 'street', 'neighbourhood',
                 'neighbourhood_cleansed', 'neighbourhood_group_cleansed', 'city', 'state',
                 'zipcode', 'market', 'smart_location', 'country_code', 'country', 'latitude',
                 'longitude', 'is_location_exact', 'property_type', 'room_type', 'accommodates',
                 'bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities', 'square_feet', 'price',
                 'weekly_price', 'monthly_price', 'security_deposit', 'cleaning_fee', 'guests_included',
                 'extra_people', 'minimum_nights', 'maximum_nights', 'calendar_updated', 'has_availability',
                 'availability_30', 'availability_60', 'availability_90', 'availability_365',
                 'calendar_last_scraped', 'number_of_reviews', 'first_review', 'last_review',
                 'review_scores_rating', 'review_scores_accuracy', 'review_scores_cleanliness',
                 'review_scores_checkin', 'review_scores_communication', 'review_scores_location',
                 'review_scores_value', 'requires_license', 'license', 'jurisdiction_names',
                 'instant_bookable', 'is_business_travel_ready', 'cancellation_policy',
                 'require_guest_profile_picture', 'require_guest_phone_verification',
                 'reviews_per_month', 'date', 'available']
keywordHeaders = ['id', 'summary', 'space', 'description', 'date', 'available', 'price']
cleanlinessHeaders = ['listing id', 'positive keywords', 'negative keywords', 'positive keyword %']
blankHeaders = list(range(1, 100))

# Loading the CSV files into dataframes
reviews_dataframe = pd.read_csv("Data/reviews_dec18.csv")
listings_dataframe = pd.read_csv("Data/listings_dec18.csv", low_memory=False)
calendar_dataframe = pd.read_csv("Data/calendar_dec18.csv")

# Left hand column, contains all the buttons
button_select_column = [
    [sg.CalendarButton(button_text='date from', key='dateToBtn', target='dateFromTxt', format="%d/%m/%Y"),
     sg.Text(text=datetime.date.today().strftime("%d/%m/%Y"), key='dateFromTxt')],

    [sg.Text('to')],

    [sg.CalendarButton(button_text='date to', key='dateFromBtn', target='dateToTxt', format="%d/%m/%Y"),
     sg.Text(text=datetime.date.today().strftime("%d/%m/%Y"), key='dateToTxt')],

    [sg.HSeparator(pad=((5, 5), (20, 20)))],

    [sg.Button(button_text='by Suburb', key='suburbBtn')],

    [sg.InputText(key='bySuburbInput')],

    [sg.HSeparator(pad=((5, 5), (20, 20)))],

    [sg.Button(button_text='by Cleanliness', key='byCleanBtn')],

    [sg.HSeparator(pad=((5, 5), (20, 20)))],

    [sg.Button(button_text='by Keyword', key='byKeywordBtn')],

    [sg.InputText(key='byKeywordInput')],

    [sg.HSeparator(pad=((5, 5), (20, 20)))],

    [sg.Button(button_text='by Name', key='byNameBtn')],

    [sg.InputText(key='byNameInput')],

    [sg.HSeparator(pad=((5, 5), (20, 20)))],

    [sg.Button(button_text='by Price', key='priceBtn')]
]

# Right hand column, will contain the table information
table_column = [
    [sg.Table(values=[[]], headings=blankHeaders, def_col_width=15,
              num_rows=15, auto_size_columns=False, vertical_scroll_only=False, key='dataTable')]
]

# Main window layout, left column, vertical separator and right column
main_layout = [
    [
        sg.Column(button_select_column, size=(150, 600)),
        sg.VSeparator(),
        sg.Column(table_column)
    ]
]

# Creating new window
mainWindow = sg.Window('DigiBird Eyeview v0.1', main_layout, size=(800, 600))


def SetChartImage(date_from, date_until):
    """
    Generates a price chart image within the given dates, and sets this as the application's chart image
    :param date_from: date from
    :param date_until: date until
    :return: none
    """
    print(date_from, date_until)
    priceDist.generate_date_distribution(calendar_dataframe, date_from, date_until)
    global chartImage
    # setting the desired path to find the chart image
    chartImage = 'img/price_distributionlive.png'
    im = Image.open(chartImage)
    width, height = im.size
    im.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    im.save(chartImage)
    # Checking if that image exists, if it doesn't, defaulting to an error image
    if not os.path.isfile(chartImage):
        chartImage = "img/Dizzy.png"


def ListByName(name_given):
    """
    Provides a 2D array of listings with an author name that matches the given name
    :param name_given: name given
    :return: 2D array
    """
    # Getting the dataframe filtered by name
    temporary_table_data_frame = custrev.reviews_by_name(reviews_dataframe, name_given)
    # Converting the dataframe to a numpy array
    temporary_table_array = (pd.DataFrame.to_numpy(temporary_table_data_frame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporary_table_array = numpy.ndarray.tolist(temporary_table_array)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporary_table_array.insert(0, reviewsHeaders)
    return temporary_table_array


def ListByCleanliness():
    """
    Provides a 2D array of listings with details about their cleanliness
    :return: 2D array
    """
    # Getting the dataframe filtered by name
    temporary_table_data_frame = cleans.find_by_cleanliness(reviews_dataframe)
    # Converting the dataframe to a numpy array
    temporary_table_array = (pd.DataFrame.to_numpy(temporary_table_data_frame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporary_table_array = numpy.ndarray.tolist(temporary_table_array)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporary_table_array.insert(0, cleanlinessHeaders)
    return temporary_table_array


def ListBySuburb(suburb_given, start_date, end_date):
    """
    Provides a 2D array of listings in the given suburb within the given dates
    :param suburb_given: suburb given
    :param start_date: start date
    :param end_date: end date
    :return: 2D array
    """
    # Getting the dataframe filtered by suburb and dates
    temporary_table_data_frame = suburbs.find_suburb_listings(listings_dataframe, calendar_dataframe, suburb_given,
                                                              start_date, end_date)
    # Converting the dataframe to a numpy array
    temporary_table_array = (pd.DataFrame.to_numpy(temporary_table_data_frame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporary_table_array = numpy.ndarray.tolist(temporary_table_array)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporary_table_array.insert(0, suburbHeaders)
    return temporary_table_array


def ListByKeyword(keyword_given, start_date, end_date):
    """
    Provides a 2D array of listings that contain a given keyword within the given dates
    :param keyword_given: keyword given
    :param start_date: start date
    :param end_date: end date
    :return: 2D array
    """
    # Getting the dataframe filtered by keyword and dates
    temporary_table_data_frame = listingKey.find_keyword_listings(listings_dataframe, calendar_dataframe,
                                                                  keyword_given, start_date, end_date)
    # Converting the dataframe to a numpy array
    temporary_table_array = (pd.DataFrame.to_numpy(temporary_table_data_frame))
    # Converting the numpy array into a normal array (conversion straight to a list was not possible)
    temporary_table_array = numpy.ndarray.tolist(temporary_table_array)
    # Inserting header labels as the first row (changing table headers with pysimplegui is not possible)
    temporary_table_array.insert(0, keywordHeaders)
    return temporary_table_array


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
        mainWindow['dataTable'].update(values=ListBySuburb(values['bySuburbInput'], mainWindow['dateFromTxt'].get(),
                                                           mainWindow['dateToTxt'].get()))

    if event == "byKeywordBtn":
        print('start date' + mainWindow['dateFromTxt'].get())
        print('end date' + mainWindow['dateToTxt'].get())
        mainWindow['dataTable'].update(values=ListByKeyword(values['byKeywordInput'], mainWindow['dateFromTxt'].get(),
                                                            mainWindow['dateToTxt'].get()))

    if event == sg.WIN_CLOSED:  # if user closes window
        print('Application exited')
        break

mainWindow.close()