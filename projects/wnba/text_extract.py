from typing import List

import os
import nltk

from extr.entities import create_entity_extractor, \
                          KnowledgeBaseEntityLinker, \
                          EntityAnnotator
from extr.relations import RelationExtractor
from extr.entities.context import ConText

from bb.labels.entity_patterns import entity_patterns
from bb.labels.relation_patterns import relation_patterns
from bb.rules.context import rule_grouping
from bb.knowledge.kb import kb

from bb.utils.filesystem import load_data, save_data


entity_extractor = create_entity_extractor(entity_patterns)

entity_annotator = EntityAnnotator()
relation_extractor = RelationExtractor(relation_patterns)

conText = ConText(
    rule_grouping=rule_grouping,
    word_tokenizer=nltk.tokenize.word_tokenize
)

entity_linker = KnowledgeBaseEntityLinker(
    attribute_label='concepts',
    kb=kb
)

def extract_data(text: str):
    entities = entity_extractor.get_entities(text)
    entities = entity_linker.link(entities)
    entities = conText.apply(
        text,
        entities,
        filter_out_rule_labels=True
    )
    
    relations = relation_extractor.extract(
        entity_annotator.annotate(text, entities),
        entities
    )

    return entities, relations

def extract(shot_chart):
    for shot in shot_chart['shots']:
        extracts = {}

        text = shot['text']
        entities, relations = extract_data(text)

        id_to_relation = {}
        for relation in relations:
            id_to_relation[relation.definition] = relation

        if 'r("QUANTITY", "UNITS")' in id_to_relation:
            is_units_of = id_to_relation['r("QUANTITY", "UNITS")']
            extracts['distance'] = int(is_units_of.e1.text)

        if 'r("SHOT", "ACTION")' in id_to_relation:
            is_of_type = id_to_relation['r("SHOT", "ACTION")']
            extracts['before'] = is_of_type.e2.text.split(' ')

        extracted_shot = [
            entity
            for entity in entities
            if entity.label == 'SHOT'
        ][0]

        extracts['text'] = extracted_shot.text

        if 'pullup' in extracted_shot.text:
            if 'before' in extracts:
                extracts['before'].append('pullup')
            else:
                extracts['before'] = ['pullup']

        ctypes = list(extracted_shot.get_attributes_by_label('ctypes'))
        if len(ctypes) > 0:
            extracts['info'] = ctypes

        concepts = list(extracted_shot.get_attributes_by_label('concepts'))
        if len(concepts) > 0:
            extracts['after'] = concepts
        
        shot['extracts'] = extracts

    return shot_chart

def run():
    for file in os.listdir('./data/pbps/'):
        file_path = f'./data/pbps/{file}'
        save_data(
            file_path,
            extract(
                load_data(file_path)
            )
        )

if __name__ == '__main__':
    run()
