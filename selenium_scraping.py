from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas


def main():
    """
    This function uses the Selenium library to scrape data about football matches and then converts
    data to csv file.
    :return: None
    """
    website = 'https://www.adamchoi.co.uk/overs/detailed'
    path = 'C:/Users/Вадим/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
    service = Service(executable_path=path)

    with webdriver.Chrome(service=service) as driver:
        driver.get(website)
        driver.find_element(by='xpath', value='//label[@analytics-event="All matches"]').click()
        driver.find_element(by='id', value='country').click()
        driver.find_element(by='xpath', value='//option[@value="object:75"]').click()

        date = [date.text for date in driver.find_elements(by='xpath', value='//tr/td[1]')]
        home_team = [date.text for date in driver.find_elements(by='xpath', value='//tr/td[2]')]
        score = [date.text for date in driver.find_elements(by='xpath', value='//tr/td[3]')]
        away_team = [date.text for date in driver.find_elements(by='xpath', value='//tr/td[4]')]

        df = pandas.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
        df.to_csv('football_data.csv', index=False)


if __name__ == '__main__':
    main()
