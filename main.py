import requests
import json
import random
import re
import os

def load_data():
    try:
        with open("data.json", "r") as f:
            words = json.load(f)
            return words

    except FileNotFoundError:
        return {}

    except json.decoder.JSONDecodeError:
        print("ERROR: 'data.json' is corrupted.")
        
        # Backup the corrupted file
        os.rename("data.json", "data_backup.json")
        print("Corrupted file backed up as 'data_backup.json'.")

        # Try to load the last valid backup
        if os.path.exists("data_backup.json"):
            try:
                with open("data_backup.json", "r") as backup_file:
                    backup_data = json.load(backup_file)

                # Restore backup
                with open("data.json", "w") as new_file:
                    json.dump(backup_data, new_file, indent=4)

                print("Restored 'data.json' from last known good backup.")
                return backup_data

            except Exception as e:
                print("Failed to restore from backup:", e)
                return None
        else:
            print("No backup found. Please fix 'data.json' manually.")
            return None



def fetch_meaning(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        data = response.json()

        if isinstance(data, list) and "meanings" in data[0]:
        # Extract first 3 meanings
            meanings = [entry['definition'] for meaning in data[0]['meanings']
            for entry in meaning['definitions']] 
        return meanings[:3]

    except:
        return []
    
def save_to_json(word, meanings):

    data = load_data()
    if word not in data:
        data[word] = meanings
        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)

def underline_valid_word(sentence, word):
    return re.sub(rf'\b{word}\b', f'\033[4m{word}\033[0m', sentence, flags= re.IGNORECASE)

# def extract_random_word(sentence):

#     words = re.findall(r'\b[a-zA-Z]{2,}\b', sentence)
#     if words:
#         return random.choice(words)
#     else:
#         None

def word_in_data(sentence):
    return [word.lower() for word in re.findall(r'\b\w+\b', sentence) if len(word) > 1]

repeated_sentence = set()

def start(sentence):
    
    data = load_data()
    if data is None:
        print("Fix 'data.json' before continuing.")
        return

    word_ = word_in_data(sentence)

    matched_key = None
    
    if sentence not in repeated_sentence:
        repeated_sentence.add(sentence)

        for key in data:

            if re.search(rf'\b{key}\b', sentence, re.IGNORECASE):
                matched_key = key
                break
         
        if matched_key:

            underlined = underline_valid_word(sentence, matched_key)
            meaning = random.choice(data[matched_key])
            print()
            print(underlined)
            print(f"{matched_key} :", meaning)
            print()
            return

        if not word_:
            print(f"No valid word in sentence.")
            return

        random_word = random.choice(word_)
        print()
        # print(f"No known word found. Picking a random word: '{random_word}'")
        print("Fetching meaning from web...")
        print()

        meanings = fetch_meaning(random_word)

        if meanings:
            data[random_word] = meanings
            save_to_json(random_word, meanings)
            print("New word added to the data.")
            print()
            
            meaning = random.choice(meanings)
            underlined = underline_valid_word(sentence, random_word)
            print(underlined)
            print(f"{random_word} :", meaning)
            print()

        else:
            print(f"Could not fetch meaning for random word '{random_word}'.")

    else:
        if not word_:
            print("No valid word found.")
            return

        random_word = random.choice(word_)
        if random_word in data:
            underlined = underline_valid_word(sentence, random_word)
            meaning = random.choice(data[random_word])
            # print("Random word exists in data.")
            print("Sentence:", underlined)
            print(f"{random_word} :", meaning)
        else:
            meanings = fetch_meaning(random_word)
            if meanings:
                data[random_word] = meanings
                save_to_json(random_word, meanings)
                underlined = underline_valid_word(sentence, random_word)
                meaning = random.choice(meanings)
                print("New word added to the data.")
                print("Sentence:", underlined)
                print(f"{random_word} :", meaning)
            else:
                if not meanings:
                    print(f"Could not fetch meaning for '{random_word}' (empty response).")
                else:
                    print(meanings[0])

if __name__ == "__main__":
    while True:
        sentence = input("\nEnter a sentence: ")
        if sentence.lower() == "exit":
            print("Goodbye!")
            exit()
        start(sentence)
        



