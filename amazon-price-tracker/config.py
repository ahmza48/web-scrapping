from selenium import webdriver

DIRECTORY= 'reports'
NAME= 'PS4'
CURRENCY= '$'
MIN_PRICE= '250'
MAX_PRICE= '850'
FILTERS={
    'min': MIN_PRICE,
    'max': MAX_PRICE
}

# BASE_URL='https://www.amazon.de/'
BASE_URL='https://www.amazon.com/'

def get_chrome_webdriver(options):
    return webdriver.Chrome(options=options)

def get_chrome_webdriver_options():
    return webdriver.ChromeOptions()

def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')

def set_browser_as_incognito(options):
    options.add_argument('--incognito')

def set_browser_delay(options):
    options.add_experimental_option('detach',True)