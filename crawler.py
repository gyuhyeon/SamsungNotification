from time import sleep
from random import randint
from selenium import webdriver
from pyvirtualdisplay import Display
from twilio.rest import Client
import Config

class SeleniumCrawler():
    def __init__(self):
        self.start_driver() # Design changes : call start driver on init, and call close_driver on script termination(except & finally)

    # Open headless chromedriver
    def start_driver(self):
        print('starting driver...')
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.driver = webdriver.Chrome("/var/chromedriver/chromedriver")
        sleep(4)

    # Close chromedriver
    def close_driver(self):
        print('closing driver...')
        self.display.stop()
        self.driver.quit()
        sleep(1)
        print('closed!')

    # Tell the browser to get a page. The method is safe, no exceptions will be thrown.
    def get_page(self, url):
        try:
            print('getting page %s'%(url))
            self.driver.get(url)
            sleep(5)
        except Exception:
            print("page wanted to give alert for some reason, probably")
            try:
                self.driver.switch_to.alert.accept()
                sleep(3)
            except Exception:
                print("Error when trying to accept alert")
        
    def samsunglogin(self):
        print("getting past the samsung login page")
        self.get_page("http://www.samsungcareers.com/rec/apply/FreResumeServlet")
        try: # prevents script failure from element search failure
            idinput = self.driver.find_element_by_id('email')
            idinput.clear()
            idinput.send_keys(Config.samsungid)
            pwinput = self.driver.find_element_by_id('password')
            pwinput.clear()
            pwinput.send_keys(Config.samsungpw)
            self.driver.find_element_by_id('budiv_mySheet_comLogin').find_element_by_link_text('로그인').click()
            sleep(5)
        except Exception:
            print("Error when logging into samsung careers page")
            pass
            
    def check_announcement(self):
        print("Checking careers announcement")
        self.get_page("http://www.samsungcareers.com/rec/apply/FreResumeServlet")
        
        try: # try to click my application form
            self.driver.find_element_by_partial_link_text('2017년').click()
            sleep(3)
        except Exception as e:
            print("Error when clicking 2017:",end="")
            print(e)
        try: # try to click "결과보기" button
            self.driver.find_element_by_partial_link_text('결과').click()
            sleep(3)
        except Exception as e: # Maybe there won't be any "결과보기" button at all, and just throw error screen
            print("Error when clicking show result:",end="")
            print(e)
            try:
                if len(self.driver.find_elements_by_xpath('//*[contains(text(), "확인기간이")]'))>=1:
                    return "ready"
            except Exception as e:
                print("Error when seeing if the page is being ready(it's not)")
                print(e)
        try: # try to see if the page has "축하" in it
            if len(self.driver.find_elements_by_xpath('//*[contains(text(), "축하")]'))>=1:
                return "announced"
        except Exception: # this won't be called, because find_elements throw empty list instead of exception unlike find_element.
            print("Error when seeing if the result was being prepared")
            pass
        try: # try to see if the page is being ready
            if len(self.driver.find_elements_by_xpath('//*[contains(text(), "확인기간이")]'))>=1:
                return "ready"
        except Exception: # this won't be called, because find_elements throw empty list instead of exception unlike find_element.
            print("Error when seeing if the result was announced")
        try: # dev purposes. See if we have correct access to page.
            print("Current page text: %s"%(self.driver.find_element_by_xpath('//div[@class="inner"]').get_attribute("innerHTML")))
            print("Current page full source: %s"%(self.driver.page_source))
        except Exception:
            print("Error when trying to print page source")
        return "" # return nothing when uninteresting

    def samsungcheck(self):
        # self.start_driver()
        self.samsunglogin()
        res = self.check_announcement()
        # self.close_driver()
        return res
    
    def codegrlogin(self):
        self.get_page("https://www.codeground.org/sst/common/userTestHistory")
        
        try:
            idinput = self.driver.find_element_by_id("username")
            idinput.clear()
            idinput.send_keys(Config.codegrid)
            pwinput = self.driver.find_element_by_id("password")
            pwinput.clear()
            pwinput.send_keys(Config.codegrpw)
            self.driver.find_element_by_id("loginBtn").click()
            sleep(3)
        except Exception:
            print("Error occurred when trying to input login credentials, or already logged in.")
        
        self.get_page("https://www.codeground.org/sst/common/userTestHistory") # Do it again to prevent any "change password" screen redirects

    def codegrcheck(self):
        self.codegrlogin()
        try:
            # print("dev test : error when 0 elements are found? - "+str(len(self.driver.find_elements_by_xpath('//*[contains(text(), "asdf")]'))))
            # confirmed : find_elements_by_xpath does not throw error when none is found. it returns an empty list.
            result = len(self.driver.find_elements_by_xpath('//*[contains(text(), "진행중")]'))
            insurance = len(self.driver.find_elements_by_xpath('//*[contains(text(), "결과")]')) # prevents from notifying when page crawling has failed
            print(insurance) # dev
            if result > 0 or insurance == 0:
                return ""
            else:
                return "codegrupdated"
        except Exception as e:
            print("Error occured???")
            print(e)
            return "" # Some error occurred... But it's unlikely to come here.

    def notify(self, phonenumber, msg):
        client = Client(Config.twsid, Config.twtoken)
        try:
            message = client.messages.create(to=phonenumber, from_="+12568184331", body=msg)
        except:
            print("Error when sending sms notification")
        
if __name__ == "__main__":
    try:
        # Run spider
        SC = SeleniumCrawler()

        # Samsung from here
        res = SC.samsungcheck()
        # res = "ready" test to see if notification will go through
        if res=="ready" or res=="announced":
            print("Samsung's onto something!")
            readynotified = False
            announcenotified = False
            # MANUAL CONFIG
            with open('/home/ubuntu/PythonCrawl/bool.txt', 'r') as f: # TODO : make DB connection instead of text log
                for line in f:
                    if "ready" in line:
                        readynotified=True
                        print('already notified about change!')
                    if "announced" in line:
                        announcenotified=True
                        print("already notified about announcement!")
            if (not readynotified and res=="ready") or (not announcenotified and res == "announced"):
                # MANUAL CONFIG
                with open('/home/ubuntu/PythonCrawl/bool.txt', 'a') as f:
                    f.write(res+'\n')
                SC.notify("+821072481535", "삼전:"+res)
        
        res = SC.codegrcheck()
        # res = "codegrupdated" test to see if notification will go through
        if res=="codegrupdated":
            print("Codeground has been updated!")
            notified = False
            # MANUAL CONFIG
            with open('/home/ubuntu/PythonCrawl/bool.txt', 'r') as f:
                for line in f:
                    if "notified" in line:
                        notified = True
            if not notified:
                # MANUAL CONFIG
                with open('/home/ubuntu/PythonCrawl/bool.txt', 'a') as f:
                    f.write("notified"+'\n')
                SC.notify("+821072481535", "SWTEST results are out")
    except:
        print("Critical error occurred :( Closing script...")
        pass
    finally:
        print("Goodbye!")
        SC.close_driver()