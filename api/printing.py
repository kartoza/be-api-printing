from selenium import webdriver  
from pathlib import Path
import os
import time  
from selenium.webdriver.common.keys import Keys  
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class APIPrint():
    def __init__(self, url_list, download_path):
        self.url_list = url_list
        self.download_path = download_path

    def apiCallBack(self):

        # driver = webdriver.Chrome()  
        # driver=webdriver.firefox()  
        #driver=webdriver.ie()  
        #maximize the window size  
        WINDOW_SIZE = "1920,1080"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        
        prefs = {'download.default_directory' : self.download_path}
        chrome_options.add_experimental_option('prefs', prefs)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        # driver = webdriver.Chrome('/app/chromedriver')
        driver.maximize_window()  
        time.sleep(10)
        delay = 5
        filenames = []

        if not os.path.exists(self.download_path):
            mode = 0o777
            os.mkdir(self.download_path, mode)

        for url in self.url_list:
            
            #navigate to the url  
            
            try:
                driver.get(url)
                wait = True
                og_files_len = len([name for name in os.listdir(self.download_path)])
                while(wait==True):
                    # element = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'feature-content')))
                    element = driver.find_element(By.ID, "feature-content")
                    if element:
                        time.sleep(2)
                        for fname in os.listdir(self.download_path):
                            if ('Unconfirmed') in fname:
                                print('downloading files ...')
                                time.sleep(5)
                            else:
                                current_files_len = len([name for name in os.listdir(self.download_path)])
                                if current_files_len > og_files_len:
                                    for name in os.listdir(self.download_path):
                                        filenames.append(name)
                                    wait=False
                                else:
                                    time.sleep(2)
                    else:
                        time.sleep(2)
                print('finished downloading all files ...')
                # self.progress_bar.value += 90
            except:
                pass
        
        driver.close()  
        return filenames
