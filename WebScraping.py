import requests
from bs4 import BeautifulSoup


def web_scraping_from_department_of_transportation():
    url = 'https://www.gov.il/he/pages/new_driver'
    response = requests.get(url)
    print("hgh")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the webpage
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the specific elements containing the regulations, limitations, and offenses text
        regulations_element = soup.find('div', {'id': 'gtm-headscript_GTM-TQNJKX'})
        limitations_element = soup.find('div', {'id': 'officeAnalyticsTrackingCode'})
        offenses_element = soup.find('div', {'id': 'gtm-headscript_GTM-T2THFL3'})

        # Extract the text from the elements
        regulations_text = regulations_element.get_text('\n',
                                                        strip=True) if regulations_element else "Regulations not found"
        limitations_text = limitations_element.get_text('\n',
                                                        strip=True) if limitations_element else "Limitations not found"
        offenses_text = offenses_element.get_text('\n', strip=True) if offenses_element else "Offenses not found"
        return regulations_text+limitations_text+offenses_text

    else:
        return "Failed to fetch data from the website."
