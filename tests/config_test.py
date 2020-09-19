import unittest
from src.config import InstallConfig

class TestConfig(unittest.TestCase):

  def test_get_install_packages(self):
    test_yaml="""
---
packages:
  install:
    - nginx
    - vim
    - test
"""
    expected_packages = ["nginx","vim","test"]

    test_conf = InstallConfig()
    test_conf.load_yaml(test_yaml)
    packages = test_conf.get_install_packages()
    self.assertEqual(expected_packages, packages)

  def test_get_remove_packages(self):
    test_yaml="""
---
packages:
  remove:
    - nginx
    - vim
    - test
"""
    expected_packages = ["nginx","vim","test"]

    test_conf = InstallConfig()
    test_conf.load_yaml(test_yaml)
    packages = test_conf.get_remove_packages()
    self.assertEqual(expected_packages, packages)

