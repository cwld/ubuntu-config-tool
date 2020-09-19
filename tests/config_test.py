import unittest
from src.config import InstallConfig,FileCopyConfig


class TestConfig(unittest.TestCase):
  def compare_file_copy_config(self, file1, file2, msg=None):
    if file1.get_name() != file2.get_name():
      raise self.failureException(msg)
    if file1.get_src() != file2.get_src():
      raise self.failureException(msg)
    if file1.get_dest() != file2.get_dest():
      raise self.failureException(msg)
    if file1.get_restart() != file2.get_restart():
      raise self.failureException(msg)
    if file1.get_owner() != file2.get_owner():
      raise self.failureException(msg)
    if file1.get_group() != file2.get_group():
      raise self.failureException(msg)
    if file1.get_mode() != file2.get_mode():
      raise self.failureException(msg)
    
 
  def setUp(self):
    self.addTypeEqualityFunc(FileCopyConfig, self.compare_file_copy_config)

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

    test_conf = InstallConfig(test_yaml)
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

    test_conf = InstallConfig(test_yaml)
    packages = test_conf.get_remove_packages()
    self.assertEqual(expected_packages, packages)

  def test_get_files(self):
    test_yaml="""
---
files:
  - test_name_1:
      source: app/test.txt
      destination: /opt/test.txt
      requiresRestart: true
      access:
        owner: user1
        group: group1
        mode: 640
  - test_name_2:
      source: app/alt
      destination: /usr/share/alt
      requiresRestart: false
      access:
        owner: user2
        group: group2
        mode: 777
"""
    expected_file_1 = FileCopyConfig("test_name_1",
      {"source":"app/test.txt","destination":"/opt/test.txt","requiresRestart": True, "access":
        {"owner":"user1","group":"group1","mode":640
        }
      })
    expected_file_2 = FileCopyConfig("test_name_2",
      {"source":"app/alt","destination":"/usr/share/alt","requiresRestart": False, "access":
        {"owner":"user2","group":"group2","mode":777
        }
      })

    test_conf = InstallConfig(test_yaml)
    files = test_conf.get_files()
    self.assertEqual(2, len(files))
    self.assertEqual(expected_file_1, files[0])
    self.assertEqual(expected_file_2, files[1])

  def test_get_service(self):
    test_yaml="""
---
service:
  startCommand: 'service test start'
  restartCommand: 'service test restart'
"""
    test_conf = InstallConfig(test_yaml)
    expected_start_cmd='service test start'
    expected_restart_cmd='service test restart'
    
    start_cmd=test_conf.get_start_cmd()
    restart_cmd=test_conf.get_restart_cmd()

    self.assertEqual(expected_start_cmd, start_cmd)
    self.assertEqual(expected_restart_cmd, restart_cmd)
