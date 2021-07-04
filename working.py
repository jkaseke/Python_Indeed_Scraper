import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=data+engineer&&sort=date&start={page}'
    r = requests.get(url,headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('h2').text.strip('new')
        company = item.find('span', class_ = 'companyName').text
        location = item.find('div', class_ = 'companyLocation').text
        try:
            salary = item.find('span', class_ ='salary-snippet').text
        except:
            salary = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n', ' ')

        job = {
            'title': title,
            'company': company,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        joblist.append(job)
    return

joblist = []

for i in range(0,40,10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')