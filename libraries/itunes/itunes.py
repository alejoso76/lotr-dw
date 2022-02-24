from libraries.common import act_on_element, capture_page_screenshot, log_message, files
from config import OUTPUT_FOLDER, tabs_dict

class Itunes:
    def __init__(self, rpa_selenium_instance, url: str) -> None:
        """Inits the class

        Args:
            rpa_selenium_instance (browser): Selenium browser
            url (str): Url of iTunes
        """
        # Minimum 2 variables
        self.browser = rpa_selenium_instance
        self.itunes_url = url
        # Aditional
        self.crew_members_list_dict = ''
        self.crew_movies_dict = ''

    def access_itunes(self):
        """Access Itunes from the browser
        """
        self.browser.go_to(self.itunes_url)

    def get_crew_members_url(self):
        """Gets the name of the crew member and its tab link. If a member has already been checked, it will not duplicate it (Unique)
        """
        crew_members = act_on_element(
            '//div[@class="l-row cast-list"]//dd[@class="cast-list__detail"]/a', "find_elements")
        crew_members_unique = []
        crew_names = []

        for crew_member in crew_members:
            if crew_member.text in crew_names:
                continue
            else:
                crew_member_data = {
                    'name': crew_member.text,
                    'url': crew_member.get_attribute('href')
                }
                crew_names.append(crew_member.text)
                crew_members_unique.append(crew_member_data)

        self.crew_members_list_dict = crew_members_unique

    def go_to_crew_member_tab_and_get_data(self):
        """Goes to each unique crew member tab and gets data from the movies
        """
        # Open tab
        self.browser.execute_javascript('window.open()')
        # Go to tab
        self.browser.switch_window(locator='NEW')
        tabs_dict['Crew Member'] = len(tabs_dict)
        # Crew members that failed to open tab or get data
        pending_crew_members = []
        # Dict that has crew member name as key and value a list of dicts
        crew_movies_dict = {}
        for crew_member in self.crew_members_list_dict:
            # Go to url in tab
            try:
                # Go to url
                self.browser.go_to(crew_member['url'])

                # Find movies and its genres
                movies = act_on_element('//section[div/h2[text()="Movies"]]//div[@class="l-row l-row--peek"]/a//div[@class="we-lockup__title "]/div', 'find_elements')[:5]
                genres = act_on_element('//section[div/h2[text()="Movies"]]//div[@class="l-row l-row--peek"]/a//div[@class="we-truncate we-truncate--single-line  we-lockup__subtitle"]', 'find_elements')[:5]
                
                # List to pass to excel
                movies_genres_list = []
                for movie, genre in zip(movies, genres):
                    dict_movie_genre = {
                        'Name': movie.text,
                        'Genre': genre.text
                    }
                    movies_genres_list.append(dict_movie_genre)
                crew_movies_dict[crew_member["name"]] = movies_genres_list
            except:
                # If fails, append to pending list
                pending_crew_members.append(crew_member)



        # Search the pending crew
        for pending_crew_member in pending_crew_members:
            # TODO: Capture page if fails
            # Go to url in tab
            self.browser.go_to(crew_member['url'])
            tabs_dict[F'Itunes-{crew_member["name"]}'] = len(tabs_dict)
            try:
                #TODO: Add data proccess here
                movies = act_on_element('//section[div/h2[text()="Movies"]]//div[@class="l-row l-row--peek"]/a//div[@class="we-lockup__title "]/div', 'find_elements')[:5]
                genres = act_on_element('//section[div/h2[text()="Movies"]]//div[@class="l-row l-row--peek"]/a//div[@class="we-truncate we-truncate--single-line  we-lockup__subtitle"]', 'find_elements')[:5]
                
                movies_genres_list = []
                for movie, genre in zip(movies, genres):
                    dict_movie_genre = {
                        'Name': movie.text,
                        'Genre': genre.text
                    }
                    movies_genres_list.append(dict_movie_genre)
                crew_movies_dict[crew_member["name"]] = movies_genres_list
            except Exception as e:
                # If fails, append to pending list
                capture_page_screenshot(OUTPUT_FOLDER)
                log_message(
                    "An unexpected error was enconutered during the process: {}".format(str(e)))

        # Close tab
        self.browser.execute_javascript('window.close()')
        # Go to initial tab
        self.browser.switch_window(locator=self.browser.get_window_handles()[tabs_dict['Itunes']])
        # Remove tab from tabs_dict
        tabs_dict.pop('Crew Member')
        self.crew_movies_dict = crew_movies_dict

    def write_data_to_excel(self):
        """Writes the data extracted to an excel file
        """
        files.create_workbook(path=F'{OUTPUT_FOLDER}/lotr_cast.xlsx')

        for key, value in self.crew_movies_dict.items():
            files.create_worksheet(
                name=key,
                content=None,
                exist_ok=False,
                header=False
            )
            files.append_rows_to_worksheet(
                value,
                name=key,
                # If dict keys will be headers
                header=True,
                # Start writing the data first row -> Leaving it for the header
                # * Start=None if and only if header=True
                # To avoid overwriting the headers
                start=None)

        # Delete Sheet sheet (default sheet)
        files.remove_worksheet(name='Sheet')
        files.save_workbook(path=None)
        files.close_workbook()
