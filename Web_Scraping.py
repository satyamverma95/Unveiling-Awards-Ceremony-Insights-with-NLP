from bs4 import BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from recipes_mapping import Recipe_Mapping
import re

class Web_Scrapper:
    def __init__ (self, site_to_scrape = "https://www.allrecipes.com/cuisine-a-z-6740455"):
        self.url_cuisines = site_to_scrape
        self.table = pd.DataFrame()
        self.recipe_handle = Recipe_Mapping()


    def scrape_website (self, url):
        '''
        This function will establish connection with the website and read all the content of the pages.
        '''

        page_context_manager = urlopen(url)
        self.page_html = BeautifulSoup(page_context_manager, 'html.parser')
        #print(self.page_html)

    def scrape_cuisine(self):

        self.scrape_website(self.url_cuisines)
        self.cuisine_list = self.page_html.find_all("div", {"class":"alphabetical-list__group"})
        #print(self.cuisine_list)

        for div in self.cuisine_list:
            a_tags = div.find_all("a")
            for a_tag in a_tags:
                link = a_tag.get("href")
                #print("Link ",  link, a_tag.contents[-1].strip())
                self.update_dict( a_tag.contents[-1].strip(), link, self.recipe_handle.cuisine_names )

        self.recipe_handle.write_to_file( self.recipe_handle.cuisine_names, "cuisine_links.json")


    def extract_recipies (self):

        for index, cuisines in enumerate(self.recipe_handle.cuisine_names.keys()):
            self.update_dict(cuisines, {}, self.recipe_handle.recipe_dict)
            #print(self.recipe_handle.cuisine_names[cuisines])
            recipies_url = self.recipe_handle.cuisine_names[cuisines]
            self.scrape_website(recipies_url)
            recipe_list = self.page_html.find_all("a", {"id": re.compile("mntl-card-list-items_.*")})
            for a_tag in recipe_list:
                link = a_tag.get("href")
                recipe_name = a_tag.find_all("span", {"class": re.compile("card__title-text")})
                self.update_dict(recipe_name[-1].text, link, self.recipe_handle.recipe_dict[cuisines])
                #print (recipe_name[-1].text, link)

        self.recipe_handle.write_to_file(self.recipe_handle.recipe_dict, "recipe_links.json")


    def scrape_recipes (self, cuisines = '', recipies = ''):

        for index_c, cuisines in enumerate(self.recipe_handle.cuisine_names.keys()):
            #if (index_c==1):
            self.update_dict(cuisines, {}, self.recipe_handle.recipe_details)
            for index_r, recipe in enumerate(self.recipe_handle.recipe_dict[cuisines].keys()):
                self.update_dict(recipe, {}, self.recipe_handle.recipe_details[cuisines])
                self.update_dict("Meta_Info", {}, self.recipe_handle.recipe_details[cuisines][recipe])
                self.update_dict("Directions", {}, self.recipe_handle.recipe_details[cuisines][recipe])
                self.update_dict("Nutrition", {}, self.recipe_handle.recipe_details[cuisines][recipe])
                temporary_ingredients_list = list()

                #if(index_r==1):
                recipe_page_url = self.recipe_handle.recipe_dict[cuisines][recipe]
                print("Scraping ...", recipe_page_url)
                self.scrape_website(recipe_page_url)

                recipe_meta_info = self.page_html.find_all("div", {"class": re.compile("mntl-recipe-details__item")})
                for item in recipe_meta_info:
                    item_label = item.find("div", {"class": re.compile("mntl-recipe-details__label")})
                    item_value = item.find("div", {"class": re.compile("mntl-recipe-details__value")})
                    self.update_dict(item_label.text, item_value.text, self.recipe_handle.recipe_details[cuisines][recipe]["Meta_Info"])

                recipe_ingredients = self.page_html.find_all("li", {"class": re.compile("mntl-structured-ingredients__list-item.*")})
                for ingredients in recipe_ingredients:
                    ingredients_quantity = ingredients.find("span", {"data-ingredient-quantity": "true"})
                    ingredients_unit = ingredients.find("span", {"data-ingredient-unit": "true"})
                    ingredients_name = ingredients.find("span", {"data-ingredient-name": "true"})

                    #print(ingredients_quantity.text, ingredients_unit.text, ingredients_name.text)
                    temporary_ingredients_list.append('__'.join([ingredients_quantity.text, ingredients_unit.text, ingredients_name.text]))

                self.update_dict("Ingredients", temporary_ingredients_list,\
                                 self.recipe_handle.recipe_details[cuisines][recipe])

                directions_steps = self.page_html.find_all("li", {"id": re.compile("mntl-sc-block_2.*")})
                for index_d, steps in enumerate(directions_steps):
                    directions_step_wise = steps.find("p", {"class": "comp mntl-sc-block mntl-sc-block-html"})
                    #print("Directions : {}, {}".format(index_d, directions_step_wise.text))
                    self.update_dict(index_d +1 , directions_step_wise.text,\
                                     self.recipe_handle.recipe_details[cuisines][recipe]["Directions"])

                nutritional_facts = self.page_html.find_all("tr", {"class": re.compile("mntl-nutrition-facts-summary__table-row")})
                for nutrition in nutritional_facts:
                    nutrition_quantity_unit = nutrition.find("td", {"class": "mntl-nutrition-facts-summary__table-cell type--dog-bold"})
                    nutrition_name = nutrition.find("td", {"class": "mntl-nutrition-facts-summary__table-cell type--dog"})
                    if ( (nutrition_quantity_unit) and (nutrition_name) ):
                        #print(nutrition_quantity_unit.text, nutrition_name.text)
                        self.update_dict(nutrition_name.text, nutrition_quantity_unit.text,\
                                     self.recipe_handle.recipe_details[cuisines][recipe]["Nutrition"])

        #print(self.recipe_handle.recipe_details)
        self.recipe_handle.write_to_file(self.recipe_handle.recipe_details, "data/recipe_details_1.json")




    def update_dict (self, key, value, dictionary):

        self.recipe_handle.add_record(key, value, dictionary)

    def parse_cast_crews (self):

        self.print_data(self.cast_and_crew)
        self.write_to_file(self.cast_and_crew, "cast_crew.txt")


    def write_to_file(self, data, filename):

        with open(self.data_directory + filename, "w", encoding='utf-8') as f:
            f.write(str(data))


    def print_data(self, data):
        print(data)
        print("Total Number of Elem ", len(data) )


def main ():

    ws_h = Web_Scrapper()
    ws_h.scrape_cuisine()
    #ws_h.recipe_handle.print_dict()
    ws_h.extract_recipies()

#if __name__ == "__main__":
#    main()