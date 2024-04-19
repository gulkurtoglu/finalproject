"""
This code runs without returning any results. I checked the web page's developer tools,
and it gives the warning that "Third-party cookie will be blocked. Learn more in the 
issues tab. When I checked it, I found that the following warnings: Reading cookie
in cross-site context will be blocked in future Chrome versions. Cookies with the
SameSite=None; Secure and not Partitioned attributes that operate in cross-site
contexts are third-party cookies. Affected resources: 10 cookes (with the cookie 
ids that are mostly Google analytics and doubleclick.net) 

# -*- coding: utf-8 -*-

Created on Thu Apr 18 15:40:08 2024

@author: Gül
"""

from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import os
from urllib.parse import urlparse
from time import sleep


# URL of the page containing links to speeches
url = "https://www.mhp.org.tr/htmldocs/genel_baskan/konusmalari/mhp/Devlet_Bahceli_Konusmalari.html"

# Define a convenience function to convert a relative or absolute
# URL to an absolute URL using urljoin
def absolute_url(s):
    return urljoin("https://www.mhp.org.tr/htmldocs/genel_baskan/konusmalari/mhp/Devlet_Bahceli_Konusmalari.html", s)


# Parse the HTML content and create the soup object
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
response = requests.get(url, headers=headers)
response = requests.get(url, timeout=60)  # Set timeout to 60 seconds
response.raise_for_status()


soup = BeautifulSoup(response.text, "html.parser")
absolute_urls = [absolute_url(tag.attrs['href']) for tag in soup.find_all('a')]


# Find all speech links
speech_links = []
speech_list = soup.find_all("li", class_="congress_programs")
for speech in speech_list:
    link = speech.find("a")["href"]
    speech_links.append(link)
    
# Iterate through each speech link and scrape the text
for speech_link in speech_links:
    # Construct the full URL of the speech page
    full_url = "https://www.mhp.org.tr" + speech_link
       
    try:      
    
        # Fetch the HTML content of the speech page
        speech_response = requests.get(full_url)
        speech_response.raise_for_status()
        
        # Parse the HTML of the speech page
        speech_soup = BeautifulSoup(speech_response.text, "html.parser")
        
        # Extract the speech text
        speech_text = speech_soup.find("div", class_="speech_text").get_text(strip=True)
        
        # Print the speech text
        print(speech_text)
    
        # Pace yourself to make sure the webpage does not block the scraper.
        sleep(1)  # Sleep for 1 second
        
    except requests.exceptions.Timeout:
            print(f"Timeout error occurred while accessing {full_url}. Skipping...")
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while accessing {full_url}: {e}")        
        
