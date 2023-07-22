import json
from transformers import pipeline, DistilBertTokenizer, TFDistilBertForQuestionAnswering
import tensorflow as tf
from nltk import word_tokenize
from nltk.corpus import wordnet
from nltk import pos_tag
from nltk import bigrams
from nltk.util import ngrams
import re
from unicodedata import numeric
from kitchen_thesaurus import Tools, Primary_Cooking_Methods, Secondary_Cooking_Methods, Utensils_synonyms,\
    Temp_synonyms, Time_synonyms, Ingredients_synonyms, All_Food, Units


class Query_Resolver:
    def __init__(self):
        self.recipe_details = dict()
        self.recipe_details_file = "data/recipe_details_1.json"
        self.cuisine = ''
        self.recipe = ''
        self.servings_required = 1
        self.stopwords = ["ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"]

    def read_json(self):
        self.recipe_details = json.load(open(self.recipe_details_file))

    def print_json(self, data):
        print(data)

    def set_cuisine_and_recipe(self, cuisine, recipe, servings):
        self.cuisine    =   cuisine
        self.recipe     =   recipe
        self.servings_required   =   servings

    def qna_model(self, query, step_no ):
        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-cased-distilled-squad")
        model = TFDistilBertForQuestionAnswering.from_pretrained("distilbert-base-cased-distilled-squad")

        context = self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step_no)]

        inputs = tokenizer(query, context, return_tensors="tf")
        outputs = model(**inputs)

        answer_start_index = int(tf.math.argmax(outputs.start_logits, axis=-1)[0])
        answer_end_index = int(tf.math.argmax(outputs.end_logits, axis=-1)[0])

        predict_answer_tokens = inputs.input_ids[0, answer_start_index: answer_end_index + 1]
        answer = tokenizer.decode(predict_answer_tokens)

        #qa_model = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')

        #user_query = query
        #answer = qa_model(question=user_query, context=context)

        return answer

    def convert_to_lower(self, line):
        return (line.lower())

    def remove_punctuation(self, line):
        return (re.sub(r'[^\w \s]', '', line))


    def parse_question(self, question):
        question_l = self.convert_to_lower(question)
        question_p = self.remove_punctuation(question_l)
        question_p_word_tokens = word_tokenize(question_p)
        filtered_question_p = ' '.join([w for w in question_p_word_tokens if not w.lower() in self.stopwords])

        print(filtered_question_p)

        return filtered_question_p

    def find_synonyms(self, word):
        words = wordnet.synsets(word)
        synonyms = [lemma.name() for word in words for lemma in word.lemmas() ]
        return (synonyms)


    def question_interpreter (self, question, step):

        #General Preprocessing
        total_no_dirs = len(self.recipe_details[self.cuisine][self.recipe]["Directions"].keys())
        question_found = False

        if ( ( step >= 1) and (step <= total_no_dirs) ):
            context = self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step)]
            

            ##handling Next step question
            synonyms = self.find_synonyms("next")
            regex_next = ".*(" + "|".join(synonyms) + ").*"
            if (re.match(regex_next, question) ) :
                question_found = True
                print("it is about next question")
                if (step < total_no_dirs):
                    return (self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step+1)])
                else:
                    return ("No More Steps, Enjoy The Dish.")

            ##Handling Prev step question.
            synonyms = self.find_synonyms("previous")
            regex_prev = ".*(" + "|".join(synonyms) + ").*"

            if (re.match(regex_prev, question) ) :
                question_found = True
                print("it is about previous question")
                if (step > 1 ):
                    return (self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step-1)])
                else:
                    return ("You Are Already At Ahe Beginning.")


            ##Handling questions that revolve around cooking actions
            synonyms = self.find_synonyms("perform")
            regex_actions = ".*(" + "|".join(synonyms) + ").*"
            if (re.match(regex_actions, question)):
                question_found = True
                #context = self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step - 1)]
                text = word_tokenize(context)
                pos_tagged = pos_tag(text)
                verbs_and_pos = list(filter(lambda x: re.match("V.*", x[1]), pos_tagged))
                #verbs = list(map(lambda x :x[0], verbs_and_pos))
                #print(verbs_and_pos)
                cooking_methods = Primary_Cooking_Methods + Secondary_Cooking_Methods
                verbs = [v[0] for v in verbs_and_pos if v[0].lower() in cooking_methods ]
                print(verbs)
                return (",".join(verbs))

            ##Handling questions that revolve around cooking utensils
            synonyms = self.find_synonyms("utensils")
            synonyms.extend(Utensils_synonyms)
            regex_actions = ".*(" + "|".join(synonyms) + ").*"
            #print(regex_actions)
            if (re.match(regex_actions, question)):
                question_found = True
                #context = self.recipe_details[self.cuisine][self.recipe]["Directions"][str(step - 1)]
                text = word_tokenize(context)
                pos_tagged = pos_tag(text)
                noun_and_pos = list(filter(lambda x: re.match("N.*", x[1]), pos_tagged))
                #noun = list(map(lambda x: x[0], noun_and_pos))
                noun = [n[0] for n in noun_and_pos if n[0].lower() in Tools]
                print(noun)
                return (",".join(noun))

            ##Handling questions that revolve around Ingredients
            synonyms = self.find_synonyms("ingredients")
            synonyms.extend(Ingredients_synonyms)
            synonyms.extend(Units)
            regex_ingredients = ".*(" + "|".join(synonyms) + ").*"
            #print(regex_ingredients)

            if (re.match(regex_ingredients, question)):
                question_found = True
                print("Ingredients Question")
                text = word_tokenize(question)
                pos_tagged = pos_tag(text)
                
                ingredients_list = self.recipe_details[self.cuisine][self.recipe]["Ingredients"]
                nouns_and_pos = list(filter(lambda x: re.match("N.*", x[1]) or re.match("JJ", x[1]), pos_tagged))
                ingredients_nouns = list(set([n[0] for n in nouns_and_pos for ingredient in ingredients_list if n[0].lower() in ingredient]))
                ingredients_bigram = [' '.join(b) for b in bigrams(text)]
                ingredients_bigram = list(set([n for n in ingredients_bigram for ingredient in ingredients_list if n.lower() in ingredient]))
                ingredients_nouns.extend(ingredients_bigram)
                ingredients_trigram = [' '.join(b) for b in ngrams(text, 3)]
                ingredients_trigram = list(set([n for n in ingredients_trigram for ingredient in ingredients_list if n.lower() in ingredient]))
                ingredients_nouns.extend(ingredients_trigram)
                print(ingredients_nouns)

                required_ingredients = self.process_ingredients(ingredients_nouns)
                return(required_ingredients)


            ##Handling questions that revolve around Time
            synonyms_time = self.find_synonyms("time")
            synonyms_time.extend(Time_synonyms)
            regex_time = ".*(" + "|".join(synonyms_time) + ").*"

            synonyms_total = self.find_synonyms("total")
            regex_total = ".*(" + "|".join(synonyms_total) + ").*"


            if (re.match(regex_time, question) and re.match(regex_total, question)):
                question_found = True
                print("Total Time Question")
                total_time = self.recipe_details[self.cuisine][self.recipe]["Meta_Info"]["Total Time:"]
                print(total_time)
                return (total_time)

            elif (re.match(regex_time, question)):
                question_found = True
                print("Time Question")
                time_regex = "\b(\d.*(minutes|mins|min|minute|hour|hours|hrs|hr){1})\b"
                text = word_tokenize(context)
                bigram = list(bigrams(text))
                time_units = [' '.join(b) for b in list(filter(lambda x: re.match("\d.*", x[0]) and re.match(".*(minutes|mins|min|minute).*", x[1]), bigram))]
                print(time_units)
                directions_senteces = context.split('.')
                answer = [ sentence for sentence in directions_senteces if time_units[0] in sentence ]

                if (answer):
                    return (answer.pop())
                else:
                    return ("Nothing Useful found at the moment")


            ##Handling questions that revolve around Temperature
            synonyms = self.find_synonyms("temperature")
            synonyms.extend(Temp_synonyms)
            regex_temperature = ".*(" + "|".join(synonyms) + ").*"
            #print(regex_temperature)

            if (re.match(regex_temperature, question)):
                question_found = True
                print("Temperature Question")
                return("")

            ##If you reached here then none of the above segreggation matched, Let go to q&a model.
            if (not question_found):
                answer = self.qna_model(question, step)
                return answer
       
    def process_ingredients(self, itemList):

        ingredients_list = self.recipe_details[self.cuisine][self.recipe]["Ingredients"]
        extracted_ingredients = [ingredient for item in itemList for ingredient in ingredients_list if item in ingredient]
        extracted_ingredients = list(set(extracted_ingredients))
        extracted_ingredients = self.scale_ingredients(extracted_ingredients)
        print("Scales Ingredients received",extracted_ingredients )
        required_ingredients  = ",  ".join(extracted_ingredients)

        return (required_ingredients)
        ##print(required_ingredients)

    def scale_ingredients(self, extracted_ingredients):

        for ingredients in extracted_ingredients:
            print("ingredients", ingredients)
            ingredients_components = ingredients.split("__")
            print("ingredients_components ", ingredients_components)
            
            if (ingredients_components[0]):
                if (len(ingredients_components[0]) > 1 ):
                    ingredients_components[0] = str(numeric(ingredients_components[0][0]) + numeric(ingredients_components[0][-1]))
                else:    
                    ingredients_components[0] = str(numeric(ingredients_components[0]))

                ingredients_components[0] = str(round((float(ingredients_components[0])/float(self.recipe_details[self.cuisine][self.recipe]["Meta_Info"]["Servings:"]))*float(self.servings_required),3) )

        return ([" ".join(ingredients_components)])


    def get_query(self):
        direction_step = int(input("Which step you want to explore?"))
        query = input("What is your Question?")
        return direction_step, query.strip()


def main():
    qr_h = Query_Resolver()
    qr_h.read_json()
    qr_h.print_json(qr_h.recipe_details)
    step_no, query = qr_h.get_query()
    parsed_query = qr_h.parse_question(query)
    qr_h.question_interpreter(parsed_query, step_no, 4)
    #answer = qr_h.qna_model(step_no,query)
    #print("Query Asked : ", query, end='\n')
    #print("Answer:", answer)


if __name__ == "__main__":
    main()
