from pipeUtils import Document
from processDocument import ProcessClassificationDoc, ProcessExtractionDoc
import pandas as pd


class RunClassificationNLP(object):
    def __init__(self, doc_list, path_of_docs, sentence_rules, target_rules, context_rules):
        self.doc_list = doc_list
        self.path_of_docs = path_of_docs
        self.sentence_rules = sentence_rules
        self.target_rules = target_rules
        self.context_rules = context_rules

    def RunPipeline(self):
        class_columns = ['PatientId', 'DocumentId', 'SpanStart', 'SpanEnd', 'SpanText', 'Status']
        class_df = pd.DataFrame(columns=class_columns)
        for doc in self.doc_list:
            try:
                txt_file = (self.path_of_docs + '/' + doc + '.txt')
                ann_file = (self.path_of_docs + '/' + doc + '.ann')

                document = Document()
                document.load_document_from_file(txt_file)
                document.load_annotations_from_brat(ann_file)
                class_pipe = ProcessClassificationDoc(document, self.sentence_rules, self.target_rules, self.context_rules)
                df = class_pipe.make_dataframe()
                class_df = class_df.append(df)
            except Exception:
                pass
        return class_df


class RunExtractionNLP(object):
    def __init__(self, doc_list, path_of_docs, sentence_rules, target_rules, between_rules):
        self.doc_list = doc_list
        self.path_of_docs = path_of_docs
        self.sentence_rules = sentence_rules
        self.target_rules = target_rules
        self.between_rules = between_rules

    def RunPipeline(self):
        extract_columns = ['PatientId', 'DocumentId', 'SpanStart', 'SpanEnd', 'SpanText', 'OxygenSaturation']
        extraction_df = pd.DataFrame(columns=extract_columns)
        for doc in self.doc_list:
            try:
                txt_file = (self.path_of_docs + '/' + doc + '.txt')
                ann_file = (self.path_of_docs + '/' + doc + '.ann')

                document = Document()
                document.load_document_from_file(txt_file)
                document.load_annotations_from_brat(ann_file)

                extract_pipe = ProcessExtractionDoc(document, self.sentence_rules, self.target_rules, self.between_rules)
                df = extract_pipe.make_dataframe()
                extraction_df = extraction_df.append(df)
            except Exception:
                pass

        return extraction_df
