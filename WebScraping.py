import requests
from bs4 import BeautifulSoup


def webscraping_from_department_of_transportation():
    url = 'https://teen.kolzchut.org.il/he/%D7%96%D7%9B%D7%95%D7%AA:%D7%A0%D7%94%D7%92_%D7%97%D7%93%D7%A9'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        text = soup.find('body').get_text()

        return text

    else:
        return "Failed to fetch data from the website."
