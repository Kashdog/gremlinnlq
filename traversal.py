import spacy
from spacy import displacy

nlp = spacy.load('en')
fetchtokens = ['give', 'show', 'find', 'retrieve', 'get', 'download', 'select', 'obtain', 'show', 'display']
keywords = {'databases': 'database', 'assets': 'asset', 'steward': 'is_steward_of', 'people': 'person', 'collections': 'collection'}
inverb = {'stewarded': 'is_steward_of', 'used': 'uses', 'rated': 'rates', 'commented': 'comments', 'contained': 'contains'}
outverb = {'contain': 'contains', 'containing': 'contains'}

used = ['used']
doc = nlp(u'find all collections that contain ABC')
be = ['is','has', 'was', 'are']
#doc = nlp(u'Show me all assets that are Critical and have a quality score below 90')
k = []
phrase = ""
for token in doc:
    #print(token.text, token.dep_, token.tag_, token.head.text, token.head.pos_,
          #[child for child in token.children])
    if(token.dep_ == "ROOT"):  
        if token.text in fetchtokens:
            phrase += r"g.V().has('types', '{}')" 
            for child in token.children:
                if child.dep_ == "dobj":
                    if child.text in keywords:
                        k.append(keywords[child.text])
                        phrase = phrase.format(*k)
                        k = []
                    for dobjchild in child.children:
                        if dobjchild.dep_ == "relcl":
                            if dobjchild.text in be:
                                phrase += r".where(_.in('{}').has('name', '{}'))"
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "attr":
                                        k.append(keywords[relclchild.text])
                                        
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "nsubj":
                                        k.append(relclchild.text)
                                phrase = phrase.format(*k)
                                k = []       
                            if dobjchild.text in inverb:
                                phrase += r".where(_.in('" + inverb[dobjchild.text]+ r"').has('name', '{}'))"
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "agent":
                                        for agentchild in relclchild.children:
                                            if agentchild.dep_ == "pobj":
                                                k.append(agentchild.text)
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "dobj":
                                        k.append(relclchild.text)
                                phrase = phrase.format(*k)
                                k = []
                            if dobjchild.text in outverb:
                                phrase += r".where(_.out('" + outverb[dobjchild.text]+ r"').has('name', '{}'))"
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "agent":
                                        for agentchild in relclchild.children:
                                            if agentchild.dep_ == "pobj":
                                                k.append(agentchild.text)
                                for relclchild in dobjchild.children:
                                    if relclchild.dep_ == "dobj":
                                        k.append(relclchild.text)
                                phrase = phrase.format(*k)
                                k = []
                    for dobjchild in child.children:
                        if dobjchild.dep_ == "acl":
                            if dobjchild.text in inverb:
                                phrase += r".where(_.in('" + inverb[dobjchild.text]+ r"').has('name', '{}'))"
                                for aclchild in dobjchild.children:
                                        if aclchild.dep_ == "agent":
                                            for agentchild in aclchild.children:
                                                if agentchild.dep_ == "pobj":
                                                    k.append(agentchild.text)
                                for aclchild in dobjchild.children:
                                    if aclchild.dep_ == "dobj":
                                        k.append(aclchild.text)
                                phrase = phrase.format(*k)
                                k = []
                            if dobjchild.text in outverb:
                                phrase += r".where(_.out('" + outverb[dobjchild.text]+ r"').has('name', '{}'))"
                                for aclchild in dobjchild.children:
                                        if aclchild.dep_ == "agent":
                                            for agentchild in aclchild.children:
                                                if agentchild.dep_ == "pobj":
                                                    k.append(agentchild.text)
                                for aclchild in dobjchild.children:
                                    if aclchild.dep_ == "dobj":
                                        k.append(aclchild.text)
                                phrase = phrase.format(*k)
                                k = []
                    for dobjchild in child.children:
                        if dobjchild.dep_ == "amod":
                            if dobjchild.text in used:
                                phrase = ""
                                phrase += r"g.E().has('name', 'uses').inV().has('types', '{}')"
                                k.append(keywords[child.text])
                                phrase = phrase.format(*k)
                                k = []
                                for amodchild in dobjchild.children:
                                    if amodchild.dep_ == "advmod":
                                        if amodchild.text == "frequently":
                                            phrase += r".dedup().order().by(inE('uses').values('count').sum(), {})"
                                            for advmodchild in amodchild.children:
                                                if advmodchild.dep_ == "advmod":
                                                    if advmodchild.text == "most":
                                                        k.append('decr')
                                                    elif advmodchild.text == "least":
                                                        k.append('incr')
                                phrase = phrase.format(*k)
                                k = []
                        if dobjchild.dep_ == "prep":
                            print(dobjchild.text)
                            for prepchild in dobjchild.children:
                                if prepchild.dep_ == "pobj":
                                    k.append(prepchild.text)
            for child in token.children:
                if child.dep_ == "ccomp":
                    if child.text in be:
                        phrase += r".where(_.in('{}').has('name', '{}'))"
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "nsubj" and ccompchild.text in keywords:
                                k.append(keywords[ccompchild.text])
                        if child.text in inverb:
                            phrase += r".where(_.in('" + inverb[child.text]+ r"').has('name', '{}'))"
                            for aclchild in child.children:
                                    if aclchild.dep_ == "agent":
                                        for agentchild in aclchild.children:
                                            if agentchild.dep_ == "pobj":
                                                k.append(agentchild.text) 
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "attr":
                                k.append(keywords[ccompchild.text])
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "nsubj" and ccompchild.text in keywords:
                                for nsubjchild in ccompchild.children:
                                    if nsubjchild.dep_ == "appos":
                                        k.append(nsubjchild.text)
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "nsubj" and ccompchild.text not in keywords and child.text not in used:
                                k.append(ccompchild.text)
                        phrase = phrase.format(*k)
                        k = []

                    if child.text in used:
                        phrase = ""
                        phrase += r"g.E().has('name', 'uses').inV().has('types', '{}')"
                    if child.text in used:
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "dobj":
                                k.append(keywords[ccompchild.text])
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "advmod":
                                if ccompchild.text == "frequently":
                                    phrase += r".dedup().order().by(inE('uses').values('count').sum(), {})"
                                    for advmodchild in ccompchild.children:
                                        if advmodchild.dep_ == "advmod":
                                            if advmodchild.text == "most":
                                                k.append('decr')
                        for ccompchild in child.children:
                            if ccompchild.dep_ == "nsubj":
                                phrase += r".limit({})"
                                k.append(ccompchild.text)
                                phrase = phrase.format(*k)
                                k = []

print(phrase)
displacy.serve(doc, style='dep')