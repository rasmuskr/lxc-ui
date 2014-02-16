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
        self.app.testing = True
        token = "test-Token"

        self.app.application.config["lxc_ui_agent_config"] = {}
        self.app.application.config["lxc_ui_agent_config"]["expected_token"] = token
        self.headers = {
            "Authorization": "Bearer %s" % (token, ),
        }

    def _get_groups(self):
        rv = self.app.get("/groups/", headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        return_data = json.loads(rv.data)
        self.assertIn("groups", return_data)
        self.assertIs(list, type(return_data["groups"]))
        return return_data

    def _get_containers(self, group_name):
        rv = self.app.get("/groups/%s/containers/" % (group_name, ), headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        return_data = json.loads(rv.data)
        logger.debug("Getting list of containers: '%s' status:'%s'", return_data, rv.status_code)
        self.assertIn("containers", return_data)
        return return_data

    def _create_container(self, group_name, container_name):
        return_data = self._get_containers(group_name)

        if container_name in return_data["containers"]:
            logger.debug("container '%s' already existing... deleting", container_name)
            self._delete_container(group_name, container_name)

        data = {
            "container_name": container_name
        }
        rv = self.app.post("/groups/%s/containers/" % (group_name, ), data=json.dumps(data), headers=self.headers)
        logger.debug("created container '%s' status:'%s'", container_name, rv.status_code)
        self.assertEqual(rv.status_code, 201)

    def _delete_container(self, group_name, container_name):
        self._stop_container(group_name, container_name)
        rv = self.app.delete("/groups/%s/containers/%s/" % (group_name, container_name, ), headers=self.headers)
        self.assertEqual(rv.status_code, 201)

    def _get_container_info(self, group_name, container_name):
        rv = self.app.get("/groups/%s/containers/%s/" % (group_name, container_name, ), headers=self.headers)
        self.assertEqual(rv.status_code, 200)
        return_data = json.loads(rv.data)
        return return_data

    def _start_container(self, group_name, container_name):
        data = {
            "state": "RUNNING",
        }
        rv = self.app.patch("/groups/%s/containers/%s/" % (group_name, container_name, ),
                            data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status_code, 200)

        return_data = self._get_container_info(group_name, container_name)
        self.assertEqual(return_data["state"], "RUNNING")


    def _stop_container(self, group_name, container_name):
        data = {
            "state": "STOPPED",
        }
        rv = self.app.patch("/groups/%s/containers/%s/" % (group_name, container_name, ),
                            data=json.dumps(data), headers=self.headers)
        self.assertEqual(rv.status_code, 200)

        return_data = self._get_container_info(group_name, container_name)
        self.assertEqual(return_data["state"], "STOPPED")

    ########################################################################################
    def test_groups(self):
        return_data = self._get_groups()
        self.assertIn("groups", return_data)
        self.assertIs(list, type(return_data["groups"]))

    ########################################################################################
    def test_get_containers(self):
        return_data = self._get_containers("test-group")
        self.assertIs(list, type(return_data["containers"]))

    ########################################################################################
    def test_create_delete_container(self):
        new_container_name = "test_container"
        group_name = "test-group"
        self._create_container(group_name, new_container_name)
        return_data = self._get_containers(group_name)
        self.assertIn(new_container_name, return_data["containers"])

        self._delete_container(group_name, new_container_name)
        return_data = self._get_containers(group_name)
        self.assertIn("containers", return_data)
        self.assertNotIn(new_container_name, return_data["containers"])


    def test_stop_start_container(self):
        new_container_name = "test_container"
        group_name = "test-group"
        self._create_container(group_name, new_container_name)
        return_data = self._get_containers(group_name)
        self.assertIn(new_container_name, return_data["containers"])

        self._start_container(group_name, new_container_name)

        self._stop_container(group_name, new_container_name)

        # cleanup from test
        self._delete_container(group_name, new_container_name)


if __name__ == '__main__':
    unittest.main()