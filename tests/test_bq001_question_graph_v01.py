import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import quote

from scripts import bq001_question_graph_v01 as graph


class QuestionGraphTests(unittest.TestCase):
    def setUp(self):
        self.data = graph.load_json(graph.OUTPUT.read_bytes())

    def test_committed_graph_is_canonical_and_reproducible(self):
        graph.validate(self.data)
        self.assertEqual(graph.OUTPUT.read_text(), graph.canonical(graph.build()))
        self.assertEqual(graph.canonical(graph.build()), graph.canonical(graph.build()))

    def test_question_has_separate_curated_and_inferred_results(self):
        result = graph.retrieve(self.data)
        self.assertEqual(len(result['curated_edges']), 2)
        self.assertEqual(len(result['inferred_candidates']), 2)
        for edge in result['inferred_candidates']:
            self.assertEqual(edge['assertion_class'], 'INFERRED_CANDIDATE')
            self.assertEqual(edge['review_state'], 'REVIEW_REQUIRED')
            self.assertIs(edge['accepted_edge'], False)
        self.assertEqual(result['question_status'], 'UNRESOLVED')
        self.assertFalse(any(result['guards'].values()))

    def test_model_retrieval_preserves_competing_candidate_and_provenance(self):
        node = 'node:model:MODEL-BQ001-BIOLOGICAL-DEPENDENCE'
        result = graph.retrieve(self.data, node)
        self.assertEqual(len(result['curated_edges']), 1)
        self.assertEqual(len(result['inferred_candidates']), 2)
        original = {e['edge_id']: e for e in self.data['edges']}
        for edge in result['curated_edges'] + result['inferred_candidates']:
            self.assertEqual(edge, original[edge['edge_id']])
        # No recursive walk pulling the correction into model evidence.
        self.assertNotIn('CORRECTS', [e['relationship_type'] for e in result['curated_edges']])

    def test_curated_view_cannot_reclassify_inference(self):
        result = graph.retrieve(self.data, view='curated')
        self.assertEqual(result['inferred_candidates'], [])
        self.assertTrue(all(e['assertion_class'] == 'DIRECT_SOURCE_METADATA' for e in result['curated_edges']))

    def test_unknown_query_fails_without_echo(self):
        for kwargs in ({'node_id': 'private-unrecognized-id'}, {'view': 'accepted'}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                graph.retrieve(self.data, **kwargs)

    def test_response_does_not_mutate_graph(self):
        original = graph.canonical(self.data)
        result = graph.retrieve(self.data)
        result['curated_edges'][0]['accepted_edge'] = True
        self.assertEqual(graph.canonical(self.data), original)

    def test_governance_mutations_fail_closed(self):
        changes = [
            lambda d: d.update(question_status='RESOLVED'),
            lambda d: d.update(finality='FINAL'),
            lambda d: d['guards'].update(truth_inference=True),
            lambda d: d['guards'].update(scientific_evidence_promotion=True),
            lambda d: d['guards'].update(rights_inference=True),
            lambda d: d['guards'].update(public_status_inference=True),
            lambda d: d['guards'].update(edge_acceptance=True),
            lambda d: d['guards'].update(truth_inference=0),
            lambda d: d['edges'][0].update(accepted_edge=True),
            lambda d: d['edges'][0].update(review_state='ACCEPTED'),
            lambda d: d['edges'][0].update(source_node_id='node:missing'),
            lambda d: d['edges'][0]['provenance'].pop('record_locator'),
            lambda d: d['edges'][0]['provenance'].update(record_locator='/models/0/model_id'),
            lambda d: d['edges'][0].update(evidence_independence_keys=['invented']),
            lambda d: d['edges'][0]['parent_edge_ids'].append(d['edges'][0]['edge_id']),
            lambda d: d['curated_edge_ids'].__setitem__(0, d['inferred_edge_ids'][0]),
            lambda d: d['nodes'].append(copy.deepcopy(d['nodes'][0])),
            lambda d: d['baseline_locks'].update({'v0.14': 'a' * 40}),
            lambda d: d['coverage'].update(accepted_edges=1),
            lambda d: d['coverage'].update(exhaustive=True),
            lambda d: d['input'].update(sha256='a' * 64),
            lambda d: d['edges'][0].update(confidence=0.99),
        ]
        for index, change in enumerate(changes):
            data = copy.deepcopy(self.data)
            change(data)
            with self.subTest(index=index), self.assertRaises(ValueError):
                graph.retrieve(data)

    def test_private_keys_values_encoded_links_and_hashes_rejected(self):
        cases = [
            {'drive_id': 'synthetic-private'},
            {'DriveFileID': 'synthetic-private'},
            {'object_hash': 'a' * 64},
            {'https://drive.google.com/file/d/synthetic/view': 'key'},
            {'label': 'https%3A%2F%2Fdrive.google.com%2Ffile%2Fd%2Fsynthetic'},
            {'label': '/My Drive/synthetic.pdf'},
            {'label': 'a' * 64},
            {'label': 'AKM-synthetic'},
            {'label': '1AbCdEfGhIjKlMnOpQrStUvWxYz012345'},
        ]
        for payload in cases:
            data = copy.deepcopy(self.data)
            data['nodes'][0].update(payload)
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                graph.validate(data)
        with self.assertRaises(ValueError):
            graph.privacy_check([['https://drive.google.com/open?id=synthetic']])

    def test_duplicate_keys_and_nonfinite_json_rejected(self):
        for raw in ('{"question_id":"BQ001","question_id":"other"}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                graph.load_json(raw)

    def test_safe_input_drift_can_generate_but_cannot_retrieve(self):
        upstream = graph.load_json(graph.INPUT.read_bytes())
        upstream['nodes'][0]['label'] = 'Public review candidate label'
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'input.json'
            target.write_text(json.dumps(upstream))
            # Keep canonical repository path independent of temporary IO location.
            with patch.object(graph, 'load_input_bytes', return_value=target.read_bytes()):
                candidate = graph.build()
            self.assertNotEqual(candidate['input']['sha256'], graph.INPUT_SHA256)
            with self.assertRaises(ValueError):
                graph.validate(candidate)

    def test_private_source_drift_cannot_generate(self):
        upstream = graph.load_json(graph.INPUT.read_bytes())
        upstream['nodes'][0]['label'] = 'https://drive.google.com/file/d/synthetic/view'
        with patch.object(graph, 'load_input_bytes', return_value=json.dumps(upstream).encode()):
            with self.assertRaises(ValueError):
                graph.build()

    def test_unknown_source_metadata_cannot_be_written(self):
        upstream = graph.load_json(graph.INPUT.read_bytes())
        upstream['nodes'][0]['unreviewed_metadata'] = 'unknown content'
        with patch.object(graph, 'load_input_bytes', return_value=json.dumps(upstream).encode()):
            with self.assertRaises(ValueError):
                graph.build()

    def test_drift_generation_requires_transitive_provenance_and_integrity(self):
        changes = [
            lambda d: d['source_artifacts'][0].update(sha256='a' * 64),
            lambda d: d['nodes'][0]['provenance'].update(sha256='b' * 64),
            lambda d: d['nodes'][1].update(node_id=d['nodes'][2]['node_id']),
            lambda d: d['edges'][0].update(target_node_id='node:missing'),
            lambda d: d['nodes'][0]['provenance'].update(record_locator='/models/0/model_id'),
            lambda d: d['edges'][0]['provenance'].update(record_locator='/missing'),
        ]
        for index, change in enumerate(changes):
            upstream = graph.load_json(graph.INPUT.read_bytes())
            change(upstream)
            with self.subTest(index=index), patch.object(graph, 'load_input_bytes', return_value=json.dumps(upstream).encode()):
                with self.assertRaises(ValueError):
                    graph.build()

    def test_nested_percent_encoding_never_emits_private_marker(self):
        private = 'https://drive.google.com/file/d/synthetic/view'
        for depth in (1, 5, 10, 40):
            value = ''.join(f'%{ord(character):02x}' for character in private)
            for _ in range(depth):
                value = quote(value, safe='')
            upstream = graph.load_json(graph.INPUT.read_bytes())
            upstream['nodes'][0]['label'] = value
            with self.subTest(depth=depth), patch.object(graph, 'load_input_bytes', return_value=json.dumps(upstream).encode()):
                with self.assertRaises(ValueError):
                    graph.build()

    def test_bounded_public_percent_encoding_is_still_allowed(self):
        graph.privacy_check({'label': 'Public%20review%20label'})


if __name__ == '__main__':
    unittest.main()
