import spacy
from spacy import displacy

nlp = spacy.load('en')
fetchtokens = ['give', 'show', 'find', 'retrieve', 'get', 'download', 'select', 'obtain', 'show', 'display']
keywords = {'databases': 'database', 'assets': 'asset', 'steward': 'is_steward_of'}
doc = nlp(u'find all assets ABC is a steward of')
#doc = nlp(u'Show me all assets that are Critical and have a quality score below 90')
k = [None] * 10
phrase = ""
for token in doc:
    if(token.dep_ == "ROOT"):
        if token.text in fetchtokens:
            phrase += r"g.V().has('types', '{}')"
    if token.dep_ == "dobj" and token.head.dep_ == "ROOT":
        k[0] = keywords[token.text]
    if token.dep_ == "ccomp" and token.head.dep_ == "ROOT":
        phrase += r".where(_in('{}').has('name', '{}'))"
    if token.dep_ == "attr" and token.head.dep_ == "ccomp":
        k[1] = keywords[token.text]
    if token.dep_ == "nsubj" and token.head.dep_ == "ccomp":
        k[2] = token.text
    #.where(__.in('is_steward_of').has('name', 'ABC'))
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])
print(phrase.format(*k))
displacy.serve(doc, style='dep')