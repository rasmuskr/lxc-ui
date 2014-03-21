import unittest
import tempfile
import subprocess
import shutil
import logging

import helpers

logger = logging.getLogger(__name__)


class TestLXCMocks(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        logger.debug("created temp directory %s", self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        logger.debug("removed temp directory %s", self.temp_dir)

    # ###########
    def test_raises_with_no_parameter(self):
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_ls, "")

    def test_empty_dir_returns_nothing(self):
        return_data = helpers.lxc_ls(self.temp_dir)
        self.assertEqual(return_data, "")

    def test_ls_syntax(self):
        __import__("lxc.test.mock_lxc_commands.lxc-ls")

    ############
    def test_create_container_shows_in_ls(self):
        helpers.lxc_create(self.temp_dir, "test1")
        helpers.lxc_create(self.temp_dir, "test2")

        return_data = helpers.lxc_ls(self.temp_dir)
        self.assertEqual(return_data, "test1\ntest2\n")

    def test_create_container_twice_raises(self):
        helpers.lxc_create(self.temp_dir, "test1")
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_create, self.temp_dir, "test1")

    def test_create_syntax(self):
        __import__("lxc.test.mock_lxc_commands.lxc-create")

    #################
    def test_destroy_container_does_not_show_in_ls(self):
        helpers.lxc_create(self.temp_dir, "test1")
        helpers.lxc_create(self.temp_dir, "test2")

        helpers.lxc_destroy(self.temp_dir, "test2")

        return_data = helpers.lxc_ls(self.temp_dir)
        self.assertEqual(return_data, "test1\n")

    def test_delete_non_existing_container_raises(self):
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_destroy, self.temp_dir, "test1")

    ##############
    def test_newly_created_container_info_gives_stopped(self):
        helpers.lxc_create(self.temp_dir, "test1")

        return_data = helpers.lxc_info(self.temp_dir, "test1")
        self.assertEqual(return_data, "state:   STOPPED\n")

    def test_info_non_existing_container_raises(self):
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_info, self.temp_dir, "test1")

    ##############
    def test_start_and_stop_container(self):
        helpers.lxc_create(self.temp_dir, "test1")

        helpers.lxc_start(self.temp_dir, "test1")

        return_data = helpers.lxc_info(self.temp_dir, "test1")
        self.assertEqual(return_data, "state:   RUNNING\n")

        helpers.lxc_stop(self.temp_dir, "test1")

        return_data = helpers.lxc_info(self.temp_dir, "test1")
        self.assertEqual(return_data, "state:   STOPPED\n")

    def test_start_already_started_raises(self):
        helpers.lxc_create(self.temp_dir, "test1")
        helpers.lxc_start(self.temp_dir, "test1")
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_start, self.temp_dir, "test1")

    def test_start_non_existing_raises(self):
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_start, self.temp_dir, "test1")

    def test_stop_already_stopped_raises(self):
        helpers.lxc_create(self.temp_dir, "test1")
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_stop, self.temp_dir, "test1")

    def test_stop_non_existing_raises(self):
        self.assertRaises(subprocess.CalledProcessError, helpers.lxc_stop, self.temp_dir, "test1")


if __name__ == '__main__':  # pragma: nocover
    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    unittest.main()