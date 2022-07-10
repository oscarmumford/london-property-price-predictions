import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import random




#CONFIG

USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
"Chrome OS/Chrome browser: Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0"]

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" 

CHROMEDRIVER_PATH = '/Users/oscarmumford/.wdm/drivers/chromedriver/mac64/101.0.4951.41/chromedriver' #ChromeDriverManager().install() 

WINDOW_SIZE = "1920,1080"




class ZooplaPageDriver:
    
    #lat_long_data = {"lat":"", "long":""}
    #listing_history = {}
    
    def __init__(self):
        
        
        #self.lat_long_data['lat'] = "NA"
        #self.lat_long_data['long'] = "NA"
        self.lat_long_data = {'lat': "NA",
                              'long':"NA"}
        self.listing_history = {}
        self.random_user_agent = random.choice(USER_AGENTS)
        self.chrome_options = selenium.webdriver.ChromeOptions()
        #self.chrome_options.add_argument("--headless")
        #self.chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.chrome_options.add_argument(f"user-agent={self.random_user_agent}")
        self.chrome_options.binary_location = CHROME_PATH
        self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                                       options=self.chrome_options)
    
    
    def accept_cookies(self):
        #wait
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "gdpr-consent-notice")))
        
        #Switch iFrame
        try:
            frame_1 = self.driver.find_element_by_id("gdpr-consent-notice")
            print('found iframe')
            self.driver.switch_to.frame(frame_1)
            print('switched to frame')
        except:
            print('ERROR: cookies iFrame not switched to')



        #Accepting Cookies on Zoopla
        #time.sleep(2)
        #pressing the cookies button
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, 'save')))
        try: 
            self.driver.find_element_by_id('save')
            print('found button')
            #button = self.driver.find_element_by_xpath('//button[@id="save"]')
            #print('found button')
            #driver.execute_script("arguments[0].click();", button)
            self.driver.execute_script("document.getElementById('save').click()")
            print('button pressed')
        except:
            print("Cookies button not pressed")

            
            
            
        #return to the main parent frame
   

        time.sleep(1)
        try:
            self.driver.switch_to.default_content()
            print('switched to default')
        except:
            print('ERROR: Unable to switch back to default HTML')


    
    def get_long_lat(self):
       
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, "img"))) 
        try:
            print("Found the img")
            search_input = self.driver.find_elements_by_tag_name("img")
            google_map_link = search_input[1].get_attribute('src')
            long_lat_from_url_pattern = r"(?:center=)([\d.-]*),([\d.-]*)"
            long_lat_scrape = re.search(long_lat_from_url_pattern,
                                 google_map_link).groups()
            print("Searching for long lat pattern")
            self.lat_long_data["lat"], self.lat_long_data["long"]  = long_lat_scrape[0], long_lat_scrape[1]
            print("Appending to lat_long_data")
        except:
            self.driver.quit()
            print("ERROR: Failed to get long lat data")
            return False
    
    def get_listing_history(self):
        
        #wait until listing button is available
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="listinghistory-button"]')))

        #press the listing history button
        try: # proceed if element is found within 3 seconds otherwise will raise TimeoutException 
            button = self.driver.find_element_by_xpath('//button[@data-testid="listinghistory-button"]')
            print('found button')
            self.driver.execute_script("arguments[0].click();", button)
            print('button pressed')
            time.sleep(1)
        except:
            print("ERROR: Listing History button not pressed")

        #grabbing data from listing history table
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//table[@data-testid="listing-history"]')))
        try:
            listing_table = self.driver.find_element_by_xpath('//table[@data-testid="listing-history"]')
            print('found the listing table')
            listing_cells = listing_table.find_element_by_xpath('//tbody').find_elements_by_xpath('//td')
            #listing_rows = listing_table.find_element_by_xpath('//tbody').find_elements_by_xpath('//tr')
            print('got the cells')
            column_names = ["first_listed_date", "first_listed_text", "first_listed_price", "last_sold_date", "last_sold_text", "last_sold_price"]
            scraped_listing_history_table = {column_name:cell.text for column_name, cell in zip(column_names, listing_cells)}
            print('scraped table')
            self.listing_history = scraped_listing_history_table
        except:
            print("ERROR: Listing Table not scraped")
    
    
        
    
    def scrape(self, url):
        # try:
        #     self.driver
        # except:
        #     pass
        
        
        
        try:
            #chrome_options.add_argument(f"user-agent={random_user_agent}")
            self.driver.implicitly_wait(10)
            self.driver.get(url)
        except Exception as e:
            print('Couldnt get to URL')
            self.driver.quit()
        
        #function calls
        self.accept_cookies()
        time.sleep(5)
        print('cookies function ended. about to start getting long lat...')
        self.get_long_lat()
        self.get_listing_history()
        self.driver.quit()
        
        #return (self.lat_long_data, self.listing_history)
        return dict(self.lat_long_data, **self.listing_history)



    def quit_scrape(self):
        self.driver.quit()
    
    