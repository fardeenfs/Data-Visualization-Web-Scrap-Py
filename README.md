# Data Visualization Web Scrap Py
 A simple program that scraps dates from the pages of a website and plots a Page-Date graph
 
<b>What The Program Does</b><br>
 On execution, the program reads all the links in the news website specified to the URL variable. The date of publication of the linked articles are captured. A bar graph which shows the number of pages published on a particular date is then plotted using the scraped data.

<b>How To Use The Program</b><br>
1. Change the <b>URL</b> variable value to a link of your choice. Example: "https://www.bbc.com"
2. (Optional) Change the <b>WebName</b> variable value to a name that represents the link. Example for the above: "BBC"
3. (Important) Change the <b>tag</b> variable value to the HTML tag used to contain the date in the website you chose. Example: BBC uses a 'time' tag. You can find this using the browser inspector.

<b>Notes</b>
1. The program only reads the links on the page specified in the URL. Links mentioned elsewhere in the website will not be scraped. This can be overcome by using a nested loop to call the link_extract() function. 
2. For accurate results, use a website's RSS Feed.

<b>The program uses the following modules:</b><br>
- csv
- time
- datetime
- matplotlib
- pandas
- requests
- BeautifulSoup 4
- selenium
- ChromeDriverManager

PS. This a project made for fun. Any further contributions to the project are welcome.
