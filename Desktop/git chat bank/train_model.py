import spacy
from spacy.training import Example
from spacy.util import minibatch
import random
from train_data import TRAIN_DATA

# Charger un modèle spaCy vierge
nlp = spacy.blank('fr')  # Utilisez 'fr' pour le français

# Ajouter le TextCategorizer au pipeline de nlp
if 'textcat_multilabel' not in nlp.pipe_names:
    textcat = nlp.add_pipe('textcat_multilabel', last=True)

# Ajouter les catégories au textcat
for _, annotations in TRAIN_DATA:
    for cat in annotations['cats']:
        textcat.add_label(cat)

# Entraîner le modèle
optimizer = nlp.begin_training()
for i in range(10):
    random.shuffle(TRAIN_DATA)
    losses = {}
    batches = minibatch(TRAIN_DATA, size=8)
    for batch in batches:
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
    print(f'Epoch {i}, Losses: {losses}')

# Sauvegarder le modèle entraîné
nlp.to_disk("model")
