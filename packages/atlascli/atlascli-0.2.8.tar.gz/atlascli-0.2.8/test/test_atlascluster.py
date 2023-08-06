import os
import unittest
import pprint
import random
import string

from atlascli.atlascluster import AtlasCluster
from atlascli.atlasapi import AtlasAPI
from atlascli.atlasorganization import AtlasOrganization


class TestAtlasCluster(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._org = AtlasOrganization()
        self._api = AtlasAPI()


    def test_get_clusters(self):
        clusters = list(self._api.get_clusters("5a141a774e65811a132a8010")) #Open Data Project
        self.assertTrue(len(clusters) > 0)

    def test_atlascluster(self):
        cluster = AtlasCluster(self._api, "5a141a774e65811a132a8010", AtlasCluster.default_single_region_cluster())

    def test_create_delete(self):
        cluster_dict = AtlasCluster.default_single_region_cluster()
        cluster_dict["name"] = AtlasAPI.random_name()
        created_cluster= self._api.create_cluster("5a141a774e65811a132a8010", cluster_dict)
        self._api.delete_cluster("5a141a774e65811a132a8010", created_cluster["name"])

    def test_modify(self):
        bi_on = {'biConnector': {'enabled': True, 'readPreference': 'secondary'}}
        self._api.modify_cluster(project_id="5a141a774e65811a132a8010",
                                 cluster_name="demodata",
                                 modifications=bi_on)

        cluster = self._api.get_one_cluster(project_id="5a141a774e65811a132a8010",
                                            cluster_name="demodata")

        #pprint.pprint(cluster)
        self.assertTrue( cluster['biConnector']["enabled"])
        bi_off = {'biConnector': {'enabled': False, 'readPreference': 'secondary'}}
        self._api.modify_cluster(project_id="5a141a774e65811a132a8010",
                                 cluster_name="demodata",
                                 modifications=bi_off)
        cluster = self._api.get_one_cluster(project_id="5a141a774e65811a132a8010",
                                            cluster_name="demodata")

        self.assertFalse( cluster['biConnector']["enabled"])

    def test_getcluster(self):
        clusters = self._org.get_cluster("GDELT")
        self.assertEqual(len(clusters), 1)

    def test_dumpload(self):
        clusters = self._org.get_cluster("GDELT")
        AtlasCluster.dump("gdelt.json", clusters[0].resource)
        new_cluster=AtlasCluster.load("gdelt.json")
        self.assertEqual(clusters[0].resource, new_cluster)
        os.unlink("gdelt.json")

if __name__ == '__main__':
    unittest.main()
