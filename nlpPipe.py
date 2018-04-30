from PyRuSH.RuSH import RuSH
from pyConTextNLP import pyConTextGraph
from itemData import get_item_data
from pipeUtils import Annotation


class ClassificationPipe(object):
    def __init__(self, sentence_rules, target_rules, context_rules):
        self.sentence_segmenter = RuSH(sentence_rules)
        self.targets = get_item_data(target_rules)
        self.modifiers = get_item_data(context_rules)
    
    def process(self, doc_text):
        sentences = self.sentence_segmenter.segToSentenceSpans(doc_text)
        
        new_anns = []
        for sentence in sentences:
            start_offset = sentence.begin
            sentence_text = doc_text[sentence.begin:sentence.end].lower()
            m = self.markup_sentence(sentence_text, modifiers=self.modifiers, targets=self.targets)
            annotations = self.convertMarkupsAnnotations(m, sentence_text, start_offset)
            new_anns.extend(annotations)

        return new_anns

    def markup_sentence(self, sentence, modifiers, targets):
        markup = pyConTextGraph.ConTextMarkup()
        txt = sentence.lower()
        markup.setRawText(txt)
        markup.graph["__txt"] = txt
        markup.graph["__scope"] = (0, len(txt))
        markup.markItems(targets, mode="target")
        markup.markItems(modifiers, mode="modifier")
        markup.pruneMarks()
        markup.dropMarks('Exclusion')
        markup.applyModifiers()
        markup.pruneSelfModifyingRelationships()
        markup.dropInactiveModifiers()
        return markup
    
    def convertMarkupsAnnotations(self, markups, sentence_text, offset=0):
        annotations=[]
        nodes = markups.nodes()
        for n in nodes:
            new_ann = Annotation(start_index=offset+n.getSpan()[0],
                                 end_index=offset+n.getSpan()[1], 
                                 type=n.getCategory()[0], 
                                 spanned_text = sentence_text[n.getSpan()[0]:n.getSpan()[1]], 
                                 ann_id=n.getTagID())
            mods = markups.getModifiers(n)
            if(len(mods) > 0):
                for modifier in mods:
                    new_ann.attributes[modifier.getCategory()[0]]=modifier.getTagID()
        
            annotations.append(new_ann)
        return annotations


class ExtractionPipe(object):
    def __init__(self, sentence_rules, target_rules, between_rules):
        self.sentence_segmenter = RuSH(sentence_rules)
        self.targets = get_item_data(target_rules)
        self.between_rules = between_rules

    def process(self, doc_text):
        sentences = self.sentence_segmenter.segToSentenceSpans(doc_text)

        new_anns = []
        for sentence in sentences:
            start_offset = sentence.begin
            sentence_text = doc_text[sentence.begin:sentence.end].lower()
            m = self.markup_sentence_extract(sentence_text, targets=self.targets)
            annotations = self.classify_relationships(m, sentence_text, start_offset)
            new_anns.extend(annotations)

        return new_anns

    def markup_sentence_extract(self, sentence, targets):
        markup = pyConTextGraph.ConTextMarkup()
        txt = sentence.lower()
        markup.setRawText(txt)
        markup.graph["__txt"] = txt
        markup.graph["__scope"] = (0, len(txt))
        markup.markItems(targets, mode="target")
        markup.pruneMarks()
        markup.dropMarks('Exclusion')
        markup.pruneSelfModifyingRelationships()
        return markup

    def classify_relationships(self, markups, sentence_text, offset = 0):
        all_targets = markups.getMarkedTargets()
        annotations = []
        if len(all_targets) > 1:
            for index, target in enumerate(all_targets):
                target_cat = target.getCategory()[0]
                try:
                    future_target = all_targets[index + 1]
                    future_cat = future_target.getCategory()[0]
                except Exception:
                    pass
                if target_cat == 'oxygen_saturation':
                    if future_cat == 'value':
                        start_text_index = target.getSpan()[1]
                        end_text_index = future_target.getSpan()[0]
                        between_text = sentence_text[start_text_index:end_text_index]
                        between_text = between_text.strip()
                        if between_text in self.between_rules:
                            new_ann = Annotation(start_index=offset + future_target.getSpan()[0],
                                                 end_index=offset + future_target.getSpan()[1],
                                                 type=future_cat,
                                                 spanned_text=sentence_text[
                                                              future_target.getSpan()[0]:future_target.getSpan()[1]],
                                                 ann_id=future_target.getTagID())
                            annotations.append(new_ann)
        return annotations
