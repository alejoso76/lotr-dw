from libraries.common import act_on_element, capture_page_screenshot, log_message
from config import OUTPUT_FOLDER

class Google:
    def __init__(self, rpa_selenium_instance) -> None:
        """Inits the class

        Args:
            rpa_selenium_instance (browser): Selenium browser
        """
        # Minimum 2 variables
        self.browser = rpa_selenium_instance
        self.google_url = 'https://www.google.com/ncr'

    def access_google(self):
        """Access Google from the browser
        """
        self.browser.go_to(self.google_url)

    def search_movie(self):
        """Searches the movie LOTR on Google
        """
        self.browser.input_text_when_element_is_visible(
            '//input[@title="Search"]', 'the lord of the rings the return of the king itunes movies us')
        act_on_element(
            '//div[@class="FPdoLc lJ9FBc"]//input[@value="Google Search"]', "click_element")
    
    def get_itunes_link(self) -> str:
        """Obtains the first itunes link

        Returns:
            str: URL of iTunes
        """
        link_to_itunes = act_on_element('(//div[@id="rso"]/div[@class="g tF2Cxc"]//a[contains(@href, "itunes")])[1]', 'find_element')
        link_to_itunes = link_to_itunes.get_attribute('href')
        return link_to_itunes

