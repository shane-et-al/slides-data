"""
Crawls the NUFORC database and scrape every month's data

Usage:
    ./scrape_crawl_demo.py

Author:
    Shane Lin - 2024-08-22
"""

import csv
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urljoin

# URL to scrape
URL = "https://nuforc.org/ndx/?id=event"
# Number of months to scrape
LIMIT = 12


def getHTML(url):
    """Return the HTML at a particular URL"""
    fp = urllib.request.urlopen(url, timeout = 10)
    return fp.read().decode("utf8")


def getReports(soup):
    """
    Find the data table in a soup object and return the gooey
    goodness as a list of lists
    """
    reports = []
    # For each data row in the table...
    for row in soup.select('table#table_1 > tbody > tr'):
        report = []
        # For each column in that row...
        for col in row.select('td'):
            link = col.find("a")
            # Unpack the link if there's a URL
            if link:
                report.append(urljoin(URL, link["href"]))
            # Otherwise, just grab the text
            else:
                report.append(col.text)
        reports.append(report)
    return reports


def getHeaders(soup):
    """
    Find the data table header in a soup object and return
    the headers as a list
    """
    ths = soup.select('table#table_1 th')
    return [th.text for th in ths]


# Grab HTML and make a Beautiful Soup
soup = BeautifulSoup(getHTML(URL), 'html.parser')

reports = []
for link in soup.select("table td a")[:LIMIT]:
    url = urljoin(URL, link["href"])
    print("Grabbing: ",url)
    html = getHTML(url)
    month_soup = BeautifulSoup(html, 'html.parser')
    headers = getHeaders(month_soup)
    reports += getReports(month_soup)

# Write the data to a CSV file
with open('ufos.csv', 'w', newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(headers)
    for report in reports:
        writer.writerow(report)
