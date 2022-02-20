from libraries.common import log_message, capture_page_screenshot, browser
from config import OUTPUT_FOLDER, tabs_dict
from libraries.google.google import Google
from libraries.itunes.itunes import Itunes
import time


class Process:
    def __init__(self):
        log_message("Initialization")
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
            "directory_upgrade": True,
            "download.default_directory": OUTPUT_FOLDER,
            "plugins.always_open_pdf_externally": True,
            "download.prompt_for_download": False
        }
        
        browser.open_available_browser(
            preferences=prefs)
        browser.set_window_size(1920, 1080)
        browser.maximize_browser_window()

        google = Google(browser)
        tabs_dict['Google'] = len(tabs_dict)
        google.access_google()
        self.google = google


    def start(self):
        log_message("Start - Search movie on Google")
        self.google.search_movie()
        log_message("Finish - Search movie on Google")
        
        log_message("Start - Get iTunes URL")
        itunes_url = self.google.get_itunes_link()
        log_message("Finish - Get iTunes URL")
        tabs_dict.pop('Google')

        itunes = Itunes(browser, itunes_url)
        tabs_dict['Itunes'] = len(tabs_dict)
        itunes.access_itunes()
        self.itunes = itunes

        log_message("Start - Get crew members URL")
        self.itunes.get_crew_members_url()
        log_message("Finish - Get crew members URL")

        log_message("Start - Go to crew member tab and get data")
        self.itunes.go_to_crew_member_tab_and_get_data()
        log_message("Finish - Go to crew member tab and get data")

        log_message("Start - Write data to Excel")
        self.itunes.write_data_to_excel()
        log_message("Finish - Write data to Excel")


    def finish(self):
        log_message("DW Process Finished")
        # Good practice: close browser manually
        browser.close_browser()
