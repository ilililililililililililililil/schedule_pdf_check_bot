import re, sys
import datetime as dt
import fitz, requests
from numpy import number
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_datetime_now(mode):
    d = dt.datetime.now()
    o_ret_full = str(d.day) + '.' + str(d.month) + '.' + str(d.year)
    o_ret_full += '_at_' + str(d.hour) + '.' + str(d.minute)
    o_ret_small = str(d.hour) + '.' + str(d.minute)
    if mode == 'full':
        return o_ret_full
    else:
        return o_ret_small


def get_html_source(url_page, chrome_driver_path):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_driver_path)
    driver.get(url_page)
    o_html_source = ''
    o_html_source = driver.page_source
    driver.close()
    driver.quit()

    return o_html_source


def get_pdf_link(i_html_source: str, search_phrase: str):

    # manual file parse for
    # with open("example.html") as fp:
    #     soup = BeautifulSoup(fp, "html.parser")

    soup = BeautifulSoup(i_html_source, "html.parser")
    data = soup.find_all("a")
    pdf_link: str = ''
    for a_item in data:
        event_title: str = a_item.text
        link_title: str = a_item.get("title")
        if link_title:
            if link_title.upper() == search_phrase.upper():
                pdf_link = a_item.get("href")

            if pdf_link is False:
                text = "ДЕКАБРЬ"
                if event_title:
                    if text.upper() in event_title.upper():
                        pdf_link = a_item.get("href")

    if pdf_link:
        first_link_part = "https://2011.bolshoi.ru" 
        o_link = first_link_part + pdf_link
    else:
        o_link = 'NO_LINK'
    return o_link


def get_pdf_and_save(pdf_link: str, i_filename_to_save: str):
    response = requests.get(pdf_link)
    open(i_filename_to_save, "wb").write(response.content)


def pdf_content_check(pdf_file_name: str, word_to_find: str, pic_output_path: str):
    phrase_found = ''
    o_result = {}
    # To get better resolution
    zoom_x = 3.0  # horizontal zoom
    zoom_y = 3.0  # vertical zoom
    matrix = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

    doc = fitz.open(pdf_file_name)
    for current_page in range(len(doc)):
        phrase_found = ''
        page = doc.load_page(current_page)
        page_text = page.get_textpage('blocks')

        data = page_text.extractBLOCKS()
        for item in data:
            w1, w2, w3, w4, w5, w6, w7 = item

            if 'озеро'.upper() in w5.upper():
                result = str(w5) + 'Got it!'
                o_result['озеро'.upper()] = str(w5)

            if word_to_find.upper() in w5.upper():
                phrase_found = 'X'
                # result = str(w5) + 'Got it!'
                o_result[word_to_find.upper()] = str(w5) + ' Найдено!'

            if phrase_found == 'X':
                png_fname = get_datetime_now('full') + '.png'
                # ffile = 'pdf_pic_proof_%i.png' % page.number
                pic_fname = pic_output_path + '/' + png_fname
                pic = page.get_pixmap(matrix=matrix)
                pic.save(pic_fname)

    return o_result
