import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class USCrosswalkTest(unittest.TestCase):
    def test_references_and_scope(self):
        data = json.loads((ROOT/'docs/us-crosswalk.json').read_text())
        topics = {t['id'] for t in json.loads((ROOT/'data/topics.json').read_text())['topics']}
        seen = set()
        for row in data['records']:
            key = row['edition'], row['standard']
            self.assertNotIn(key, seen)
            seen.add(key)
            self.assertTrue(set(row['topicIds']) <= topics)
            self.assertIs(row['formalAssociationAuthored'], False)
            self.assertTrue(row['remainingConditions'])
            self.assertTrue(row['learnerEvidence'])
            self.assertTrue(row['sourceUrl'].startswith('https://'))
        density = next(r for r in data['records'] if r['standard']=='5-PS1-3')
        self.assertEqual(density['relationship'], 'assessment_exclusion')
        self.assertFalse(data['sourceTextIncluded'])
        self.assertEqual({r['edition'] for r in data['records'] if 'PRO-' in r['standard']}, {'2026'})
