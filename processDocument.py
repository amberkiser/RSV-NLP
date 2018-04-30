from nlpPipe import ClassificationPipe, ExtractionPipe
import pandas as pd
import re


class ProcessClassificationDoc(object):
    def __init__(self, document, sentence_rules, target_rules, context_rules):
        self.document = document
        self.sentence_rules = sentence_rules
        self.target_rules = target_rules
        self.context_rules = context_rules

    def make_dataframe(self):
        doc_annotations = self.make_annotations()

        class_columns = ['PatientId', 'DocumentId', 'SpanStart', 'SpanEnd', 'SpanText', 'Status']
        classification_df = pd.DataFrame(columns=class_columns)

        for ann in doc_annotations:
            if ann.type == 'rsv':
                patient_id = self.document.document_id[:3]
                doc_id = self.document.document_id
                span_start = ann.start_index
                span_end = ann.end_index
                span_text = ann.spanned_text
                status = 'affirmed'
                for k, v in ann.attributes.items():
                    if k == 'hypothetical' or k == 'negated':
                        status = k
                ann_dict = {'PatientId': patient_id, 'DocumentId': doc_id, 'SpanStart': span_start,
                            'SpanEnd': span_end, 'SpanText': span_text, 'Status': status}
                classification_df = classification_df.append(ann_dict, ignore_index=True)

        return classification_df

    def make_annotations(self):
        classification_pipe = ClassificationPipe(self.sentence_rules, self.target_rules, self.context_rules)
        doc_annotations = classification_pipe.process(self.document.text)
        return doc_annotations


class ProcessExtractionDoc(object):
    def __init__(self, document, sentence_rules, target_rules, between_rules):
        self.document = document
        self.sentence_rules = sentence_rules
        self.target_rules = target_rules
        self.between_rules = between_rules

    def make_dataframe(self):
        doc_annotations = self.make_annotations()

        extract_columns = ['PatientId', 'DocumentId', 'SpanStart', 'SpanEnd', 'SpanText', 'OxygenSaturation']
        extraction_df = pd.DataFrame(columns=extract_columns)

        for ann in doc_annotations:
            patient_id = self.document.document_id[:3]
            doc_id = self.document.document_id
            span_start = ann.start_index
            span_end = ann.end_index
            span_text = ann.spanned_text
            o2sat = [int(s) for s in re.findall(r'\b\d+\b', span_text)][0]
            ann_dict = {'PatientId': patient_id, 'DocumentId': doc_id, 'SpanStart': span_start,
                        'SpanEnd': span_end, 'SpanText': span_text, 'OxygenSaturation': o2sat}
            extraction_df = extraction_df.append(ann_dict, ignore_index=True)

        return extraction_df

    def make_annotations(self):
        extraction_pipe = ExtractionPipe(self.sentence_rules, self.target_rules, self.between_rules)
        doc_annotations = extraction_pipe.process(self.document.text)
        return doc_annotations
