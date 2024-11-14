from mistralai import Mistral
import time
import re
import random

# Mistral init
#api_key = os.environ["MISTRAL_AI_KEY"]
model = "mistral-large-latest"
#model = "mistral-small-latest"
#model = "open-mistral-nemo"    # open-source
#client = Mistral(api_key=api_key)
client = Mistral(api_key="MJ0ZB2X5IiJd7LslJOl74kwivn0U98QI")

# List to store the conversation history
conversation_history = []


# Replace `client.chat.complete` call with throttled function
last_request_time = 0  # Store the last request time globally

# Management of the rate of API calls (1 request per second max)
def throttled_chat_complete(client, **kwargs):
    global last_request_time
    rate_limit_interval = 1.1  # Interval in seconds between requests (adjust as needed)
    
    now = time.time()
    if now - last_request_time < rate_limit_interval:
        time.sleep(rate_limit_interval - (now - last_request_time))
    last_request_time = time.time()

    # Make the API call
    return client.chat.complete(**kwargs)


prompt_prep_1 = """Je vais te donner un document type decrivant un projet ci-dessous.
J'aimerais que tu utilises ce document en tant qu'exemple de trame de document descriptif projet. Quand je te demanderai de consolider les idees de chaque projet dans
un document, j'aimerais que tu le construises avec cette meme trame, section par section.

Document projet exemple :
Projet : Lumis Un nouvel outil pour le design du reseau de transport
Auteur : Florian Burp Date : 25/10/2024
Equipe : EU Network Planning

Executive Summary

L'objectif du projet est de construire un outil de simulation d'impacts de changements dans la configuration du reseau de Transport Amazon sur le reseau Europeen. Aujourd'hui, nous n'avons que deux methodes pour simuler les consequences de changements a venir dans la configuration du reseau : l'environnement ATROPS et des calculs ad-hoc sous Excel. Ces deux approches presentent des desavantages importants : 8 heures pour une simulation de 150k colis avec ATROPS et un nombre limite de colis que l'on peut simuler avec la simulation ATROPS (500k) qui ne permet d'estimer des impacts que sur une semaine maximum, ou un manque de process qui ralentit la construction de scenario sous Excel et rend difficile l'explication de la methodologie de chaque modele. Il est egalement difficile d'estimer une erreur de prevision ou d'avoir suffisamment de granularite dans la simulation avec les modeles construits en ad-hoc sous Excel.
Lumis est une nouvelle approche de simulation codee en python et reproduisant le mode de fonctionnement de l'affectation des colis aux entrepots et transporteurs en place chez Amazon. Les avantages de l'outil sont :

Simulation 1500 fois plus rapide qu'avec l'environnement ATROPS (20 secondes versus 8h);
Aucune limitation du nombre de colis simules ce qui permet d'estimer les impacts de changement sur plusieurs mois;
Plus de granularite dans les resultats des simulations (codes postaux des clients, tailles et poids des colis)
Les gains potentiels estimes en utilisant cette approche sont de l'ordre de 30M€ par an d'opportunites identifiees et activees sur le reseau Europeen. Les investissements necessaires pour finir le developpement de Lumis et le deployer en 2025 sont de 850k€. Il n'y a pas d'autres projets de ce type en cours ou en lancement a ce jour. En cas de validation du budget, le projet pourra demarrer des Novembre 2024 et les premiers gains pourront etre observes des le deuxieme trimestre 2025. Un risque potentiel identifie pour la reussite du projet est la disponibilite des equipes Transport en France et en Italie, risque que l'on mitige par l'engagement recu par les Directeurs Transport de ces deux regions d'accorder 2 jours par semaines a minima pour 2 personnes de leurs equipes pour l'usage de Lumis a partir du premier trimestre 2025.
Cas d'usages
Lumis sera utile tout au long de l'annee pour anticiper et planifier tous les evenements qui ont un impact sur le reseau de transport : gestion des jours feries, grands evenements comme Prime Day ou Peak a la fin de l'annee, problemes lies aux operations (inondations, greves d'un ou plusieurs entrepots, problemes recurrents sur des axes routiers), negociation de capacites avec les transporteurs ou integration d'un nouveau transporteur. Il sera utile egalement dans toutes les negociations commerciales avec les transporteurs (negociations tarifaires, identification d'opportunites d'injections directes dans le reseau des transporteurs last mile) ainsi que dans le design de notre reseau middle mile.

Utilisateurs / Clients
Les utilisateurs de Lumis sont les responsables transport ou les responsable "Network Design". Une fois l'outil deploye, une plateforme sera mise en place pour que ces deux populations puissent soumettre des propositions de simulation a l'equipe "Network Planning". Un data analyst de l'equipe sera mandate pour travailler avec chaque demandeur a la calibration de la simulation et lancera les differentes iterations necessaires afin d'evaluer l'impact des changements proposes. Une fois le meilleur scenario identifie, le demandeur sera en charge de deployer les changements, le data analyst s'assurera de mesurer les impacts effectifs des changements et calculera l'erreur versus la simulation. Enfin, le demandeur et le data analyst seront en charge de faire un bilan au plus tard 2 mois apres la mise en place pour communiquer sur les gains realises.

Defis potentiels et solutions
Aucun probleme technique identifie pour finaliser l'implementation de Lumis mais il s'agira de rester vigilant. Pour cela un comite de surveillance a ete designe et un point mensuel est mis en place pour presenter l'avancement par rapport a la roadmap et resoudre les potentiels problemes techniques ou d'acces aux donnees.
Un probleme potentiel a ete identifie par rapport au manque de disponibilite des equipes Transport, tres demandees par les sujets operationnels et qui ont peu de temps pour faire evoluer leurs modes de fonctionnement, notamment pour la France et l'Italie. Pour gerer ce risque nous avons convenu avec les Directeurs Transport France et Italie qu'ils liberent 2 responsables transport pendant 2 jours par semaine pour se consacrer entierement aux sujets de simulation a partir de Janvier 2025.

Equipe projet
L'equipe est deja composee de 2 data scientists (Youssef et Simon) ainsi que du manager des equipes "Network Planning and Analytics EU" (Florian). Si la validation projet est prononcee alors nous recruterons un 3eme data scientist afin de faire la transition avec Florian.

Roadmap
En cas de validation suite a notre reunion, les developpements de Lumis continueront des le debut de Novembre 2024. Le calendrier ensuite sera le suivant :

Fin Decembre 2024 : Lumis V2 finalisee et testee en mode "challenger" sur Peak Day
T1 2025 : 3 cas d'usages (France, Italie et Allemagne) traites pour fine tuning
T2 2025 : code finalise et 6 cas d'usage supplementaires pris par les equipes dans les autres geographies.
Juin 2025 : presentation des resultats au comite projet et generalisation de l'approche sur le deuxieme semestre 2025.

Budget previsionnel et ROI
Le budget previsionnel estime est de 450k€ pour les equipes "Network Planning" : 3 data scientists pendant 6 mois representant 300k€, puis 3 data analysts pendant 6 mois representant 200k€.
En ce qui concerne les equipes transports, nous planifions un besoin moyen de ressources de 2 responsables transport, 2 jours par semaine, tout au long de l'annee, pour chacune des 5 marketplaces. Cela represente 400k€ pour 2025.
En ce qui concerne les equipes Network Design, pas de besoins additionnels, Lumis ne sera qu'un outil facilitant le travail deja realise.
Les gains attendus estimes et actives en 2025 avec les responsables transport sont de : 20M€ (5M€ opportunites d'injection directe en France, 10M€ negociation de contrat en Allemagne, 5M€ changements de design et tarification dans les 5 marketplaces). Les gains estimes et actives avec les equipes "Network Design" sont de 10M€ (optimisation du plan de tris et du middle mile au depart des 3 nouveaux entrepots).
Le retour sur investissement estime en 2025 (annee 1) est donc de : 29,1M€ (30M€ - 900k€).
Le retour sur investissement estime les annees suivantes est de : 35M€ (2026), 40M€ (2027)"""

prompt_prep_2 = """Voici ci-dessous un systeme de notation en 8 sections pour evaluer une idee de projet, j'aimerais que tu l'utilises pour evaluer les idees de projets que je vais te donner.
Systeme de notation, section par section :

1-Resume executif (20 points), contenant :
- Présence d'un résumé synthétique et clair des objectifs et enjeux du projet (vaut pour 10 points)
- Clarté et précision dans la description des défis actuels et de la valeur ajoutée proposée (vaut pour 10 points)

2-Objectifs et bénéfices (20 points), contenant :
- Identification précise des bénéfices quantitatifs (par ex., gains financiers) (vaut pour 10 points)
- Explication claire de l'impact sur les processus existants et des bénéfices pour les parties prenantes (vaut pour 10 points)

3-Cas d'usage (15 points), contenant :
- Exemples concrets et pertinents des cas d’utilisation, démontrant l'applicabilité du projet dans diverses situations (vaut pour 15 points)

4-Budget et retour sur investissement (15 points), contenant :
- Détails des coûts estimés et d'un retour sur investissement attendu (vaut pour 15 points).

5-Utilisateurs et clients cibles (10 points), contenant :
- Identification des utilisateurs et des équipes impliquées, avec description de leurs rôles respectifs (vaut pour 10 points)

6-Équipe projet et gouvernance (10 points), contenant :
- Présence d'une structure d'équipe et d'un processus de gouvernance clair pour le suivi de projet (vaut pour 10 points)

7-Planification et roadmap (5 points), contenant :
- Description d'un calendrier clair avec des étapes concrètes, incluant des jalons pour le suivi (vaut pour 5 points)

8-Risques et solutions (5 points), contenant :
- Identification des risques potentiels, accompagnée de stratégies de mitigation (vaut pour 5 points)

Dans chaque element, mets la note de 0 point si jamais tu n'as aucune information, la moitie des points si cela repond partiellement a l'attente, et la note maximum si jamais
cela repond pleinement a l'attente. Note de maniere severe : si jamais il n'y a pas d'information sur une partie alors ca vaut 0.
Enfin, l'evaluation totale, ou note totale, est la somme des notes de chaque partie."""

prompt_prep_3 = """Quand je te donne une description de projet, peux-tu appliquer le systeme de notation que je t'ai decrit pour affecter une note a chaque partie ?
Je te rappelle que si tu n'as aucune information pour repondre a une section du systeme de notation alors cela vaut 0 points (il n'y a pas de note minimale par section).
Utilise des balises <##note_NomDeLaSection##> avant d'indiquer la note de chacune des sections. Exemple <##note_Resume_executif##>5.
Enfin, calcule la note totale comme somme des notes de chaque section, et indique la avec la balise <##note_totale##>. Exemple : <##note_totale##>30.
Et finalement, en dernière partie de ta réponse, peux-tu poser 3 questions afin d'ameliorer la note sur les sections qui en ont le plus besoin, en les classant en fonction des points que cela rapporterait ?
Utilise une balise egalement <##question##> avant de poser chaque question. Exemple: <##question##>Peux-tu m'en dire plus sur les gains potentiels que ton projet permettrait d'obtenir ?"""

prompt_reshaped = """Consignes pour l'évaluation des idées de projets :

Système de notation :

1-Résumé exécutif (20 points) :
Présence d'un résumé synthétique et clair des objectifs et enjeux du projet (vaut pour 10 points)
Clarté et précision dans la description des défis actuels et de la valeur ajoutée proposée (vaut pour 10 points)
2-Objectifs et bénéfices (20 points) :
Identification précise des bénéfices quantitatifs (par ex., gains financiers) (vaut pour 10 points)
Explication claire de l'impact sur les processus existants et des bénéfices pour les parties prenantes (vaut pour 10 points)
3-Cas d'usage (15 points) :
Exemples concrets et pertinents des cas d’utilisation, démontrant l'applicabilité du projet dans diverses situations (vaut pour 15 points)
4-Budget et retour sur investissement (15 points) :
Détails des coûts estimés et d'un retour sur investissement attendu (vaut pour 15 points)
5-Utilisateurs et clients cibles (10 points) :
Identification des utilisateurs et des équipes impliquées, avec description de leurs rôles respectifs (vaut pour 10 points)
6-Équipe projet et gouvernance (10 points) :
Présence d'une structure d'équipe et d'un processus de gouvernance clair pour le suivi de projet (vaut pour 10 points)
7-Planification et roadmap (5 points) :
Description d'un calendrier clair avec des étapes concrètes, incluant des jalons pour le suivi (vaut pour 5 points)
8-Risques et solutions (5 points) :
Identification des risques potentiels, accompagnée de stratégies de mitigation (vaut pour 5 points)
Notation :

0 point si aucune information
La moitié des points si cela répond partiellement à l'attente
Note maximale si cela répond pleinement à l'attente
Format de la réponse :

Utiliser des balises <##note_NomDeLaSection##> avant d'indiquer la note de chacune des sections. Exemple : <##note_Resume_executif##>5
Calculer la note totale comme somme des notes de chaque section, et l'indiquer avec la balise <##note_totale##>. Exemple : <##note_totale##>30
Questions pour amélioration :

Poser 3 questions pour améliorer la note sur les sections qui en ont le plus besoin, en les classant en fonction des points que cela rapporterait.
Utiliser une balise <##question##> avant de poser chaque question. Exemple : <##question##>Peux-tu m'en dire plus sur les gains potentiels que ton projet permettrait d'obtenir ?

Enfin, je ne veux aucun preambule et aucune explication sur les notes que tu proposes. Ne repete pas les consignes dans tes reponses. Le format de reponse que j'attends est simplement (a titre d'exemple):
<##note_Resume_executif##>10
<##note_Objectifs_et_benefices##>5
<##note_Cas_d_usage##>0
<##note_Budget_et_retour_sur_investissement##>0
<##note_Utilisateurs_et_clients_cibles##>0
<##note_Equipe_projet_et_gouvernance##>0
<##note_Planification_et_roadmap##>0
<##note_Risques_et_solutions##>0

<##note_totale##>15

<##question##>La premiere question que tu auras ?
<##question##>La deuxieme question que tu auras ?
<##question##>La troisieme question que tu auras ?"""


list_preparationForTheNextQuestion_g = [
"Merci pour ces complements ! Voici mes questions pour poursuivre:",
"Merci de partager tout ca avoir moi! Voici mes questions pour poursuivre:",
"Merci ! Voici mes questions pour poursuivre:",
"Ok je vois... Pour aller plus loin :",
"Super ! Voici mes questions pour poursuivre:",
"Hmm... ok ! Je crois que ça m'aide a y voir plus clair ! Voici mes questions pour poursuivre:",
"Ah oui ? Top ! Voici mes questions pour poursuivre:",
"Merci pour ces explications. Voici mes questions pour poursuivre:"]


# Ex 1er input user projet : J'ai une idée d'outil de planification du personnel naviguant pour les compagnies aérienne, qui peut leur faire gagner jusqu'a 5% de productivite.
# Ex 2eme input : plus spécifiquement, cet outil sera développer par les équipes RO (4 ingénieurs en optimisation à temps plein pendant 1 an) et consiste à utiliser les méthodes de programmation linéaire afin de coder des algorithmes permettant d'optimiser le remplissage des plannings des hôtesses et stewards, tout en respectant les contraintes réglementaires de chaque compagnie aérienne. Aujourd'hui ce processus est fait à la main avec des agents planificateurs, ce qui ne permet pas de s'approcher de la solution optimale d'affectation chaque mois. Grâce à ce projet, nous calculerons en 1 journée chaque moi (contre 10 jours aujourd'hui) les plannings mensuels, et nous garantirons une augmentation de 5% de productivité.

beginning_of_chat = 1   # global variable to adjust the prompt for the first interaction


# Prepare the mistral prompt
#conversation_history.append(
#        {
#            "role": "user",
#            "content": (
#                prompt_prep_1
#            ),
#        })
#conversation_history.append(
#        {
#            "role": "user",
#            "content": (
#                prompt_prep_2
#            ),
#        })
#conversation_history.append(
#        {
#            "role": "user",
#            "content": (
#                prompt_prep_3
#            ),
#        })
conversation_history.append(
        {
            "role": "user",
            "content": (
                prompt_reshaped
            ),
        })
#conversation_history.append(
#        {
#            "role": "user",
#            "content": (
#                prompt_consigne
#            ),
#        })


chat_response = throttled_chat_complete(client,
    model= model,
    messages = conversation_history
)

conversation_history.append({
        "role": "assistant",
        "content": chat_response.choices[0].message.content
    })
    

# Fonction pour générer une réponse simple du bot
def get_bot_response(user_input):
    
    global beginning_of_chat
    global question_list
    
    prompt_l = user_input
    if beginning_of_chat:
        prompt_l = "Ok, voici la premiere idee projet que je te propose d'evaluer : "+prompt_l
    
    # Add user input to the conversation history
    conversation_history.append({
        "role": "user",
        "content": prompt_l
    })
    
    # Send the entire conversation history to the API
    chat_response = throttled_chat_complete(client,
        model=model,
        messages=conversation_history
    )
    # Extract the bot's response content (as a plain string)
    bot_response_content = chat_response.choices[0].message.content
    
    # Extract the current evaluation of the document if any
    match = re.search(r"<##note_totale##>\s*(\d+)", bot_response_content)
    total_note = 0
    if match:
        total_note = match.group(1)  # Extract the number after the tag
    
    # Extract the list of follow-up questions to ask
    questions = re.findall(r"<##question##>(.*?)(?=<|\n|$)", bot_response_content)
    question_list = []
    if questions:
        question_list = [question.strip() for question in questions]
    
    random_question = "Je n'ai pas d'autre question. Merci !"
    if len(question_list) > 0:
        random_question = random.choice(question_list)
    
    random_prep = ""
    if beginning_of_chat:
        random_prep = "Merci pour cette premiere description ! J'evalue la completude de ton descriptif sur la droite de l'ecran. Je vais te poser quelques questions pour augmenter le score si tu veux bien ! Mes premieres sont:"
    
    else:
        random_prep = random.choice(list_preparationForTheNextQuestion_g)
    
    # Add bot response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": bot_response_content
    })
    
    bot_response = random_prep
    for question in question_list:
        bot_response += "\n - " + question
    
    # It's not the first interaction anymore
    beginning_of_chat = 0
    
    #return bot_response_content
    return bot_response, total_score
    
   