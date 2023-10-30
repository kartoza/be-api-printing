from selenium import webdriver  
from pathlib import Path
import os
import time  
from selenium.webdriver.common.keys import Keys  

class APIPrint():
    def __init__(self, url_list, download_path, progress_bar):
        self.url_list = url_list
        self.download_path = download_path
        self.progress_bar = progress_bar

    def apiCallBack(self):

        driver = webdriver.Chrome()  
        #driver=webdriver.firefox()  
        #driver=webdriver.ie()  
        #maximize the window size  
        driver.maximize_window()  

        for url in self.url_list:
            
            #navigate to the url  
            
            try:
                driver.get(url)
                wait = True
                while(wait==True):
                    for fname in os.listdir(self.download_path):
                        if ('Unconfirmed') in fname:
                            print('downloading files ...')
                            time.sleep(2)
                        else:
                            wait=False
                print('finished downloading all files ...')
                self.progress_bar.value += 90
            except:
                pass

        driver.close()  
