from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape():

    # URL of pages to be scraped
    mars_news_url = 'https://redplanetscience.com'
    space_img_url = "https://spaceimages-mars.com"
    mars_facts_url = "https://galaxyfacts-mars.com"
    hemisph_url = "https://marshemispheres.com"

    # Setup Splinter Browser
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Go to the news url
    browser.visit(mars_news_url)

# Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

# Find the news section
    latest_news = soup.find('div', id='news')

# Get the latest news title
    news_text = latest_news.find('div', class_='content_title').text
    news_text

    # Get the latest news paragraph
    news_details = latest_news.find('div', class_='article_teaser_body').text
    news_details

    #Featured Space Image site 
    browser.visit(space_img_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    local_image_url = soup.find('img', class_="headerimage fade-in")['src']
    featured_image_url = space_img_url+'/'+local_image_url
    featured_image_url

    table = pd.read_html(mars_facts_url)
    newdf = table[0]
    newdf.columns=['Mars - Earth Comparison','Mars', 'Earth']
    newdf.set_index('Mars - Earth Comparison', inplace=True)
    df = newdf.iloc[1: , :]
    html_newdf = df.to_html()
    html_newdf = html_newdf.replace('\n', ' ')
    html_newdf

    # Convert the data to a HTML table string
    html_table = df.to_html()
    html_table.replace('\n', '')
    html_table

    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    xpath = '//*[@id="product-section"]/div[2]/div[1]/div/a/h3'
    xpath2 = '//*[@id="product-section"]/div[2]/div[2]/div/a/h3'
    xpath3 = '//*[@id="product-section"]/div[2]/div[3]/div/a/h3'
    xpath4 = '//*[@id="product-section"]/div[2]/div[4]/div/a/h3'
    info_list = []
    xpath_list = [xpath, xpath2, xpath3, xpath4]
    
    for x in xpath_list:
            results = browser.find_by_xpath(x)
            click = results[0]
            click.click()

            html = browser.html
            soup = BeautifulSoup(html, "html.parser")

            hemi_title = soup.find('h2', class_='title').text
            full_image = soup.find('img', class_='wide-image')['src']
            full_image_url = url + full_image

            data = {
                "title": hemi_title,
                "img_url": full_image_url
            }
            info_list.append(data)
            browser.back()
    browser.quit()

    table_body = html_table.replace('<table border="1" class="dataframe">\n  ',"").replace('</table>','')

    # Save result of all the scraping to the dictionary
    final_dict = {'news_title': news_text, 'news_par': news_details, "featured_img": featured_image_url,
            "table": table_body, "hemispheres": info_list}

    return final_dict