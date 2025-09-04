import requests
from dotenv import load_dotenv
import os

print("\n\n\tWelcome to the Random Generator!!!\n\n")
load_dotenv()
api_key=os.getenv("API_KEY")

def fetch_quote():
    url = "https://api.api-ninjas.com/v1/quotes"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error Fetching: ', response.status_code, response.text)
        
def fetch_dad_joke():
    url = "https://api.api-ninjas.com/v1/dadjokes"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_jokes():
    url = "https://api.api-ninjas.com/v1/jokes"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_animal_facts(query):
    url = "https://api.api-ninjas.com/v1/animals?name={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_advice():
    url = "https://api.api-ninjas.com/v1/advice"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)

def fetch_facts():
    url = "https://api.api-ninjas.com/v1/facts"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)

def fetch_trivia():
    url = "https://api.api-ninjas.com/v1/trivia"
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_spell_check(query):
    url = "https://api.api-ninjas.com/v1/spellcheck?text={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_dictionary(query):
    url = "https://api.api-ninjas.com/v1/dictionary?word={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_hobbies(query):
    url = "https://api.api-ninjas.com/v1/hobbies?category={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_exercises(group, detail):
    url = "https://api.api-ninjas.com/v1/exercises?{}={}".format(group, detail)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)

def fetch_nutrition(query):
    url = "https://api.api-ninjas.com/v1/nutrition?query={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_IP_address(query):
    url = "https://api.api-ninjas.com/v1/iplookup?address={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)

def fetch_DNS(query):
    url = "https://api.api-ninjas.com/v1/dnslookup?domain={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def fetch_password(query):
    url = "https://api.api-ninjas.com/v1/passwordgenerator?length={}".format(query)
    response = requests.get(url, headers = {'X-Api-Key':api_key})
    if response.status_code == requests.codes.ok:
        data = response.json()
        return data
    else:
        print('Error fetching: ', response.status_code, response.text)
        
def logic(thing):
    if thing == 1:
        response = fetch_quote()
        author = response[0]['author']
        quote = response[0]['quote']
        print("\nAuthor:", author, "\n")
        print("Quote:", quote, "\n")
    elif thing == 2:
        response = fetch_dad_joke()
        joke = response[0]['joke']
        print("\nDad Joke:", joke, "\n")
    elif thing == 3:
        response = fetch_jokes()
        joke = response[0]['joke']
        print("\nJoke:", joke, "\n")
    elif thing == 4:
        animal = str(input("\nWhat animal would you like a fact about? "))
        response = fetch_animal_facts(animal)
        for name in response:
            print("\nName:", name['name'])
            print("Scientific Name:", name['taxonomy'].get('scientific_name', 'N/A'))
            print("Locations:")
            for location in name.get('locations', 'N/A'):
                print(location)
            print("Prey:", name['characteristics'].get('prey', 'N/A'))
            print("Biggest Threat:", name['characteristics'].get('biggest_threat', 'N/A'))
            print("Most Distinctive Feature:", name['characteristics'].get('most_distinctive_feature', 'N/A'))
            print("Litter Size:", name['characteristics'].get('litter_size', 'N/A'))
            print("Habitat:", name['characteristics'].get('habitat', 'N/A'))
            print("Top Speed:", name['characteristics'].get('top_speed', 'N/A'))
            print("Lifespan:", name['characteristics'].get('lifespan', 'N/A'))
            print("Weight:", name['characteristics'].get('weight', 'N/A'))
            print("Estimated Population Size:", name['characteristics'].get('estimated_population_size', 'N/A'), "\n")
    elif thing == 5:
        response = fetch_advice()
        advice = response['advice']
        print("\nAdvice:", advice, "\n")
    elif thing == 6:
        response = fetch_facts()
        facts = response[0]['fact']
        print("\nFact:", facts, "\n")
    elif thing == 7:
        response = fetch_trivia()
        print("\nCategory:", response[0]['category'], "\n")
        print("Question:", response[0]['question'], "\n")
        user = input("Please type your answer: ").upper()
        answer = (response[0]['answer']).upper()
        i = 1
        while i < 3:
            if user == answer:
                print("Congratulations, you answered correctly")
                break
            else:
                user = input("Sorry that is incorrect, please enter another guess: ").upper()
                i += 1
            if i == 3:
                print("The correct answer was:", (response[0]['answer']).capitalize())
                break
    elif thing == 8:
        word = str(input("\nWhat word would you like to spell check? "))
        response = fetch_spell_check(word)
        correct = response['corrected']
        print("Correct Spelling:", correct, "\n")
    elif thing == 9:
        word = str(input("\nWhat word would you like to lookup in the dictionary? "))
        response = fetch_dictionary(word)
        definition = response['definition']
        print("Definition:", definition, "\n")
    elif thing == 10:
        print("""\nYou can select from the following options for categories (must be typed how you see them):
general,
sports_and_outdoors,
education,
collection,
competition,
observation
                """)
        category = str(input("Please enter exactly which category you would like: "))
        response = fetch_hobbies(category)
        hobby = response['hobby']
        link = response['link']
        print("Hobby:", hobby, "\n")
        print("Link to Hobby:", link, "\n")
    elif thing == 11:
        print("""\nFor exercise you can pick anything in this list, within each grouping:
Name:
    Name/Type of exercise.
Type:
    Exercise Type. Possible values are:
        Cardio
        Olympic Weightlifting
        Plyometrics
        Powerlifting
        Strength
        Stretching
        Strongman
Muscle:
    Muscle group targeted by the exercise. Possible values are:
        Abdominals
        Abductors
        Adductors
        Biceps
        Calves
        Chest
        Forearms
        Glutes
        Hamstrings
        Lats
        Lower Back
        Middle Back
        Neck
        Quadriceps
        Traps
        Triceps
Difficulty:
    Difficulty level of the exercise. Possible values are:
        Beginner
        Intermediate
        Expert""")
        type = ["cardio", "olympic_weightlifting", "plyometrics", "powerlifting", "strength", "stretching", "strongman"]
        muscle = ["abdominals", "abductors", "adductors", "biceps", "calves", "chest", "forearms", "glutes", "hamstrings", "lats", "lower_back", "middle_back", "neck", "quadriceps", "traps", "triceps"]
        difficulty = ["beginner", "intermediate", "expert"]
        detail = str(input("Please type exactly which value you want: ")).lower().replace(" ", "_")
        
        if detail in type:
            group = "type"
        elif detail in muscle:
            group = "muscle"
        elif detail in difficulty:
            group = "difficulty"
        else:
            group = detail
        
        response = fetch_exercises(group, detail)
        for name in response:
            print("\nName:", name['name'])
            print("Type:", name['type'])
            print("Muscle:", name['muscle'])
            print("Equipment:", name['equipment'])
            print("Difficulty:", name['difficulty'])
            print("Instructions:", name['instructions'], "\n")
    elif thing == 12:
        food = str(input("\nPlease enter any sort of food for nutrition information: "))
        response = fetch_nutrition(food)
        for name in response:
            print("Name:", name['name'])
            print("Fat Total (grams):", name['fat_total_g'])
            print("Fat Saturated (grams):", name['fat_saturated_g'])
            print("Sodium (milligrams):", name['sodium_mg'])
            print("Potassium (milligrams):", name['potassium_mg'])
            print("Cholesterol (milligram):", name['cholesterol_mg'])
            print("Carbs Total:", name['carbohydrates_total_g'])
            print("Fiber (grams):", name['fiber_g'])
            print("Sugar (grams)", name['sugar_g'], "\n")
    elif thing == 13:
        ip = str(input("\nPlease enter IP address either in IPv4 or IPv6: "))
        response = fetch_IP_address(ip)
        print("Valid?", response['is_valid'])
        print("Country:", response['country'])
        print("Region:", response['region'])
        print("Timezone:", response['timezone'])
        print("ISP:", response['isp'])
        print("Address:", response['address'])
    elif thing == 14:
        dns = str(input("\nPlease enter any DNS domain (ex: example.com): "))
        response = fetch_DNS(dns)
        for name in response:
            if name['record_type'] in ["A", "AAAA", "CNAME", "MX", "NS", "PTR", "SRV", "TXT", "CAA"]:
                print("Record Type:", name['record_type'])
                print("Value:", name['value'], "\n")
            else:
                print("Record Type:", name['record_type'])
                print("Mname:", name['mname'])
                print("Rname:", name['rname'])
    else:
        length = int(input("\nPlease enter the number of characters (length) you would like the password to be: "))
        response = fetch_password(length)
        print("\nPassword:", response['random_password'], "\n")


def main():
    
    print("""
Please type the number from the following options: \n\n
    1. Random Quote
    2. Dad Jokes
    3. Jokes
    4. Animal Facts
    5. Advice
    6. Facts
    7. Trivia
    8. Spell Check
    9. Dictionary
    10. Hobbies
    11. Exercises
    12. Nutrition Information
    13. IP Address Lookup
    14. DNS Lookup
    15. Password Generator
                       \n""")
    try:
        number = int(input("Enter Number: "))
    except:
        number = int(input("Please enter one of the 15 numbers this time: "))

    logic(number)
    
    while True: # maybe do while True
        question = str(input("Would you like to select another option (y/n)? "))
        if question == "y":
            again = int(input("If you would like to run a different option, please enter the number: "))
            logic(again)
        else:
            quit()


if __name__ == "__main__":
    main()