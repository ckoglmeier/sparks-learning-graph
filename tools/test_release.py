# SPDX-License-Identifier: MIT
import copy,json,pathlib,tempfile,unittest
from verify_release import ROOT,read_graph,check_graph,check_inventory,sha,check_boundary

class GraphMutations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.g=read_graph(ROOT)
    def changed(self,key):
        g=self.g.copy();g[key]=copy.deepcopy(g[key]);return g
    def test_real_graph(self):check_graph(self.g)
    def test_duplicate_id(self):
        g=self.changed('topics');g['topics']['topics'].append(g['topics']['topics'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate topic'):check_graph(g)
    def test_dangling_edge(self):
        g=self.changed('dependencies');g['dependencies']['dependencies'][0]['prerequisiteId']='mt_missing'
        with self.assertRaisesRegex(ValueError,'Dangling prerequisite'):check_graph(g)
    def test_cycle(self):
        g=self.changed('dependencies');e=g['dependencies']['dependencies'][0]
        g['dependencies']['dependencies'].append({'topicId':e['prerequisiteId'],'prerequisiteId':e['topicId'],'strength':'soft'})
        with self.assertRaisesRegex(ValueError,'Dependency cycle'):check_graph(g)
    def test_bad_citation(self):
        g=self.g.copy();collection=self.g['teaching-research'].copy();records=list(collection['records']);records[0]=copy.deepcopy(records[0]);records[0]['learn']['activities'][0]['sourceIds']=['citation_missing'];collection['records']=records;g['teaching-research']=collection
        with self.assertRaisesRegex(ValueError,'Dangling activity source'):check_graph(g)
    def test_restricted_wording(self):
        g=self.changed('curriculum-standards')
        c=next(c for c in g['curriculum-standards']['curricula'] if not c['textIncluded']);c['topics'][0]['data']={'description':'synthetic forbidden wording'}
        with self.assertRaisesRegex(ValueError,'Restricted curriculum text'):check_graph(g)
    def test_public_catalogue_is_identifiers_only(self):
        catalog=self.g['curriculum-standards']
        self.assertEqual(set(catalog['codesOnlySources']), {c['slug'] for c in catalog['curricula']})
        for source in catalog['curricula']:
            self.assertFalse(source['textIncluded'])
            for row in source['topics']: self.assertEqual(set(row), {'key','code'})
    def test_count_mismatch(self):
        g=self.changed('manifest');g['manifest']['counts']['topics']+=1
        with self.assertRaisesRegex(ValueError,'Manifest count'):check_graph(g)

class InventoryMutations(unittest.TestCase):
    def test_tamper_and_unlisted_file(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);(root/'a.json').write_bytes(b'{}')
            (root/'RELEASE-MANIFEST.json').write_text(json.dumps({'files':[{'path':'a.json','bytes':2,'sha256':sha(b'{}')}]}))
            check_inventory(root)
            (root/'a.json').write_bytes(b'[]')
            with self.assertRaisesRegex(ValueError,'checksum'):check_inventory(root)
            (root/'a.json').write_bytes(b'{}');(root/'paths.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'Inventory mismatch'):check_inventory(root)
    def test_product_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=pathlib.Path(d);(root/'paths.json').write_text('{}')
            with self.assertRaisesRegex(ValueError,'Product-only'):check_boundary(root)

if __name__=='__main__':unittest.main()
