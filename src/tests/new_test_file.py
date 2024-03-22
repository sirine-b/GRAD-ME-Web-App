import time
def test_new_file(dash_br):
    dash_br.server_url="http://127.0.0.1:8050/"
    dash_br.wait_for_element("h1", timeout=4)
    time.sleep(2)
    # Find the text content of the H1 heading element
    h1_text = dash_br.find_element("h1").text
    assert h1_text=='hey'