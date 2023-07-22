from Web_Scraping import Web_Scrapper
from recipes_mapping import Recipe_Mapping
from flask import Flask, jsonify, render_template, request
import json


class Recipe_CookBook:
    def __init__ (self, recepie_name = "Panner Butter Masala"):
        self.scrape_cuisine = True
        self.extract_recipe = True

def main():

    rcb_h = Recipe_CookBook()
    rm_h = Recipe_Mapping()
    ws_h = Web_Scrapper()

    if (rcb_h.scrape_cuisine):
        ws_h.scrape_cuisine()
    else:
        rm_h.load_json("cuisine_links.json", 1)
        #print(rm_h.cuisine_names)

    if (rcb_h.extract_recipe):
        ws_h.extract_recipies()
    else:
        rm_h.load_json("recipe_links.json", 2)
        #print(rm_h.recipe_dict)

    ws_h.scrape_recipes()


if __name__ == "__main__":
    main()