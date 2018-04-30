import os
import pandas as pd
from ProcessAllDocuments import RunClassificationNLP, RunExtractionNLP

# Input the path to your documents.
path_of_docs = 'Documents/example'

file_list=[f[:-4] for f in os.listdir(path_of_docs) if f.endswith('.txt')]

# Input rules
sentence_rules = 'Rules/rush_rules.tsv'
classification_targets = 'Rules/classification_targets.yml'
classification_context = 'Rules/classification_modifiers.yml'
extraction_targets = 'Rules/extraction_targets.yml'
between_rules = [':', 'was', 'were', 'is', 'are', '', '/']

class_nlp = RunClassificationNLP(file_list, path_of_docs, sentence_rules, classification_targets, classification_context)
class_df = class_nlp.RunPipeline()
writer_class = pd.ExcelWriter('classification.xlsx')
class_df.to_excel(writer_class, 'Sheet1', index=False)
writer_class.save()

extract_nlp = RunExtractionNLP(file_list, path_of_docs, sentence_rules, extraction_targets, between_rules)
extract_df = extract_nlp.RunPipeline()
writer_extract = pd.ExcelWriter('extraction.xlsx')
extract_df.to_excel(writer_extract, 'Sheet1', index=False)
writer_extract.save()
