import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_google_play_data():
    MAIN_LINK = "https://play.google.com/store/apps"
    # Get the content of the main page and create a BeautifulSoup object from it
    play_store_page = requests.get(MAIN_LINK)
    soup = BeautifulSoup(play_store_page.content, "html.parser")
#     print(soup.prettify())

    # Find the "See More" button to see more applications from the same category.
    # Use find to get the first found element.
    # Use find_all to get all the elements on the page.
    # For testing purposes, we'll stick to the first element found on the page for now.
    see_more_apps = soup.find_all(class_ = "W9yFB")

    # From there, we will need the link (href) which leads to the "See more apps" from each category

    APPS, PACKAGE_NAMES = [], []

    for elem in see_more_apps:
        see_more_apps_link = [a["href"] for a in elem.find_all("a", href = True)]

        # With the link scraped, we will combine it with "https://play.google.com"
        # to get to the "See more # apps" pages.
        see_more_apps_link = "https://play.google.com" + see_more_apps_link[0]
#         print("\nComplete 'See More' Button Link: ", see_more_apps_link)

        # With the obtained link, we will request the content of each
        # page and create a BS4 object from it.
        see_more_apps_page = BeautifulSoup(requests.get(see_more_apps_link).content, "html.parser")

        # Now we got to the "See More" applications page. 
        # From here, we will need to scrape through each page and obtain the following informations:
        # - Application name - we will store it in global variable APPS
        # - The 'href' link of every application, which contains the package name 
        #      - we will store it in global variable PACKAGE_NAMES

        # All the apps displayed in the page are stored under classes named "ImZGtf mpg5gc"
        for item in see_more_apps_page.find_all(class_ = "ImZGtf mpg5gc"):
            title = item.find(class_ = "WsMG1c nnK0zc").get_text()
            APPS.append(title)
            # We'll get the application link by splitting the elements found
            app_link = str(item.find(class_ = "wXUyZd").find(href = True))
            app_link = app_link.split("id=")[1].split('"')[0]
            PACKAGE_NAMES.append(app_link)
    #         print("{}: {}".format(title, app_link))

    GOOGLE_PLAY_DATA = pd.DataFrame(
        {
            "Application": APPS,
            "App ID": PACKAGE_NAMES
        }
    )
    return GOOGLE_PLAY_DATA