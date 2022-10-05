from utils import (get_html_source,
                   get_pdf_link,
                   get_pdf_and_save,
                   pdf_content_check)

from settings import (CHROME_DRIVER_PATH,
                      WORD_TO_FIND,
                      SEARCH_PHRASE_FOR_PDF_LINK,
                      URL_PAGE
                      )


# html_page_source = get_html_source(URL_PAGE, CHROME_DRIVER_PATH)
html_page_source = ''
pdf_link = get_pdf_link(html_page_source, SEARCH_PHRASE_FOR_PDF_LINK)

pdf_file_name = "example_2.pdf"
# get_pdf_and_save(pdf_link=pdf_link, i_filename_to_save=pdf_file_name)
# result = pdf_content_check(pdf_file_name, WORD_TO_FIND)
