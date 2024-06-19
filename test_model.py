import spacy

# Assurez-vous que le chemin est correct pour charger le modèle entraîné
nlp = spacy.load("model")

# Exemples de textes à tester
test_texts = [
    "Bonjour",
    "Comment puis-je ouvrir un compte chez Attijari?",
    "J'ai oublié mon mot de passe bancaire en ligne, que faire?",
    "Quels types de comptes offrez-vous?"
]

# Exécuter le modèle sur les textes de test et afficher les catégories prédites
for text in test_texts:
    doc = nlp(text)
    print(f"Texte: '{text}' - Catégorie prédite: {doc.cats}")
