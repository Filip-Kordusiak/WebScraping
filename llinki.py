from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv

# Konfiguracja ścieżki do chromedriveraclea
chrome_driver_path = "C:\chromedriver\chromedriver.exe"  # Zmień na właściwą ścieżkę do chromedrivera

# Opcje przeglądarki (opcjonalne)
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Uruchomienie przeglądarki w trybie pełnoekranowym

# Inicjalizacja przeglądarki
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Otwieranie strony internetowej
driver.get(f"https://login.compl")  # Zmień na URL strony, na którą chcesz się zalogować

# Szukanie pola loginu
login_field = driver.find_element(By.NAME, "username")  # Zmień na prawidłowy identyfikator pola loginu
login_field.send_keys("777777")  # Wprowadź login

# Szukanie pola hasła
password_field = driver.find_element(By.NAME, "password")  # Zmień na prawidłowy identyfikator pola hasła
password_field.send_keys("7777777")  # Wprowadź hasło

# Wysłanie formularza logowania (np. kliknięcie przycisku 'Zaloguj')
login_button = driver.find_element(By.NAME, "login-btn")  # Zmień na prawidłowy selektor przycisku
login_button.click()
time.sleep(5)
cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")  # Zmień na prawidłowy selektor przycisku
cookies_button.click()

# Czekanie kilka sekund, aby strona się załadowała
time.sleep(1)

href_set = set()

# Powtarzanie dla 10 stron (page=x)
for x in range(1, 168):  # Pętla od 1 do 10
    # Dynamicznie zmieniany URL z numerem strony
    url = f"https://www..com/shop-pl/pl/search/?page={x}"
    
    # Otwieranie strony z odpowiednią numeracją
    driver.get(url)
    time.sleep(7)
    # Szukanie wszystkich elementów 'a', które mają w klasie 'ui-item-tile__link'
    link_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'ui-item-tile__link')]")

    # Iteracja przez znalezione elementy i pobieranie wartości href
    for element in link_elements:
        href_value = element.get_attribute("href")
        href_set.add(href_value)  # Dodanie href do zbioru

    # Dla bezpieczeństwa dodajemy krótki czas oczekiwania na załadowanie strony
    time.sleep(5)  # Oczekiwanie 2 sekundy na załadowanie strony

# Wyświetlenie zbioru wszystkich unikalnych href
print(href_set)
print("len",len(href_set))
with open('href_set_Kver.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Zapisujemy każdy element zestawu w nowym wierszu
    for href in href_set:
        writer.writerow([href])
x = 0
input(x)
# Zamykanie przeglądarki
driver.quit()