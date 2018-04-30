#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:23:09 2018

@author: amberkiser
"""

from PyRuSH.RuSH import RuSH
from pyConTextNLP import pyConTextGraph
from pyConTextNLP.utils import get_document_markups


from DocumentClassifier import FeatureInferencer
from DocumentClassifier import DocumentInferencer
from nlp_pneumonia_utils import markup_sentence
from itemData import get_item_data
from visual import convertMarkups2DF


# because there are too many sentence segmentation rules, let's read them from an external file
sentence_rules='Rules/rush_rules.tsv'
# you can point target_rules to a file path instead, if there are many rules
target_rules='''
Comments: ''
Direction: ''
Lex: fever
Regex: ''
Type: FEVER
---
Comments: ''
Direction: ''
Lex: high temperature
Regex: '1\d\d\.\d F'
Type: FEVER'''
# context rules are often lengthy, you can point context_rules to an external rule files instead
context_rules='''Comments: ''
Direction: forward
Lex: 'no'
Regex: ''
Type: DEFINITE_NEGATED_EXISTENCE
---
Comments: ''
Direction: forward
Lex: 'denies'
Regex: ''
Type: DEFINITE_NEGATED_EXISTENCE
'''
# define the feature inference rule
feature_inference_rule='''
#Conclusion type, Evidence type, Modifier values associated with the evidence
NEGATED_CONCEPT,FEVER,DEFINITE_NEGATED_EXISTENCE
'''
# define the document inference rule
document_inference_rule='''
#Conclusion Type at document level, Evidence type at mention level
FEVER_DOC,FEVER

#Default document type
NO_FEVER
'''

sentence_segmenter = RuSH(sentence_rules)
feature_inferencer=FeatureInferencer(feature_inference_rule)
document_inferencer = DocumentInferencer(document_inference_rule)

targets=get_item_data(target_rules)
modifiers=get_item_data(context_rules)

# Example sentences
#input = 'This is a sentence. It is just a test. I like this sentence.'

input='''
No vomiting, chest pain, shortness of breath, nausea, dizziness, or chills on arrival.
On operative day three, the patient fever was detected with temperature 101.5 F.
After 3 days no fever was detected.
Patient came back for a follow up, denies fever.
'''

sentences=sentence_segmenter.segToSentenceSpans(input)

# See what the document was splitted into
for sentence in sentences:
    print("Sentence({}-{}):\t{}".format(sentence.begin, sentence.end, input[sentence.begin:sentence.end]))
    print('\n'+'-'* 100+'\n')
    
# initiate a pyConTextGraph to hold the pyConText output
context_doc = pyConTextGraph.ConTextDocument()

for sentence in sentences:
    sentence_text=input[sentence.begin:sentence.end].lower()
    # Process every sentence by adding markup
    m = markup_sentence(sentence_text, modifiers=modifiers, targets=targets)
    context_doc.addMarkup(m)
    context_doc.getSectionMarkups()
    print(m)

# convert graphic markups into dataframe    
markups = get_document_markups(context_doc)
annotations, relations, doc_txt = convertMarkups2DF(markups) 

head(annotations)

# apply inferences for document classication
inferenced_types = feature_inferencer.process(annotations, relations)
print('After inferred from modifier values, we got these types:\n '+str(inferenced_types))
doc_class = document_inferencer.process(inferenced_types)
print('\nDocument classification: '+ doc_class )


