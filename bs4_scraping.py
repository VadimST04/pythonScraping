from bs4 import BeautifulSoup
import requests


def bs4_config(path=''):
    root_url = 'https://subslikescript.com/'
    website = f'{root_url}{path}'
    content = requests.get(website).text
    return BeautifulSoup(content, 'lxml')


def main():
    soup = bs4_config('movies')
    last_page = soup.select_one('li.page-item:nth-last-child(2)').get_text()
    for page in range(1, int(last_page) + 1):
        soup = bs4_config(f'movies?page={page}')
        box = soup.find('article', class_='main-article')
        links = [link['href'] for link in box.find_all('a')]

        for link in links:
            soup = bs4_config(link)
            box = soup.find('article', class_='main-article')
            title = box.find('h1').get_text()
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

            with open(f'{title}.txt', mode='w', encoding='utf-8') as file:
                file.write(transcript)


if __name__ == '__main__':
    main()
