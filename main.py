from bs4 import BeautifulSoup
import requests
import time
import random

base_url = "https://wesmckinney.com/book/"

def main():
    sub_urls = [
        "https://wesmckinney.com/book/"
    ]

    repeated = False

    url = base_url

    while not repeated:
        next_url = find_next_url(url)

        if next_url in sub_urls:
            repeated = True 
            break

        sub_urls.append(next_url)
        url = next_url
        delay()

    print(sub_urls)

def find_next_url(url):
    page = requests.get(url)
    if page.status_code != 200:
        return url

    soup = BeautifulSoup(page.text, "html.parser")

    try:
        resp = soup.find('div', class_ = "nav-page nav-page-next").find("a", href=True)
        link = base_url + resp["href"][2:]
    
    except Exception:
        link = url

    return link

def delay():
    lenght = random.uniform(1,5)
    print(f"Waiting {lenght} seconds between requests")
    time.sleep(lenght)




if __name__ == "__main__":
    main()