from typing import List

import os
import nltk

from extr.entities import create_entity_extractor, \
                          KnowledgeBaseEntityLinker, \
                          EntityAnnotator
from extr.relations import RelationExtractor
from extr.entities.context import ConText
from extr.pipelines import EntityPipeline, RelationPipeline

from bb.labels.entity_patterns import entity_patterns
from bb.labels.relation_patterns import relation_patterns
from bb.rules.context import rule_grouping
from bb.knowledge.kb import kb

from bb.utils.filesystem import load_data, save_data


relation_extractor = RelationPipeline(
    EntityPipeline(
        create_entity_extractor(entity_patterns),
        KnowledgeBaseEntityLinker(
            attribute_label='concepts',
            kb=kb
        ),
        ConText(
            rule_grouping=rule_grouping,
            word_tokenizer=nltk.tokenize.word_tokenize
        )
    ),
    EntityAnnotator(),
    RelationExtractor(relation_patterns)
)

def extract(shot_chart):
    for shot in shot_chart['shots']:
        extracts = {
            'info': []
        }

        text = shot['text']
        entities, relations = relation_extractor.extract(text)

        id_to_relation = {}
        for relation in relations:
            id_to_relation[relation.definition] = relation

        if 'r("QUANTITY", "UNITS")' in id_to_relation:
            is_units_of = id_to_relation['r("QUANTITY", "UNITS")']
            extracts['distance'] = {
                'value': int(is_units_of.e1.text),
                'unit': is_units_of.e2.text,
            }

        if 'r("SHOT", "ACTION")' in id_to_relation:
            is_of_type = id_to_relation['r("SHOT", "ACTION")']
            extracts['before'] = is_of_type.e2.text
            extracts['info'].extend(
                list(is_of_type.e2.get_attributes_by_label('concepts'))
            )

        extracted_shot = [
            entity
            for entity in entities
            if entity.label == 'SHOT'
        ][0]

        extracts['text'] = extracted_shot.text

        if 'pullup' in extracted_shot.text:
            if not 'before' in extracts:
                extracts['before'] = []

            extracts['before'].append(['pullup'])

        extracts['info'].extend(
            list(extracted_shot.get_attributes_by_label('ctypes'))
        )

        extracts['info'].extend(
            list(extracted_shot.get_attributes_by_label('concepts'))
        )

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
