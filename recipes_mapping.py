import os
import json

class Recipe_Mapping:
    def __init__ ( self ):
        self.cuisine_names = dict()
        self.recipe_dict = dict()
        self.recipe_details = dict()
        self.cwd = os.getcwd()

    def add_record(self, key, value, dictionary):

        if ( key not in dictionary):
            dictionary[ key ] = value

    def delete_record (self, key, value, dictionary):

        if ( key in dictionary):
           del dictionary[ key ]

    def print_dict (self, dictionary) :
        print (dictionary)

    def write_to_file(self, data, filename):

        with open( self.cwd + '/' + filename, "w", encoding='utf-8') as f:
            data = json.dumps(data)
            f.write(str(data))

    def load_json (self, filename, type):

        f_h = open(filename)

        if (type == 1):
            self.cuisine_names = json.load(f_h)
        elif(type == 2):
            self.recipe_dict = json.load(f_h)

