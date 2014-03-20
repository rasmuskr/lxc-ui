import unittest

import logging

logger = logging.getLogger(__name__)

import helpers


class TestLXCContainers(unittest.TestCase):
    def setUp(self):
        self.containers = helpers.get_containers_with_mock_binaries()

    def tearDown(self):
        helpers.cleanup_containers_with_mock_binaries(self.containers)

    # ############
    def test_create_and_delete_container(self):
        container_name = "test_container_1"
        group_name = "test_group_1"
        self.containers.create_container(container_name, group_name, "ubuntu")
        containers = self.containers.list_containers(group_name)

        self.assertIn(container_name, containers)

        self.containers.delete_container(container_name, group_name)
        containers = self.containers.list_containers(group_name)
        self.assertNotIn(container_name, containers)

    def test_start_stop_container(self):
        container_name = "test_container_1"
        group_name = "test_group_1"
        self.containers.create_container(container_name, group_name, "ubuntu")
        container_status = self.containers.container_status(container_name, group_name)
        self.assertIn("state", container_status)
        self.assertEqual(container_status["state"], "STOPPED")

        self.containers.start_container(container_name, group_name)
        container_status = self.containers.container_status(container_name, group_name)
        self.assertIn("state", container_status)
        self.assertEqual(container_status["state"], "RUNNING")

        self.containers.stop_container(container_name, group_name)
        container_status = self.containers.container_status(container_name, group_name)
        self.assertIn("state", container_status)
        self.assertEqual(container_status["state"], "STOPPED")

    def test_get_groups(self):
        container_name = "test_container_1"
        group_name1 = "test_group_1"
        self.containers.create_container(container_name, group_name1, "ubuntu")

        group_name2 = "test_group_2"
        self.containers.create_container(container_name, group_name2, "ubuntu")

        return_data = self.containers.list_groups()
        self.assertIs(list, type(return_data))

        self.assertEqual(len(return_data), 2)
        self.assertIn(group_name1, return_data)
        self.assertIn(group_name2, return_data)


if __name__ == '__main__':
    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    unittest.main()