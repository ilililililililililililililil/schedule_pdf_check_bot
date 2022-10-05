import re, sys, fitz, requests

from selenium import webdriver
from bs4 import BeautifulSoup

from utils import (get_html_source,
                   get_pdf_link,
                   get_pdf_and_save)

from settings import (CHROME_DRIVER_PATH,
                      WORD_TO_FIND,
                      SEARCH_PHRASE_FOR_PDF_LINK,
                      URL_PAGE
                      )

html_page_source = get_html_source(URL_PAGE, CHROME_DRIVER_PATH)
pdf_link = get_pdf_link(html_page_source, SEARCH_PHRASE_FOR_PDF_LINK)
pdf_file_name = "example_2.pdf"
get_pdf_and_save(pdf_link=pdf_link, i_filename_to_save=pdf_file_name)

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

            if WORD_TO_FIND.upper() in w5.upper():
                print(w5,'Got it!')
