from utils import *

import re
import random

list_preparationForTheNextQuestion_g = [
"Merci pour ces complements !",
"Merci de partager tout ca avoir moi!",
"Merci !",
"Ok je vois... Pour aller plus loin :",
"Super !",
"Hmm... ok ! Je crois que ça m'aide a y voir plus clair !",
"Ah oui ? Top !",
"Merci pour ces explications."]

def main():
    print("Hello ! Je suis spécialiste en lancement de projet ! Tu peux me décrire ta dernière idée de projet ?")
    print("Type 'exit' to quit the program.\n")
    
    while True:
        # Step 1: Wait for the user's response
        user_response = input("> ")
        
        # Step 2: Check if the user wants to exit
        if user_response.lower() == "exit":
            print("Goodbye! Have a great day!")
            break
        
        # call Mistral API and get answer
        response_l, total_note_l = get_bot_response(user_response)
        
        # print output
        print("Evaluation: "+total_note_l+"/100")
        print(response_l)
        ## Step 3: Parse the response to check for the tag <##note_totale##>
        #match = re.search(r"<##note_totale##>\s*(\d+)", response_l)
        #
        ## Step 4: Determine the output message
        #total_note = 0
        #if match:
        #    total_note = match.group(1)  # Extract the number after the tag
        #    print(f"For now, you achieve the mark of: {total_note}")
        #else:
        #    print("I couldn't find your total note. Please include it with the tag <##note_totale##>.")
        #
        #questions = re.findall(r"<\*\*question\*\*>(.*?)(?=<|\n|$)", response_l)
        #if questions:
        #    question_list = [question.strip() for question in questions]
        #    random_question = random.choice(question_list)
        #    radom_prep = random.choice(list_preparationForTheNextQuestion_g)
        #    followup = radom_prep + "\n" + random_question
        #    print(followup)
        #elif not total_note and not questions:
        #    print("I couldn't find a valid tag. Please include <##note_totale##> or <**question**> in your response.")

# Entry point of the script
if __name__ == "__main__":
    main()