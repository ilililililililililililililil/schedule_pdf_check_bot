import re, sys, fitz, requests
from selenium import webdriver


def get_html_source(url_page, chrome_driver_path):
    driver = webdriver.Chrome(chrome_driver_path)
    driver.get(url_page)
    o_html_source = ''
    o_html_source = driver.page_source
    driver.close()
    driver.quit()

    return o_html_source


def get_pdf_link(i_html_source: str, search_phrase: str) -> str:

    soup = BeautifulSoup(i_html_source, "html.parser")
    txt_data_array = soup.select_one("a")
    data = txt_data_array.find_all("title")

    for line in data:
        print(str(line))

    o_link: str = 'empty'

    return o_link


def get_pdf_and_save(pdf_link: str, i_filename_to_save: str):
    response = requests.get(pdf_link)
    open(i_filename_to_save, "wb").write(response.content)
