import time
from utils import (get_html_source,
                   get_pdf_link,
                   get_pdf_and_save,
                   pdf_content_check,
                   get_datetime_now)

from settings import (CHROME_DRIVER_PATH,
                      WORD_TO_FIND,
                      SEARCH_PHRASE_FOR_PDF_LINK,
                      URL_PAGE,
                      PIC_PATH,
                      PDF_PATH,
                      HTML_PATH
                      )

stop_working = 0
delay = 600
print('Program starts at:', get_datetime_now('full'))
print('Delay between requests is: ', delay, 'seconds')
print('_________________________________________________')

while stop_working != 1:
    html_page_source = get_html_source(URL_PAGE, CHROME_DRIVER_PATH)
    # html_page_source = '' # manual file for
    pdf_link = get_pdf_link(html_page_source, SEARCH_PHRASE_FOR_PDF_LINK)

    pdf_fname = get_datetime_now('full') + '.pdf'
    pdf_file_name = PDF_PATH + '/' + pdf_fname
    get_pdf_and_save(pdf_link, pdf_file_name)
    result = pdf_content_check(pdf_file_name, WORD_TO_FIND, PIC_PATH)

    for key, value in result.items():
        print('one more try at:', get_datetime_now('small'))
        print('Key: ', key, ', result: ', value)
        print('________________________')

        if key == WORD_TO_FIND.upper():
            stop_working = 1

    time.sleep(delay)
