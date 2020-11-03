import urllib
import requests
from bs4 import BeautifulSoup
import json

url = "https://iptvxtreamcodes.com/free-stbemu-portalmac-and-iptv-xtream-codesiptv-m3u-playlists-02-11-2020/"
platform = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
headers = {"user-agent": platform}
response = requests.get(url, headers=headers)

result = []
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    for elem in soup.find_all('h4'):
        if any("LIVE" in content for content in elem.contents):
            result.append(elem.contents)


def search(array):
    if any("AFRICA" in elem for elem in array) or any("Africa" in elem for elem in array) or any("africa" in elem for elem in array):
        return True
    return False

def build_dict(content):
    m3u_elem = [string for string in content if 'type=m3u' in string]
    if len(m3u_elem) == 0:
        return None
    m3u_string = m3u_elem[0]
    url = [string for string in m3u_string.split(' ') if 'http://' in string][0]
    if "username" not in url or "password" not in url:
        return None
    url_string = "http://"+url.split('?')[0].split('/')[2]
    username = url.split("?")[1].split('&')[0].split('=')[1]
    password = url.split("?")[1].split('&')[1].split('=')[1]
    return {
        "url": url_string,
        "username": username,
        "password": password
    }

def build_url(content):
    m3u_elem = [string for string in content if 'type=m3u' in string]
    if len(m3u_elem) == 0:
        return None
    m3u_string = m3u_elem[0]
    url = [string for string in m3u_string.split(
        ' ') if 'http://' in string][0]
    if "username" not in url or "password" not in url:
        return None
    return url

african_accounts = list(filter(search, result))

list_of_good_accounts = [build_dict(account) for account in african_accounts if build_dict(account) != None]
list_of_good_urls = [build_url(account) for account in african_accounts if build_url(account) != None]
f = open("results.json", "w")
f.write(json.dumps(list_of_good_accounts))
f.close()
f2 = open("urls.txt", "w")
for url in list_of_good_urls:
    f2.write(f'{url}\n')
f2.close()
