# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# from pytrading212 import CFDMarketOrder
# from pytrading212.trading212 import CFD, Mode
#
# email = 'frambrosini1998@gmail.com'
# password = 'Fraambro_98'
#
# # Use your preferred web driver with your custom options
# options = Options()
# # # headless (optional)
# # options.add_argument('--headless')
# # options.add_argument('--disable-gpu')
# # Chrome
# driver = webdriver.Chrome(options=options)
# # or Firefox
# # driver = webdriver.Firefox(options=options)
# cfd = CFD(email, password, driver, mode=Mode.DEMO)
# order = cfd.execute_order(CFDMarketOrder('GOOG', 0.0, 0.1))
# print(order)
#
#
# input()
import requests
from selenium import webdriver

from pytrading212 import CFD, Mode

r = requests.post(url=f"https://demo.trading212.com/rest/v2/trading/open-positions", headers={'Content-Type': 'application/json','Cookie':
                                                                                                  'JSESSIONID=C05970E2EBE4748A346FA1E33FD49689; user_locale={"locale":"it"}; 5d60904a5b52802c63d8b5b97bf8a1ea="224996d9-c7bf-4958-8468-b1090aa338e7"; _ga=GA1.2.1465324166.1616597323; LOGIN_TOKEN=eyJ1c2VybmFtZSI6ImZyYW1icm9zaW5pMTk5OEBnbWFpbC5jb20iLCJ0b2tlbiI6IjQ0NmNmMzA5LTEzZTItNGVlOS1iZDljLTY0NGQzOWIyYjVhOCJ9; LOADING_TEXT_DEMO=UHJhdGljYQ==; __zlcmid=13HjuG7Kq4JFqUs; PLATFORM_LOADED_212=eyJmcmFtYnJvc2luaTE5OThAZ21haWwuY29tIjoiREVNTyJ9; CUSTOMER_SESSION=66eccab5-9f28-4290-8e47-a863ff69f2cf; TRADING_LANG=IT; _gid=GA1.2.418124862.1617012591; LOADING_TEXT_REAL=TW9kYWxpdMOgIERlbmFybyBSZWFsZQ==; TRADING212_SESSION_DEMO=fc844b87-22f2-4438-8de2-8ebcfdf961f0; _gat_UA-101403076-1=1; amp_795329=224996d9-c7bf-4958-8468-b1090aa338e7.Nzc2MzY1MzQtNjJhYy00YzZjLWIyYzctYTcxMjFkYjlmN2Iz..1f1unc2np.1f1upmc1o.k.j.17',
                                                                                              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'},
                  data='{"notify":"NONE","targetPrice":1000000.00,"quantity":0.1,"instrumentCode":"GOOG"}')
print(r.text)
email = 'frambrosini1998@gmail.com'
password = 'Fraambro_98'
driver = webdriver.Chrome()
cfd = CFD(email, password, driver, mode=Mode.DEMO)
