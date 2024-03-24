import requests
import time
from dash.testing.application_runners import import_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

def test_server_live(dash_duo):

    """
    GIVEN the app is running
    WHEN a HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the server with the app using the dash_duo fixture
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    url = dash_duo.driver.current_url
    print(f'The server url is {url}')

    # Make an HTTP GET request to the sever url
    response = requests.get(url)

    # Use pytest assertion to check that the status code in the HTTP response is 200 (i.e. success)
    assert response.status_code == 200

def test_app_header(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading text should be "Welcome to GRAD:ME! Dashboard !!!"
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text

    # Check the heading has the text we expect
    assert h1_text == "Welcome to GRAD:ME! Dashboard !!!"


def test_select_course_filters(dash_duo):
    """
    GIVEN the app is running
    THEN the value of the first satisfaction indicator should be 60.2% for the default filter values (i.e. Design Studies + Full-Time + Kis mode 3)
    WHEN the user selects new filter options (e.g. Software Engineering + Full-Time + Kis mode 4)
    THEN the value of the first satisfaction indicator should be 68.9%
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the search to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("#search_button", timeout=4)

    # Check that the correct value of the first satisfaction indicator is displayed for the default filter values
    sat_indicator_one_start=dash_duo.find_element("#satisfaction_indicators > div.js-plotly-plot > div > div > svg:nth-child(3) > g.indicatorlayer > g:nth-child(3) > g.numbers")
    assert sat_indicator_one_start.text==str('60.2%')

    # Define the different filter options/buttons that will be selected by the user
    kis_level_four=dash_duo.find_element('#_dbcprivate_radioitems_kis_level_select_input_3')
    course_software_eng=dash_duo.find_element('#course_name_select > option:nth-child(11)')
    search_button=dash_duo.find_element('#search_button')

    # Simulate the user clicking on the above filter options
    kis_level_four.click()
    course_software_eng.click()
    search_button.click()

    # Check that the correct value of the first satisfaction indicator is displayed after the new filter options have been selected
    sat_indicator_one_end=dash_duo.find_element("#satisfaction_indicators > div.js-plotly-plot > div > div > svg:nth-child(3) > g.indicatorlayer > g:nth-child(1) > g.numbers")
    assert sat_indicator_one_end.text==str('69.8%')

def test_select_countries(dash_duo):
    """
    GIVEN the app is running
    THEN the bar plot should only display salary data for the UK (as it is the only country selected by default)
    WHEN the user selects additional countries
    THEN the bar plot should display the salary data for all the selected countries
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the search to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("#search_button", timeout=4)

    # Check that only salary data for the UK is displayed for the default filter values (i.e. before the user makes any selections)
    countries_before=dash_duo.find_element('#bar_chart > div.js-plotly-plot > div > div > svg:nth-child(1) > g.cartesianlayer > g > g.xaxislayer-above > g')
    assert countries_before.text == str('UK')

    # Define the different country options that will be selected by the user
    wales_selector=dash_duo.find_element('#countries_select > div:nth-child(4) > label')
    
    # Simulate the user clicking on additional countries (i.e.Wales) on the multiselector filter
    wales_selector.click()

    # Check that the correct value of the first satisfaction indicator is displayed after the new filter options have been selected
    countries_after=dash_duo.find_element('#bar_chart > div.js-plotly-plot > div > div > svg:nth-child(1) > g.cartesianlayer > g > g.xaxislayer-above')
    assert countries_after.text== 'UK\nWales'

def test_error_messages(dash_duo):
    """
    GIVEN the app is running
    WHEN the user deselects all countries
    THEN an error message should be displayed next to the bar plot to ask the user to select a country
    WHEN the user selects a combination of course options for which no data is available (e.g. )
    THEN an error message should be displayed on the top right of web app
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the search to be visible, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("#search_button", timeout=4)

    # Check that no error message is displayed when a correct combination of course filters is selected
    assert dash_duo.find_element('#errors > div') == False
     

    # Define the different filter options/buttons that will be selected by the user (inexistent combination)
    kis_level_four=dash_duo.find_element('#_dbcprivate_radioitems_kis_level_select_input_3')
    microbiology_course=dash_duo.find_element('#course_name_select > option:nth-child(117)')
    search_button=dash_duo.find_element('#search_button')

    # Simulate the user clicking on the above filter options
    kis_level_four.click()
    microbiology_course.click()
    search_button.click()  

    error_message_after=dash_duo.find_element('#errors > div')
    assert error_message_after.text=='Sorry, no data is currently available for the selected\
          course options. We will try our best to add it to our database soon! Please select \
            a different study mode, kis level or course name.'