import re, sys, fitz, requests
from selenium import webdriver
from selenium import webdriver
from bs4 import BeautifulSoup


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


def pdf_content_check(file_name: str, word_to_fine: str):
    doc = fitz.open(pdf_file_name)
    i = 0
    for current_page in range(len(doc)):
        i += 1
        if i == 1:
            page = doc.load_page(current_page)
            page_text = page.get_textpage('blocks')
            # print(page_text.extractBLOCKS())
            # data = page_text.extractWORDS()
            # data = page_text.extractBLOCKS()
            # if_word_exist = page_text.search(WORD_TO_FIND, quads=False)
            data = page_text.extractBLOCKS()
            for item in data:
                w1, w2, w3, w4, w5, w6, w7 = item

                if word_to_fine.upper() in w5.upper():
                    o_result = str(w5) + 'Got it!'
    return o_result