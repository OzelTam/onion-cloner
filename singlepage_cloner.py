from bs4 import BeautifulSoup
import requests
import os
from utils import extract_internal_links, is_valid_link


port = input("Socks listener port: ") # Port that Tor Socks listener working on
directory = input("Please specify dirlectory: ") # Directory to dump website contents


proxies = {
        'http': 'socks5h://127.0.0.1:'+ port,
        'https': 'socks5h://127.0.0.1:'+port
}


def create_file(file,code):
    try:
        if not os.path.exists(directory):
            os.mkdir(directory) #Creates folder if not exists
        file = directory + "\\" + file #points file to dir.
        f = open(file, "w") #open file write mode
        f.write(code) 
        f.close()
    except:
        return False
  

def download_page(link):
    return requests.get(link,proxies=proxies).text #Downloads specified url content

#GETS CSS FILES AND POINTS IMPORTS IN HTML TO DOWNLOADED
def get_css_files(html,link):
    soup = BeautifulSoup(html, 'html.parser')
    stylesheets = soup.find_all('link') # gets <link> tags
    for css in stylesheets:
        if not css.get('type') == 'text/css': #filters nin css type files
            continue
        css_link = css.get('href') # gets source of css
        if css_link[0] == "/":  # converts to full if path is relative
            css_link = link + css_link[1:]
        create_file(get_path_name(css_link,"css"), download_page(css_link)) #downloads creates css file
        css['href'] = get_path_name(css_link, "css") # points css href to local file
    return soup.prettify() # retuns new version of html

#GETS JS FILES AND POINTS IMPORTS IN HTML TO DOWNLOADED
def get_js_files(html,link):
    soup = BeautifulSoup(html, 'html.parser')
    scripts = soup.find_all('script') # find <script tags>
    for js in scripts:
        if js.get('src') == None: # if src is empty 
            continue
        js_link = js.get('src')
        if js_link[0] == "/":       # converts to full if path is relative
            js_link = link + js_link[1:]

        create_file(get_path_name(js_link,"js"), download_page(js_link)) #downloads creates js file
        js['src'] =  get_path_name(js_link, "js")# points js src to local file
    return soup.prettify() # retuns new version of html

#GETS IMAGES AND POINTS IMPORTS IN HTML TO DOWNLOADED
def get_images(html,link):
    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img') # find <img> tags
    for img in imgs:
        img_link = img.get('src')
        if img_link[0] == "/":       # converts to full if path is relative
            img_link = link + img_link[1:]
        download_image(get_path_name(img_link),img_link)
        img['src'] = get_path_name(img_link)
    return soup.prettify()


def download_image(file, link):
    r = requests.get(link, stream=True, proxies=proxies)
    if r.status_code == 200:
        os.makedirs(os.path.dirname(directory + "\\" + file), exist_ok=True)
        with open(directory + "\\" + file, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def get_path_name(link, extension = "*"):
    p_name = link.split("/")[-1].replace("?","").replace("=","") # trims illegal chars

    if extension == "*":
        return p_name

    if len(p_name) < len(extension): #checks extension if not same adds specified ext.
        p_name += "." + extension #returns filename

    last =  p_name[(len(p_name) - len(extension)): ] #checks extension if not same adds specified ext.
    if not last == extension:
        p_name += "." + extension

    return p_name #returns filename


def clone_page(link):
    html = download_page(link) # get Index html src
    html = get_css_files(html,link) # get update html (downloads and points to local css files)
    html = get_js_files(html,link) # get update html (downloads and points to local js files)
    html = get_images(html, link)
    create_file("index.html",html) #creates index.html with updated html


clone_link = input("Enter Link to clone: ")
clone_page(clone_link)
