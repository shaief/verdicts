import requests
from bs4 import BeautifulSoup

def empty_bullshit(user_soup):
    for script in user_soup.find_all('script'):
        script.extract()
    for script in user_soup.find_all('ins'):
        script.extract()
    for script in user_soup.find_all('div', attrs={u'id':u'google_ads_frame1'}):
        script.extract()
    return user_soup.get_text('\n')

def html_cleanup(raw_html):
    new_html = []
    for i, word in enumerate(raw_html[0:-7]):
            if len(word) == 7:
                if word[0:4].isdigit() and word[4] == '/' and word[5:8].isdigit():
                    # print (word,)
                    word = '[[{}]]'.format(word)
                    # print (word)
            new_html.append(word)

    cleaned_html = ' '.join(new_html)
    # print (cleaned_html)
    return cleaned_html


header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
website = raw_input('Please enter website address: ')
r = requests.get(website, headers=header)

soup = BeautifulSoup(r.content)

days_links = []

for link in soup.find_all('a'):
    if link.get('href')[0:4].isdigit() and not link.get('href')[4].isdigit():
        days_links.append(link.get('href'))

verdict_links = []
for i, link in enumerate(days_links):
    # if i != 10:
    #     continue
    # if i == 10:
    r = requests.get('{}{}'.format(website, link), headers=header)
    soup = BeautifulSoup(r.content)
    print (link)



    for verdict_link in soup.find_all('a'):
        if verdict_link.get('href')[0:5].isdigit():
            verdict_links.append(verdict_link.get('href'))

    for j, verdict in enumerate(verdict_links):
        # if j > 0:
        #     break
        print (verdict)
        r = requests.get('{}{}'.format(website, verdict), headers=header)
        soup = BeautifulSoup(r.content)
        title = soup.title.string
        raw_html = empty_bullshit(soup)
        text = html_cleanup(raw_html)
        with open(file='./verdicts/{}{}'.format(verdict[0:-4], 'md'), mode='w', encoding='utf-8') as f:
            f.write(title)
            f.write(raw_html)
