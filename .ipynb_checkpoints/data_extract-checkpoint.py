import json
from bs4 import BeautifulSoup
import requests

def consider_text(text):
    # print(text)
    return 'Sign in' not in text and 'min read' not in text

def get_article_text(url):
    
    story_page = requests.get(url)
    story_soup = BeautifulSoup(story_page.text, 'html.parser')
    
    tags = story_soup.find_all(['p', 'ol', 'ul', 'h2'])
    
    texts = [t.text for t in tags if consider_text(t.text)]
    
    texts = ' '.join(texts)
    content = texts.split('Ramsri Goutham') if 'Ramsri Goutham' in texts else texts.split('Murali M K')
    return content[1].strip()

if __name__ == '__main__':
    
    # Getting article urls
    url = 'https://ramsrigoutham.medium.com/'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    links = []
    for tag in soup.find_all('a'):
        links.append(tag['href'])

    links = [x for x in links if str.startswith(x, 'https://towardsdatascience.com/') \
             and not str.startswith(x, 'https://towardsdatascience.com/?source=user_profile')]
    links = [x.split('?')[0] for x in links]
    links = list(set(links))

    links.remove('https://towardsdatascience.com/how-to-properly-use-the-gpu-within-a-docker-container-4c699c78c6d1')
    links.append('https://towardsdatascience.com/practical-tips-for-beginners-in-data-science-debunking-few-myths-30537117a4e4')
    
    print('Articles getting scraped...')
    print(links)
    
    data = {}
    for link in links:
        key = link.split('/')[-1]
        print(f'Scraping: {key}')
        data[key] = get_article_text(link)
    
    with open('data/medium_scraped_data.json', 'w') as fp:
        json.dump(data, fp)
    
    print(f'Data stored in data/medium_scraped_data.json')
    