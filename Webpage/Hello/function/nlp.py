import spacy
from spacy import displacy
import visualise_spacy_tree
from pathlib import Path

nlp = spacy.load("en_core_web_sm")


# extracting the basic info of the product needed to solve the problem
def products(question):
    doc = nlp(question)
    things_and_adjectives = []

    for token in doc:
        if token.pos_ in ["NOUN"]:
            for child in token.children:
                if child.pos_ == "NUM":
                    things_and_adjectives.append(child.text)
                if child.pos_ == "ADJ":
                    things_and_adjectives.append(child.text)
            things_and_adjectives.append(token.text)

    output = '+'.join(things_and_adjectives)
    print(output)
    return output


# visualize the sentence struce and the relation the words present in it
def visualization(sentence):
    doc = nlp(sentence)
    
    svg = displacy.render(doc, style="dep", jupyter=False)
    png = visualise_spacy_tree.create_png(sentence)
    
    file_name = '-'.join([w.text for w in doc if not w.is_punct]) + ".svg"
    output_path = Path("sentence_structure_simple/" + file_name)
    output_path.open("w", encoding="utf-8").write(svg)
