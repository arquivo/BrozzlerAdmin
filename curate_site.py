import os

import rethinkstuff

from selenium import webdriver

# TODO this do not work, if warcprox meta is not sent for every request with the right warcprox_meta the captures will
# go to another WARC and deduplication will also not work (bucket + hashpayload)
# Manual Solution is to use the addon ModHeader or launch a special warcprox instance with this
# meta information prefconfigured

# TODO it needs to launch a unique warcprox instance with the PREFIX pre configured


# https://github.com/nlevitt/rethinkstuff
r = rethinkstuff.Rethinker(['localhost:28015'], 'brozzler')
site = list(r.table('sites').filter({"job_id": "lisbon.greenhackathon.com"}).run())

# proxy = site[0]['proxy']
proxy = "localhost:8001"
warcprox_meta = site[0]['warcprox_meta']
user_agent = site[0]['user_agent']
cookie_db = site[0]['cookie_db']

webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy": proxy,
    "ftpProxy": proxy,
    "sslProxy": proxy,
    "noProxy": None,
    "proxyType": "MANUAL",
    "autodetect": False
}

chromedrive = "/home/dbicho/Desktop/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedrive
browser = webdriver.Chrome(chromedrive)
browser.get("http://lisbon.greenhackathon.com")

while browser:
    pass
