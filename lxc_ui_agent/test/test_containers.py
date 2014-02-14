import unittest
import json
import logging

import lxc_ui_agent.lxc_ui_agent


logging.root.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.root.addHandler(handler)

logger = logging.getLogger(__name__)


class TestContainers(unittest.TestCase):
    def setUp(self):
        self.app = lxc_ui_agent.lxc_ui_agent.app.test_client()

        token = "test-Token"

        self.app.application.config["lxc_ui_agent_config"] = {}
        self.app.application.config["lxc_ui_agent_config"]["expected_token"] = token
        self.headers = {
            "Authorization": "Bearer %s" % (token, ),
        }

    def test_groups(self):
        rv = self.app.get("/groups/", headers=self.headers)
        return_data = json.loads(rv.data)
        self.assertIn("groups", return_data)
        self.assertIs(list, type(return_data["groups"]))

    def test_get_containers(self):
        rv = self.app.get("/groups/test-group/containers/", headers=self.headers)
        return_data = json.loads(rv.data)
        self.assertIn("containers", return_data)
        self.assertIs(list, type(return_data["containers"]))

    def test_create_delete_container(self):
        new_container_name = "test_container"
        group_name = "test-group"

        # delete the first container if it exists, to make sure failed tests does not fail
        rv = self.app.get("/groups/%s/containers/" % (group_name, ), headers=self.headers)
        self.assertEqual(rv.status_code, 200)

        return_data = json.loads(rv.data)
        if new_container_name in return_data["containers"]:
            logger.debug("container '%s' already existing... deleting", new_container_name)
            rv = self.app.delete("/groups/%s/containers/%s/" % (group_name, new_container_name, ), headers=self.headers)

        data = {
            "container_name": new_container_name
        }
        rv = self.app.post("/groups/%s/containers/" % (group_name, ), data=json.dumps(data), headers=self.headers)
        logger.debug("created container '%s' status:'%s'", new_container_name, rv.status_code)
        self.assertEqual(rv.status_code, 201)

        rv = self.app.get("/groups/%s/containers/" % (group_name, ), headers=self.headers)
        return_data = json.loads(rv.data)
        logger.debug("Getting list of containers: '%s' status:'%s'", return_data, rv.status_code)
        self.assertIn("containers", return_data)
        self.assertIn(new_container_name, return_data["containers"])

        rv = self.app.delete("/groups/%s/containers/%s/" % (group_name, new_container_name, ), headers=self.headers)
        self.assertEqual(rv.status_code, 200)

        rv = self.app.get("/groups/%s/containers/" % (group_name, ), headers=self.headers)
        return_data = json.loads(rv.data)
        logger.debug("Getting list of containers: '%s' status:'%s'", return_data, rv.status_code)
        self.assertIn("containers", return_data)
        self.assertNotIn(new_container_name, return_data["containers"])


if __name__ == '__main__':
    unittest.main()