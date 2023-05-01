import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class Data:
    def __init__(self):
        self.layout_names = []
        self.image_paths = []
        self.costs_info = []
        self.size = []
        self.tiles = []
        self.space_eff = []
        self.production_info = []

        self.driver = None
        self.driver_setup()
        self.soup = BeautifulSoup(self.driver.page_source, features='lxml')
        self.extract_data_elements()
        self.extract_images()
        self.create_data_frame()
        self.driver.quit()

    def driver_setup(self):
        # Setup headless browser option.
        options = Options()
        options.add_argument('--headless=new')
        # Use the webdriver_manager library to get the Chrome driver.
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.driver.get('https://anno1800.fandom.com/wiki/Production_layouts')

    def extract_data_elements(self):
        def clean_data_string(string, classification=None):
            # Remove unnecessary information and white space
            data_string = string
            data_string = data_string.split(':')[1]
            data_string = data_string.strip()

            # Split the data values into their own strings.
            if classification == 'Construction' or classification == 'Production':
                data_string = data_string.split('•')

            return data_string

        # The layout name is in a <p> tag with an inline <span> tag all with the same style.
        for name in self.soup.find_all(attrs={'style': 'font-size:125%'}):
            self.layout_names.append(name.find('b').text)

        costs_data = []
        costs_types = []
        production_data = []
        production_types = []

        # Most of the data needed is in an HTML table. To keep each data point for each layout together, find the
        # beginning of each table definition. Then go through the data cells to extract the relevant data.
        for element in self.soup.find_all('tbody'):
            # Using a boolean flag to know when to add an entry to the production list when there is no data listed on
            # the website. This will keep the production data list the same size as the other data lists.
            production_found = False
            for cell in element.find_all('td'):
                if cell.find('b').text == 'Construction costs':
                    # Format the extracted string
                    costs_data.append(clean_data_string(cell.text, 'Construction'))

                    # Get the type of material by extracting the image name since the materials are represented by
                    # images on the website.
                    materials = []
                    for material_type in cell.find_all('img'):
                        material_data_string = material_type.get('alt')
                        material_data_string = material_data_string.split('.')[0]
                        materials.append(material_data_string)
                    costs_types.append(materials)

                if cell.find('b').text == 'Size':
                    self.size.append(clean_data_string(cell.text))

                if cell.find('b').text == 'Tiles':
                    self.tiles.append(clean_data_string(cell.text))

                if cell.find('b').text == 'Space Efficiency':
                    self.space_eff.append(clean_data_string(cell.text))

                if cell.find('b').text == 'Production (per minute)':
                    production_found = True
                    production_data.append(clean_data_string(cell.text, 'Production'))
                    produce = []
                    for produce_type in cell.find_all('img'):
                        produce_data_string = produce_type.get('alt')
                        produce_data_string = produce_data_string.split('.')[0]
                        produce.append(produce_data_string)
                    production_types.append(produce)

            # When there is no production data on the table, add an empty string to keep the lists size consistent with
            # the rest of the data lists.
            if not production_found:
                production_data.append('')
                production_types.append('')

        # Match the cost type with the cost value with a dictionary and store each dictionary in a list.
        for i in range(len(costs_types)):
            self.costs_info.append(dict(zip(costs_types[i], costs_data[i])))

        # Match the production type with the production value with a dictionary and store each dictionary in a list.
        for i in range(len(production_data)):
            self.production_info.append(dict(zip(production_types[i], production_data[i])))

        # At the time of writing this program, one layout on the website had an error with its image but had the other
        # fields of data. Removing this data is needed to keep the lists of data consistent with the image data.
        bad_data_index = self.layout_names.index('Canned Food 06 WH TU - [Recipe Archivist]')
        self.layout_names.pop(bad_data_index)
        self.costs_info.pop(bad_data_index)
        self.size.pop(bad_data_index)
        self.tiles.pop(bad_data_index)
        self.space_eff.pop(bad_data_index)
        self.production_info.pop(bad_data_index)

    def extract_images(self):
        # Find the image information in the HTML.
        image_results = self.driver.find_elements(By.XPATH, "//figure[contains(@class, 'thumb tleft show-info-icon')]")

        images = []

        # Extract the links to the image.
        for result in image_results:
            image = result.find_element(By.CLASS_NAME, 'image')
            images.append(image.get_attribute('href'))

        # Download the image and save the image locally.
        for i in range(len(image_results)):
            self.image_paths.append(urllib.request.urlretrieve(
                str(images[i]), f"images/layout_images/{self.layout_names[i].split('-')[0]}.jpg".format(i))[0])

    def create_data_frame(self):
        names_series = pd.Series(self.layout_names, name='Names')
        image_series = pd.Series(self.image_paths, name='Image')
        costs_series = pd.Series(self.costs_info, name='Cost')
        size_series = pd.Series(self.size, name='Size')
        tiles_series = pd.Series(self.tiles, name='Tiles')
        space_eff_series = pd.Series(self.space_eff, name='Space Efficiency')
        production_series = pd.Series(self.production_info, name='Production')

        df = pd.DataFrame({
            'Name': names_series,
            'Image': image_series,
            'Cost': costs_series,
            'Size': size_series,
            'Tiles': tiles_series,
            'Space Efficiency': space_eff_series,
            'Production': production_series})
        df.to_csv('names.csv', index=False, encoding='utf-8')
