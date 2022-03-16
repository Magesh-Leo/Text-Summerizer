from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import warnings
from google.cloud import storage
import uuid

from app.taskGenerator import create_task

warnings.filterwarnings("ignore",category=DeprecationWarning)
#reference pages
#videourl = "https://hackernoon.com/i-tried-hacking-a-bluetooth-speaker-heres-what-happened-next"
#audiowithtext = "https://hackernoon.com/the-fastest-way-to-invoke-a-httprest-url-from-an-aws-lambda"
#onlytext = "https://hackernoon.com/an-intro-to-ens-ethereum-name-services-and-why-you-should-get-one"
def sentUrl(uid,url):
    try:
        web = DesiredCapabilities.CHROME
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Remote(
            command_executor= 'https://standalone-chrome-zlzujd3glq-em.a.run.app/wd/hub', #f'{os.environ.get("SELENIUM_URL")}/wd/hub' 
            desired_capabilities = web,
            options=options)
        
        if "https://hackernoon.com" in url:
            if len(url.split('.com/'))==2:
                driver.get(url)
                content = driver.find_elements_by_tag_name('p')   #scrapping content
                content2 = driver.find_elements_by_class_name('paragraph')
                try:
                    adiotext = driver.find_element_by_id('wave-loader')
                    if adiotext.is_displayed(): # wave-loader for audio content page
                        try:
                            text=''
                            for i in range (1,int(len(content))+1):
                                try:
                                    text += driver.find_element_by_xpath(f'//*[@id="__next"]/div/main/div/div[5]/div/div/div/p[{i}]').text  #//*[@id="__next"]/div/main/div/div[5]/div/div/div/p
                                    #text.append(t)                        
                                except:
                                    pass
                            for i in range (1,int(len(content2))+1):
                                try:
                                    text += driver.find_element_by_xpath(f"//*[contains(@class,'paragraph')][{i}]").text  #//*[@id="__next"]/div/main/div/div[5]/div/div/div/p
                                    #text.append(t)
                                except:
                                    pass
                            text.split('\n')
                            text = [line for line in text.split('\n') if line.strip() != '']
                            text_summerized = " ".join(text)
                            
                            fName = str(uuid.uuid4())    
                            client = storage.Client()
                            bucket = client.get_bucket('mydemo-bucket-ts')
                            new_blob = bucket.blob(f'remote/hackernoon/{fName}.txt')
                            new_blob.upload_from_string(text_summerized)
                            print('Upload successfully')
                            #### create task here ######
                            create_task(uid=uid,url=url,payload=text_summerized)
                            ############################
                            print('summerized')
                            return text_summerized
                            
                        except Exception:
                            print('p tag loop not working..')
                            return "Data not Fetching"
                except Exception:
                    try:
                        text=''
                        for i in range (1,int(len(content))+1):
                            try:
                                text += driver.find_element_by_xpath(f'//*[@id="__next"]/div/main/div/div[4]/div/div/div/p[{i}]').text  #//*[@id="__next"]/div/main/div/div[5]/div/div/div/p
                                #text.append(t)                        
                            except:
                                pass
                        for i in range (1,int(len(content2))+1):
                            try:
                                text += driver.find_element_by_xpath(f"//*[contains(@class,'paragraph')][{i}]").text
                            except:
                                pass
                        text.split('\n')
                        text = [line for line in text.split('\n') if line.strip() != '']
                        text_summerized = " ".join(text)
                        
                        fName = str(uuid.uuid4())    
                        client = storage.Client()
                        bucket = client.get_bucket('mydemo-bucket-ts')
                        new_blob = bucket.blob(f'remote/hackernoon/{fName}.txt')
                        new_blob.upload_from_string(text_summerized)
                        print('Upload successfully')
                        #### create task here ######
                        create_task(uid=uid,url=url,payload=text_summerized)
                        ############################
                        print('summerized')
                        return text_summerized
                    except Exception:
                        print('p tag loop not working..(Text only)')
                        return "Data not Fetching"
                #video content page there is no more text content
                try:
                    vdeoonly = driver.find_element_by_class_name('html5-video-container')
                    if vdeoonly.is_displayed():
                        print("This is Video file there is no more text content to read...")
                except Exception:   
                    pass

            driver.quit() 
    except Exception as e:
        print(e) 

