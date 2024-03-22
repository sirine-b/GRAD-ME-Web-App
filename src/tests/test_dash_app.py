import requests
import time
from dash.testing.application_runners import import_app
from selenium import webdriver

#driver = webdriver.Chrome(executable_path=r'C:\Users\sirin\Downloads\chrome-win32\chrome-win32\chrome.exe')


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