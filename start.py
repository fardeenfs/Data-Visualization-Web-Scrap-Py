import csv
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# Change the URL variable value to a link of your choice. Example: "https://www.bbc.com"
URL = "https://www.bbc.com"

# (Optional) Change the WebName variable value to a name that represents the link. Example for the above: "BBC"
WebName = "BBC"

# (Important) Change the tag variable value to the HTML tag used to contain the date in the website you chose.
# For Example: BBC uses a 'time' tag. You can find this using the browser inspector.
tag = 'time'


def time_format(gdate):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    gdate = gdate.lower()
    gdate = gdate.replace(',', '')
    gdate = gdate.replace('-', ' ')
    gdate = gdate.split(' ')

    if gdate == "NONE":
        return gdate

    for i in gdate:
        if i in ["minutes", "hours", "minute", "hour", "today"]:
            gdate = datetime.date.today()
            return gdate
        elif i == "days":
            gix = gdate.index("days")
            gdate = datetime.date.today() - datetime.timedelta(int(gdate[gix - 1][-1]))
            return gdate
        elif i in ["day", "yesterday"]:
            gdate = datetime.date.today() - datetime.timedelta(1)
            return gdate

    for month in months:
        try:
            if month in gdate:
                month = gdate.index(month)
                try:
                    if month == 0:
                        year = gdate[month + 2]
                        day = gdate[month + 1]
                    if len(gdate[month - 1]) == 4:
                        year = gdate[month - 1]
                        day = gdate[month + 1]
                    else:
                        day = gdate[month - 1]
                        year = gdate[month + 1]
                except IndexError:
                    gdate = "NONE"
                    return gdate
                try:
                    print(day, month, year)
                    gdate = datetime.date(int(year), int(month), int(day))
                except ValueError or IndexError:
                    gdate = "NONE"
                    return gdate
        except TypeError:
            return gdate
    if type(gdate) != 'Date':
        gdate = "NONE"
        return gdate


def link_visit(link):
    src = requests.get(link)
    p_content = BeautifulSoup(src.content, 'html.parser')
    a_time = p_content.find(tag)
    print("Processing Link :", link)
    if a_time is not None:
        time = time_format(a_time.text)
        print(link)
        links.writerow([link, time])
        print(time)


def link_extract(content):
    for aLink in content.find_all('a'):
        link = aLink.get('href')
        if "https://" in link and link is not None:
            link_visit(link)
        elif link[0] == '/' and link not in [None, '']:
            link = URL + link
            link_visit(link)


def create_data_file():
    file = open(WebName + " links.csv", 'r')
    file_read = csv.reader(file)
    datafile = open(WebName + " dataplot.csv", 'w', newline="")
    datafile_write = csv.writer(datafile)
    datafile_write.writerow(["Date", "No.Of Pages"])
    data = {}
    for i in file_read:
        if i[1] not in data.keys() and i[1] not in ["NONE", 'Date']:
            dates = i[1]
            data[dates] = 0
        elif i[1] not in ["NONE", 'Date']:
            dates = i[1]
            data[dates] = data[dates] + 1
    for i in reversed(sorted(data.keys())):
        datafile_write.writerow([i, data[i]])
    print(data)
    datafile.close()


def data_plot():
    datafile = pd.read_csv(WebName + " dataplot.csv")
    x = datafile['Date']
    y = datafile['No.Of Pages']
    plt.bar(x, y)
    plt.title("Dot Graph Showing No. Of Pages Published " + WebName + " By Date")
    plt.xlabel('Date', fontsize=15)
    plt.ylabel('No. Of Pages', fontsize=15)
    plt.tick_params(axis='x', labelsize=8)
    plt.show()


def driver_start():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    driver.minimize_window()

    content = BeautifulSoup(driver.page_source, 'html.parser')
    link_extract(content)
    driver.close()


linklist = open(WebName + " links.csv", "w", newline="")
links = csv.writer(linklist)
links.writerow(["URL", "Date"])
driver_start()
linklist.close()

create_data_file()
data_plot()
