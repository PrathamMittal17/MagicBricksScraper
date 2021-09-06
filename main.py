import re
import time
from selenium import webdriver
import pandas as pd
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException

drive_path = "C:\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(drive_path)


def getData(city, path):
    pricelist = []
    bhklist = []
    statuslist = []
    transactionlist = []
    addresslist = []
    arealist = []
    furnishedlist = []
    url = f'https://www.magicbricks.com/property-for-sale/residential-real-estate?&proptype=Multistorey-Apartment,' \
          f'Builder-Floor-Apartment,Penthouse&cityName={city} '
    driver.get(url)

    # getting properties
    yScroll = 8000
    for i in range(1, 4):
        time.sleep(3)
        driver.execute_script(f"window.scrollTo(0,{yScroll})")
        print(i, yScroll)
        yScroll += 8000

    time.sleep(1)
    driver.execute_script(f"window.scrollTo(0,0)")
    time.sleep(4)
    desc_box = driver.find_elements_by_class_name('m-srp-card__title')
    print(len(desc_box))
    # getting data
    for i in range(0, len(desc_box)):
        price = ''
        bhk = ''
        status = ''
        transaction_type = ''
        furnished = ''
        address = ''

        time.sleep(1)

        isselected = driver.find_element_by_id('exitIntent').is_displayed()

        if isselected:#exitIntent > div > div.m-contact__close
            closeisselected = driver.find_elements_by_css_selector('#exitIntent > div > div.m-contact__close')
            closeisselected.click()

        skip = False
        atag = desc_box[i].get_attribute('innerHTML')
        for j in atag.split():
            if "<a" in j:
                skip = True
                break

        if skip:
            print("skip")
            continue

        print(f"{i}")
        desc_box[i].click()
        driver.switch_to.window(driver.window_handles[1])

        price = driver.find_element_by_id('priceSv').text

        try:
            if price == '':
                price = driver.find_element_by_css_selector(
                    '#propertyDetailTabId > div.whiteBgBlock > div.luxury-prop > '
                    'div.luxury-prop__content-block > div.luxury-prop__price-area > '
                    'div:nth-child(1) > div.luxury-prop__price-area__price').text
                price = [float(s) for s in re.findall(r'-?\d+\.?\d*', price)]
                price = price[0] * 100


            else:
                if 'cr' in price.lower():
                    price = [float(s) for s in re.findall(r'-?\d+\.?\d*', price)]
                    price = price[0] * 100
                else:
                    price = [float(s) for s in re.findall(r'-?\d+\.?\d*', price)]
                    price = price[0]



        except:
            price = ''

        bhk = driver.find_element_by_class_name('seeBedRoomDimen').text
        try:
            if bhk == '':
                bhk = driver.find_element_by_css_selector(
                    '#propertyDetailTabId > div.whiteBgBlock > div.luxury-prop > div.luxury-prop__content-block > '
                    'div.luxury-prop__bhk').text
            bhk = [int(s) for s in str.split(bhk) if s.isdigit()]
            bhk = int(bhk[0])

        except NoSuchElementException:
            bhk = ''

        try:
            status = driver.find_elements_by_class_name('p_value')

            for v in status:
                text = v.text.lower()

                if "ready" in text:
                    status = text
                    break
                else:
                    status = 'not ready'




        except:
            transaction_type = ''

        try:
            transaction_type = driver.find_elements_by_class_name('p_value')

            for i, v in enumerate(transaction_type):
                text = v.text.lower()

                if "new" in text:
                    transaction_type = text.splitlines()[0]
                    break
                elif "resale" in text:
                    transaction_type = text.splitlines()[0]
                    break
                else:
                    transaction_type = ''




        except:
            transaction_type = ''

        try:
            address = driver.find_element_by_css_selector('.p_address a').text

            if address == '':
                address = driver.find_element_by_css_selector('.luxury-prop__loc a').text



        except:
            address = ''

        try:
            try:
                area = driver.find_element_by_id('coveredAreaDisplay').text
            except:
                area = driver.find_element_by_id('carpetAreaDisplay').text
        except:
            area = ''

        try:
            furnished = driver.find_elements_by_css_selector('.fltLeft div')

            for i, v in enumerate(furnished):
                text = v.text.lower()

                if "furnish" in text:
                    furnished = text
                    break
                else:
                    furnished = ''


        except:
            furnished = ''

        pricelist.append(price)
        bhklist.append(bhk)
        statuslist.append(status)
        transactionlist.append(transaction_type)
        addresslist.append(address)
        arealist.append(area)
        furnishedlist.append(furnished)

        driver.close()

        driver.switch_to.window(driver.window_handles[0])

    driver.quit()
    tuples = list(zip(pricelist, bhklist, statuslist, transactionlist, addresslist, arealist, furnishedlist))
    df = pd.DataFrame(tuples, columns=["price", "bhk", "status", "transaction", "address", "area", "furnished"])
    if Path(f'{path}\data.csv').is_file():
        df.to_csv(f'{path}\data.csv', index=False, mode='a', header=False)
    else:
        df.to_csv(f'{path}\data.csv', index=False)

    print("Csv file created")


getData("Jaipur", 'F:\')
