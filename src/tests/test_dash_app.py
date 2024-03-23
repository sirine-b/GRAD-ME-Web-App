import requests
import time
from dash.testing.application_runners import import_app
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

#driver = webdriver.Chrome(executable_path=r'C:\Users\sirin\Downloads\chrome-win32\chrome-win32\chrome.exe')


# def test_server_live(dash_duo):

#     """
#     GIVEN the app is running
#     WHEN a HTTP request to the home page is made
#     THEN the HTTP response status code should be 200
#     """

#     # Start the server with the app using the dash_duo fixture
#     app = import_app(app_file="src.app")
#     dash_duo.start_server(app)

#     # Delay to wait 2 seconds for the page to load
#     dash_duo.driver.implicitly_wait(2)

#     # Get the url for the web app root
#     url = dash_duo.driver.current_url
#     print(f'The server url is {url}')

#     # Make an HTTP GET request to the sever url
#     response = requests.get(url)

#     # Use pytest assertion to check that the status code in the HTTP response is 200 (i.e. success)
#     assert response.status_code == 200

# def test_app_header(dash_duo):
#     """
#     GIVEN the app is running
#     WHEN the home page is available
#     THEN the H1 heading text should be "Welcome to GRAD:ME! Dashboard !!!"
#     """
#     app = import_app(app_file="src.app")
#     dash_duo.start_server(app)

#     # Wait for the H1 heading to be visible, timeout if this does not happen within 4 seconds
#     dash_duo.wait_for_element("h1", timeout=4)

#     # Find the text content of the H1 heading element
#     h1_text = dash_duo.find_element("h1").text

#     # Check the heading has the text we expect
#     assert h1_text == "Welcome to GRAD:ME! Dashboard !!!"


def test_select_course_filters(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading text should be "Welcome to GRAD:ME! Dashboard !!!"
    """
    app = import_app(app_file="src.app")
    dash_duo.start_server(app)

    # Wait for the kis_mode_select heading to be visible, timeout if this does not happen within 4 seconds
    #dash_duo.wait_for_element(By.ID, "kis_mode_select",timeout=4)
    # dash_duo.wait_for_element(By.CSS_SELECTOR,"satisfaction_indicators > div.js-plotly-plot > div > div > svg:nth-child(3) > g.indicatorlayer > g:nth-child(1) > g.numbers > text",timeout=4)

    sat_meaningfulness_before=dash_duo.driver.find_element(By.CSS_SELECTOR,"satisfaction_indicators > div.js-plotly-plot > div > div > svg:nth-child(3) > g.indicatorlayer > g:nth-child(1) > g.numbers > text")
    #check that the correct value of the first satisfaction indicator is displayed for the default filter values
    print(sat_meaningfulness_before)
    print(type(sat_meaningfulness_before))
    assert sat_meaningfulness_before==str('60.2%')
    
    # #conduct a chain of user actions to simulate the user selecting the 3 course filters
    # course_software_eng=dash_duo.driver.find_element(By.CSS_SELECTOR, "course_name_select > option:nth-child(11)")
    # kis_mode_part_time = dash_duo.driver.find_element(By.CSS_SELECTOR,"_dbcprivate_radioitems_kis_mode_select_input_2")
    # kis_level_four=dash_duo.driver.find_element(By.CSS_SELECTOR,"#_dbcprivate_radioitems_kis_level_select_input_4")
    # # "kis_mode_select > div:nth-child(2) > label"
    # kis_mode_part_time.click()
    # #press the search button
    # search_button=dash_duo.driver.find_element(By.CSS_SELECTOR,"search_button")



