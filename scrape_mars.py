#################################################
# Jupyter Notebook Conversion to Python Script
#################################################

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    # Run init_browser/driver.
    browser = init_browser()

    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)



    # Parse HTML with Beautiful Soup
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")
    slide_element = news_soup.select_one("ul.item_list li.slide")

    # Retrieve the most recent article's title and paragraph.
    # Store in news variables.
    news_title = slide_element.find("div", class_="content_title").get_text()
    
    # Scrape the Latest Paragraph Text
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    
    # Exit Browser
    browser.quit()


    ### JPL Mars Space Images - Featured Image
    # Run init_browser/driver
    browser = init_browser()

    ## Visit the url for JPL Featured Space Image
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    ## Select "FULL IMAGE"
    browser.click_link_by_partial_text("FULL IMAGE")

    ## Find "more info" for first image, set to variable, and command click
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    ## HTML Object
    html = browser.html

    ## Parse HTML with Beautiful Soup
    image_soup = BeautifulSoup(html, "html.parser")

    ## Scrape image URL
    image_url = image_soup.find("figure", class_="lede").a["href"]

    ## Concatentate https://www.jpl.nasa.gov with image_url
    featured_image_url = f'https://www.jpl.nasa.gov{image_url}'

    ## Exit Browser
    browser.quit()


    ### Mars Weather - twitter issue

    ### Mars Facts

    # URL for Mars Facts
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df.columns=["Description", "Value"]
    df.reset_index()
    mars_facts = df.to_html(classes="table table-striped")


    
    ### Mars Hemispheres

    # Run init_browser/driver
    browser = init_browser()

    # Visit the url for USGS Astrogeology

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, "html.parser")

    # Store main URL in a variable so that 'href' can be appended to it after each iteration.
    main_astrogeo_url = "https://astrogeology.usgs.gov"

    # Locate all 4 and store in variable
    hems_url = soup.find_all("div", class_="item")

    # Create empty list for each Hemisphere URL.
    hemis_url = []

    for hem in hems_url:
        hem_url = hem.find('a')['href']
        hemis_url.append(hem_url)

    browser.quit()

    # Create list of dictionaries called hemisphere_image_urls
    # Iterate through all URLs saved in hemis_url
    # Concatenate each with the main_astrogeo_url
    # Confirm the concat worked properly: confirmed
    # Visit each URL

    hemisphere_image_urls = []
    for hemi in hemis_url:
        hem_astrogeo_url = main_astrogeo_url + hemi
        print(hem_astrogeo_url)
        
        # Run init_browser/driver
        browser = init_browser()
        browser.visit(hem_astrogeo_url)
        
        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        hemi_soup = BeautifulSoup(html, "html.parser")

        # Locate each title and save to raw_title, to be cleaned
        raw_title = hemi_soup.find("h2", class_="title").text
        
        # Remove ' Enhanced' tag text from each "title" via split on ' Enhanced'
        title = raw_title.split(' Enhanced')[0]
        
        # Locate each 'full.jpg' for all 4 Hemisphere URLs
        img_url = hemi_soup.find("li").a['href']
        
        # Append both title and img_url to 'hemisphere_image_url'
        hemisphere_image_urls.append({'title': title, 'img_url': img_url})
        
        browser.quit()

    print(hemisphere_image_urls)


    
    #Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemispheres": hemisphere_image_urls,
    }
    browser.quit()

    return mars_data 
 