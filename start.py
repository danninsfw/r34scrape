import requests as req
import os
import shutil
from bs4 import BeautifulSoup

BASE_URL = "https://rule34.paheal.net"
DOWNLOADS_DIR = os.path.join(os.getcwd(), ".downloads")

def is_imglink(a_elem):
    return a_elem.string == 'File Only'

def download_img(imglink):
    print(imglink)
    global DOWNLOADS_DIR
    r = req.get(imglink, stream=True)
    filename = imglink.split("/")[-1]
    if r.status_code == 200:
        while os.path.exists(os.path.join(DOWNLOADS_DIR, filename)):
            filename = "+" + filename
        with open(os.path.join(DOWNLOADS_DIR, filename), "wb") as file:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, file)

def download_page(page):
    img_list = page.find(id="image-list")
    linklist = [link for link in img_list.find_all('a') if is_imglink(link)]
    listlen = str(len(linklist))
    print("found " + listlen + " links in page")
    for i, link in enumerate(linklist):
            print("downloading img " + str(i+1) + " of " + listlen)
            download_img(link["href"])
            print("finished")

def get_pagelinks(root):
    global BASE_URL
    page_list = root.find(id="paginator")
    urls = []
    for link in page_list.find_all('a'):
        urls.append(BASE_URL + link['href'])
    print(urls)
    return set(urls)

if not os.path.exists(DOWNLOADS_DIR):
    os.mkdir(DOWNLOADS_DIR)


start = req.get("https://rule34.paheal.net/post/list/Valkyrien/1")
root = BeautifulSoup(start.content, 'html.parser')

print("starting scrape...")
pagelinks = get_pagelinks(root)
print("found " + str(len(pagelinks)) + " pages of content")
for i, page_url in enumerate(pagelinks):
    if i+1 >= 8: 
        print("downloading page " + str(i+1) + " of " + str(len(pagelinks)))
        page = BeautifulSoup(req.get(page_url).content, 'html.parser')
        download_page(page)
        print("finished page " + str(i+1) + " of " + str(len(pagelinks)))
