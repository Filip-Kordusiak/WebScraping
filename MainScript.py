import time
import csv
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


def get_product_info(driver):
    try:
    # Pobieramy element h1 zawierający zarówno ItemNumber, jak i ItemName
        product_header = driver.find_element(By.CSS_SELECTOR, "h1[data-testid='ProductHeader']")

    # Pobieramy wartości z poszczególnych spanów
        item_number = product_header.find_element(By.CSS_SELECTOR, "span[data-testid='ItemNumber']").text
        item_name = product_header.find_element(By.CSS_SELECTOR, "span[data-testid='ItemName']").text

    # Łączenie tych wartości w jeden ciąg znaków
        product_full_name = f"{item_name}"
        print(f"Produkt: {product_full_name}")

    except Exception as e:
        print(f"Błąd podczas pobierania numeru i nazwy produktu: {e}")
    try:
        # Wyciągnięcie ItemNumber
        item_number = driver.find_element(By.CSS_SELECTOR, "span[data-testid='ItemNumber']").text
        print(f"ItemNumber: {item_number}")
    except Exception as e:
        print(f"Nie udało się znaleźć 'ItemNumber': {e}")
        item_number = None

    try:
        # Wyciągnięcie ceny netto produktu
        net_price = driver.find_element(By.CSS_SELECTOR, "h2[data-testid='ProductNetPrice'] span").text
        print(f"Cena netto: {net_price}")
    except Exception as e:
        print(f"Nie udało się znaleźć ceny netto produktu: {e}")
        net_price = None

    try:
        # Wyciągnięcie informacji o dostępności produktu (np. "18 za 4 dni")
        availability_info = driver.find_element(By.CSS_SELECTOR, "span.kh-12e2jbd").text
        print(f"Informacja o dostępności: {availability_info}")
    except Exception as e:
        print(f"Nie udało się znaleźć informacji o dostępności: {e}")
        availability_info = None

    try:
        # Szukanie kodu EAN w tabeli
        ean_row = driver.find_element(By.XPATH, "//tr[th/span[text()='EAN']]")
        ean_code = ean_row.find_element(By.CSS_SELECTOR, "td.kh-1yk0fx9").text.strip()
        print(f"EAN: {ean_code}")
    except Exception as e:
        print(f"Nie udało się znaleźć kodu EAN: {e}")
        ean_code = None

    try:
        # Szukanie href dla producenta
        producer_link = driver.find_element(By.CSS_SELECTOR, "a.kh-1aous46").get_attribute("href")
        print(f"ProducentNazwa: {producer_link}")
    except Exception as e:
        print(f"Nie udało się znaleźć producenta: {e}")
        producer_link = None

    try:
        # Wyciąganie breadcrumb
        breadcrumb_elements = driver.find_elements(By.CSS_SELECTOR, "ul[data-testid='Breadcrumbs'] li a")
        breadcrumbs = [element.text for element in breadcrumb_elements]
        breadcrumb_path = "-".join(breadcrumbs)
        print(f"Breadcrumbs: {breadcrumb_path}")
    except Exception as e:
        print(f"Nie udało się znaleźć breadcrumb: {e}")
        breadcrumb_path = None

    return product_full_name, item_number, net_price, availability_info, ean_code, producer_link, breadcrumb_path


def download_images_from_class(driver, class_name, folder_prefix="zdj"):
    try:
        item_number = driver.find_element(By.CSS_SELECTOR, "span[data-testid='ItemNumber']").text
    except Exception as e:
        print(f"Nie udało się znaleźć numeru 'ItemNumber': {e}")
        return
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, class_name))
        )
    except TimeoutException:
        print(f"Nie znaleziono elementów z klasą: {class_name}")
        return

    buttons = driver.find_elements(By.CSS_SELECTOR, f".{class_name} button")
    image_links = []

    for button in buttons:
        try:
            img_tag = button.find_element(By.TAG_NAME, "img")
            src = img_tag.get_attribute("src")
            modified_src = src.replace("profile=thumb", "profile=krampd_rd")
            image_links.append(modified_src)
        except Exception as e:
            print(f"Błąd podczas pobierania linku: {e}")
            continue

    def download_image(url, folder, filename):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(os.path.join(folder, filename), 'wb') as file:
                    file.write(response.content)
        except Exception as e:
            print(f"Błąd podczas pobierania obrazu: {e}")

    for i, img_link in enumerate(image_links):
        folder_name = f"{folder_prefix}{i + 1}"
        os.makedirs(folder_name, exist_ok=True)
        file_name = f"{item_number}.jpg"
        download_image(img_link, folder_name, file_name)


chrome_driver_path = "C:\\chromedriver\\chromedriver.exe"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get(f"https://login..com/?redirectTo=https%3A%2F%2Fwww..com%2Fshop-pl%2Fpl&country=pl&lang=pl")
    login_field = driver.find_element(By.NAME, "username")
    login_field.send_keys("877777")
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("777777")
    login_button = driver.find_element(By.NAME, "login-btn")
    login_button.click()

    time.sleep(5)
    
    cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookies_button.click()
except Exception as e:
    print(f"Błąd podczas logowania: {e}")

with open('href_set.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    
    for row in reader:
        url = row[0]
        print(f"Przechodzę do: {url}")
        
        try:
            driver.get(url)
            time.sleep(5)
            
            input_field = driver.find_element(By.CSS_SELECTOR, "input[data-testid='SetQuantityInput']")
            input_field.clear()
            input_field.send_keys("9999")

            buttons = driver.find_elements(By.CSS_SELECTOR, "span[data-testid='show-loadable-value']")
            time.sleep(3)

            if len(buttons) >= 2:
                buttons[0].click()
                buttons[1].click()
            else:
                print("Za mało elementów do kliknięcia.")
            
            time.sleep(5)

            rows = driver.find_elements(By.CSS_SELECTOR, "table[data-test-id='attributes-list'] tr")
            
            
            ###
            html_output = "<table><tbody>"

            for row in rows:
                try:
        # Pobieranie nagłówka
                    header = row.find_element(By.TAG_NAME, "th").text

        # Pobieranie wartości z komórki `td`
                    value_element = row.find_element(By.TAG_NAME, "td")

        # Sprawdzenie, czy w `td` znajduje się lista `ul`
                    ul_element = value_element.find_elements(By.TAG_NAME, "ul")
        
                    if ul_element:
            # Pobieranie wszystkich elementów `li` i łączenie ich w jedną linię tekstu
                        li_elements = value_element.find_elements(By.TAG_NAME, "li")
                        value = ", ".join([li.text.strip() for li in li_elements])
                    else:
            # Jeśli nie ma listy, pobieranie tekstu bezpośrednio z komórki `td`
                        value = value_element.text.strip()

        # Dodawanie wiersza do HTML output
                    html_output += f"<tr><th>{header}</th><td>{value}</td></tr>"
                except Exception as e:
                    print(f"Błąd podczas przetwarzania wiersza: {e}")

            html_output += "</tbody></table>"

# Wyświetlenie przetworzonego HTML
            print(html_output)
            
            
            
            '''
            html_output = "<table><tbody>"

            for row in rows:
                try:
                    header = row.find_element(By.TAG_NAME, "th").text
                    value = row.find_element(By.TAG_NAME, "td").text.strip()
                    html_output += f"<tr><th>{header}</th><td>{value}</td></tr>"
                except Exception as e:
                    print(f"Błąd podczas przetwarzania wiersza: {e}")

            html_output += "</tbody></table>"
            print(html_output)
'''
            download_images_from_class(driver, "kh-1vrm80b")
            product_full_name, item_number, net_price, availability_info, ean_code, producer_link, breadcrumb_path = get_product_info(driver)
            print("Dane:",product_full_name, item_number, net_price, availability_info, ean_code, producer_link, breadcrumb_path)

            do_csv = url + "$%^&" + str(product_full_name) + "$%^&" + str(item_number) + "$%^&" + str(ean_code) + "$%^&&" + str(net_price) + "$%^&" + html_output + "$%^&" + str(availability_info) + "$%^&" + str(producer_link) + "$%^&" + str(breadcrumb_path)
            
            with open('plik.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([do_csv])
        
        except Exception as e:
            print(f"Błąd podczas przetwarzania strony: {e}")

driver.quit()
