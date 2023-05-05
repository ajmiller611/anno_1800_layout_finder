import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor


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
        self.soup = None

    def driver_setup(self, progress_var):
        # Setup headless browser option.
        options = Options()
        options.add_argument('--headless=new')

        # The driver setup logic is separated into four parts to update the progress bar.
        progress_var.set(progress_var.get() + 0.25)

        # Use the webdriver_manager library to get the Chrome driver.
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        progress_var.set(progress_var.get() + 0.25)

        # Give the url to load the target web page.
        self.driver.get('https://anno1800.fandom.com/wiki/Production_layouts')
        progress_var.set(progress_var.get() + 0.25)

        # Setup BeautifulSoup with the source HTML and the HTML parser.
        self.soup = BeautifulSoup(self.driver.page_source, features='html.parser')
        progress_var.set(progress_var.get() + 0.25)

    def extract_data_elements(self, progress_var):
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

        # The extract data elements logic is separated into five parts for the progress bar.
        progress_var.set(progress_var.get() + 0.20)

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
        progress_var.set(progress_var.get() + 0.20)

        # Match the cost type with the cost value with a dictionary and store each dictionary in a list.
        for i in range(len(costs_types)):
            self.costs_info.append(dict(zip(costs_types[i], costs_data[i])))
        progress_var.set(progress_var.get() + 0.20)

        # Match the production type with the production value with a dictionary and store each dictionary in a list.
        for i in range(len(production_data)):
            self.production_info.append(dict(zip(production_types[i], production_data[i])))
        progress_var.set(progress_var.get() + 0.20)

        # At the time of writing this program, one layout on the website had an error with its image but had the other
        # fields of data. Removing this data is needed to keep the lists of data consistent with the image data.
        bad_data_index = self.layout_names.index('Canned Food 06 WH TU - [Recipe Archivist]')
        self.layout_names.pop(bad_data_index)
        self.costs_info.pop(bad_data_index)
        self.size.pop(bad_data_index)
        self.tiles.pop(bad_data_index)
        self.space_eff.pop(bad_data_index)
        self.production_info.pop(bad_data_index)
        progress_var.set(progress_var.get() + 0.20)

    def extract_images(self, progress_var=None):
        # Find the image information in the HTML.
        image_results = self.driver.find_elements(By.XPATH, "//figure[contains(@class, 'thumb tleft show-info-icon')]")

        images = []

        # Extract the links for each image.
        for result in image_results:
            image = result.find_element(By.CLASS_NAME, 'image')
            images.append(image.get_attribute('href'))

        # Calculate the weight each image download would be on the progress bar. First find the weight in terms of
        # percentage. Then since the range for the value of a progress bar is 0 to 1, dividing the percentage by 100
        # would get the weight in the range of 0 to 1.
        progress_weight = (100 / len(images)) / 100

        # Create a thread pool of worker threads for the image downloads to occur. By using a with statement, this
        # ensures when the threads are no longer needed they are properly shutdown and the resources are released.
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit the image downloading tasks to the worker threads and store the files locally. The submit method
            # returns a Future object that can be used to get the result of the urlretrieve method.
            futures = [executor.submit(
                urllib.request.urlretrieve,
                str(img),
                f"images/layout_images/{self.layout_names[index].split('-')[0]}.jpg") for index, img in
                enumerate(images)]

            # The callback method allows the definition of a function to be called when the Future object is done.
            # The defined function is called with the Future object as its only argument. By using a lambda function,
            # the Future object and information needed to update the progress bar can be passed to the defined function.
            for future in futures:
                future.add_done_callback(
                    lambda future_arg: self.update_progress(future_arg, progress_var, progress_weight))

        # At the point the images are downloaded, all the web scrapping process is completed. The headless browser and
        # the webdriver session need to be ended, so they can be cleared out of the memory. If this isn't done then
        # memory leak errors could occur.
        self.driver.quit()

    def update_progress(self, future, progress_var, progress_weight):
        # The result in the Future object contains the returned tuple of the urlretrieve method which contains the
        # relative path of the image.
        self.image_paths.append(future.result()[0])
        # Increment the progress bar value by the progress weight since downloading of the image is completed.
        progress_var.set(progress_var.get() + progress_weight)

    def create_data_frame(self):
        # Convert all the data list to pandas.Series.
        names_series = pd.Series(self.layout_names, name='Names')
        image_series = pd.Series(self.image_paths, name='Image')
        costs_series = pd.Series(self.costs_info, name='Cost')
        size_series = pd.Series(self.size, name='Size')
        tiles_series = pd.Series(self.tiles, name='Tiles')
        space_eff_series = pd.Series(self.space_eff, name='Space Efficiency')
        production_series = pd.Series(self.production_info, name='Production')

        # Create a DataFrame to store all the data into one object to be written to a file.
        df = pd.DataFrame({
            'Name': names_series,
            'Image': image_series,
            'Cost': costs_series,
            'Size': size_series,
            'Tiles': tiles_series,
            'Space Efficiency': space_eff_series,
            'Production': production_series})

        # Create a comma separated values file to store the data locally. This file will be used to get the requested
        # data to be displayed to the GUI.
        df.to_csv('layout_data.csv', index=False, encoding='utf-8')
