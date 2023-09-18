from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import (
    get_chrome_webdriver,
    get_chrome_webdriver_options,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_browser_delay,
    DIRECTORY,
    NAME,
    CURRENCY,
    MAX_PRICE,
    FILTERS,
    BASE_URL
)


class GenerateReport:
    def __init__(self):
        pass

class AmazonAPI:
    def __init__(self, search_item, base_url, filters, currency):
        self.base_url=base_url
        self.search_item=search_item
        self.filters=filters
        self.currency=currency
        options=get_chrome_webdriver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        set_browser_delay(options)
        self.driver=get_chrome_webdriver(options)
        self.driver.maximize_window()
        self.price_filters=f'&rh=p_36%3A{filters["min"]}00-{filters["max"]}00'

    def run(self):
        print('Starting Script...')
        print(f'Looking for {self.search_item} products...')
        links=self.get_products_links()
        if not links:
            print('Nothing Found! Stopping Scrapper..')
            return
        print(f'Got {len(links)} links to products')
        print('Getting info about products...')
        products=self.get_products_info(links)
        print(f"Got info about {len(products)} products...")

        # self.driver.quit()
        return products

    def get_products_info(self,links):
        asins=self.get_asins(links)
        products=[]
        for asin in asins:
            product=self.get_single_product_info(asin)
            if product:
                products.append(product)
            return products

    def get_single_product_info(self,asin):
        print(f'Getting Data -> Product ID: {asin}')
        prod_short_url=self.shorten_url(asin)
        self.driver.get(prod_short_url)
        title=self.get_title()
        print(title)
        seller=self.get_seller()
        print(seller)
        print('URL: ', self.driver.current_url)
        price=self.get_price()
        availability=None
        if price==None:
            price=float(0.0)
            availability='Not Available'
        else:
            price = float(price.split(self.currency)[1])
            availability='Available'
        if title and seller and price:
            product_info = {
                'asin': asin,
                'url': prod_short_url,
                'availability': availability,
                'title': title,
                'seller': seller,
                'price': price
            }
            return product_info
        return None

    def get_title(self):
        try:
            return self.driver.find_element(By.ID,'productTitle').text
        except Exception as e:
            print(f'Couldn\'t get title of product - {self.driver.current_url}')
            print(str(e))
            return None

    def get_seller(self):
        try:
            return self.driver.find_element(By.ID,'bylineInfo').text
        except Exception as e:
            print(f'Couldn\'t get seller of product - {self.driver.current_url}')
            print(str(e))
            return None

    # def get_price(self):
    #     try:
    #         # # price_element = self.driver.find_element(By.ID,'corePrice_desktop')
    #         # price_tag = self.driver.find_element(By.CLASS_NAME,'a-lineitem')
    #         # price = price_tag.find_element(By.CLASS_NAME,'a-offscreen').text
    #         # # price = self.driver.find_element(By.CLASS_NAME,'a-price-whole').text
    #         # print(price)
    #         wait = WebDriverWait(self.driver, 4)  # Wait up to 10 seconds for website to load data dynamically
    #         # price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'a-offscreen')))
    #         # price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'aok-offscreen')))
    #         # price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'apexPriceToPay')))
    #         price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'priceToPay')))
    #         if not price_element:
    #             price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'apexPriceToPay')))

    #         price=price_element.text
    #         print(price)
    #     except Exception as e:
    #         print(f'Couldn\'t get price of product - {self.driver.current_url}')
    #         print(str(e))
    #         return None


    def get_price(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            price_element = None

            # Try to locate the price element using different class names
            possible_class_names = ['a-offscreen', 'apexPriceToPay', 'priceToPay']

            for class_name in possible_class_names:
                try:
                    price_element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
                    if price_element:
                        break
                except Exception:
                    pass

            if price_element:
                price = price_element.text.strip()
                print(price)
            else:
                print('Price element not found')
                return None
        except Exception as e:
            print(f'Couldn\'t get price of product - {self.driver.current_url}')
            print(str(e))
            return None


    def shorten_url(self,asin):
        return self.base_url+'dp/'+asin



    def get_asins(self,links):
        return [self.get_asin(link) for link in links]

    def get_asin(self,prod_link):
        # this will return what is present between '/dp/' and '/ref' -> simply the id of product
        return prod_link[prod_link.find('/dp/') + 4 :prod_link.find('/ref')]


    def get_products_links(self):
        self.driver.get(self.base_url)
        # search_bar = self.driver.find_element('xpath','//input[@id="twotabsearchtextbox"]')
        search_bar = self.driver.find_element(By.ID,'twotabsearchtextbox')
        search_bar.send_keys(self.search_item)
        search_bar.send_keys(Keys.ENTER)
        self.driver.get(f'{self.driver.current_url}{self.price_filters}')
        result_list=self.driver.find_element(By.CLASS_NAME,'s-result-list')
        print(result_list)
        links=[]
        # try:
        #     results=result_list.find_elements(By.TAG_NAME, 'h2')
        #     # results=result_list.find_elements(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a')
        #     for result in results:
        #         href=result.get_attribute('href')
        #         print('trying')
        #         links.append(href)
        #     # links=[link.get_attribute('href') for link in results]
        # except Exception as e:
        #     print('Didn;t get any results')
        #     print(str(e))
        
        # print(links)
        try:
            titles=result_list.find_elements(By.TAG_NAME, 'h2')
            for title in titles:
                anchor_tag=title.find_element(By.TAG_NAME,'a')
                href=anchor_tag.get_attribute('href')
                print(href)
                links.append(href)
        except Exception as e:
            print('Didn\'t get any results')
            print(str(e))
        return links





# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div/div/div[2]/div/div/div[1]/h2/a


if __name__ == '__main__':
    print('Starting Script')
    amazon=AmazonAPI(NAME,BASE_URL,FILTERS,CURRENCY)
    print(amazon.price_filters)
    data = amazon.run()
    print(data)





