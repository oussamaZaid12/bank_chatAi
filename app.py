# app.py
from flask import Flask, request, jsonify, render_template
import spacy

app = Flask(__name__, static_folder=".", static_url_path="")
nlp = spacy.load("model")  # Assurez-vous que le modèle est chargé correctement

def select_category(doc):
    threshold = 0.5  # Abaisser le seuil pour être moins restrictif
    sorted_cats = sorted(doc.cats.items(), key=lambda x: x[1], reverse=True)
    
    # Accepter la catégorie si son score est supérieur au seuil
    if sorted_cats[0][1] > threshold:
        return sorted_cats[0][0]
    return "unknown"

def get_fallback_response(input_text):
    greetings = ["bonjour", "salut", "hello", "hi", "bonsoir"]
    if any(greet in input_text.lower() for greet in greetings):
        return "Bonjour! Comment puis-je vous aider aujourd'hui?"
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-response', methods=['POST'])
def get_response():
    user_input = request.json.get('input')
    fallback_response = get_fallback_response(user_input)
    if fallback_response:
        return jsonify({'response': fallback_response})
    
    doc = nlp(user_input)
    category = select_category(doc)
    
    response_mapping = {
        "salutation": "Bonjour! Comment puis-je vous aider aujourd'hui?",
        "ouverture_compte": "Vous pouvez ouvrir un compte directement sur notre site web ou en visitant une de nos succursales.",
        "support_technique": "Pour toute assistance technique, veuillez contacter notre support technique.",
        "info_compte": "Nous offrons divers types de comptes, incluant des comptes courants, des comptes d'épargne, et des comptes pour entreprises.",
        "demande_pret": "Vous pouvez demander un prêt en ligne via notre site web ou en visitant l'une de nos succursales pour plus d'informations.",
        "info_generale": "Pour toute information générale, vous pouvez consulter la FAQ sur notre site ou nous appeler directement.",
        "info_sucursale": "Vous pouvez trouver les adresses de toutes nos succursales sur notre site dans la section Contacts.",
        "info_investissement": "Nous offrons une gamme de produits d'investissement. Pour en savoir plus, je vous invite à consulter notre section dédiée aux investissements sur notre site.",
        "info_assurance": "Nous proposons diverses options d'assurance. Pour plus de détails, veuillez visiter la section assurances de notre site.",
        "fermeture_compte": "Pour fermer votre compte, veuillez vous connecter à votre espace client et suivre les instructions ou contacter notre support client.",
        "question_rh_ssi": "Pour les questions relatives aux ressources humaines ou à la sécurité des systèmes d'information, veuillez consulter le portail interne ou contacter le département concerné.",
        "unknown": "Je suis désolé, je ne comprends pas votre demande. Pouvez-vous reformuler?"
    }
    
    response = response_mapping.get(category, "Je suis désolé, je ne comprends pas votre demande.")
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
