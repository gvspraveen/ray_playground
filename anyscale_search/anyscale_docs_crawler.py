from bs4 import BeautifulSoup
import requests

# website to be scrape
root_site="https://docs.anyscale.com"

# reference code: https://www.geeksforgeeks.org/python-program-to-recursively-scrape-all-the-urls-of-the-website/#
urls=set([])
# function created
def _scrape_urls(site, depth=0):
    print ("Scraping: ", site)
    # getting the request from url

    r = requests.get(site)     
    # converting the text
    s = BeautifulSoup(r.text,"html.parser") 
    # print(s)
    for i in s.find_all("a"):          
        href = i.attrs['href']
        if "/reference" in href:
            continue       
        if href.startswith("/"):
            site = root_site + href               
            if site not in urls:
                urls.add(site) 
                # calling it self
                _scrape_urls(site, depth+1)

 
def scrape_urls():
    urls.clear()
    _scrape_urls(root_site)
    print("Total URLs fetch: ", len(urls))
    return urls


