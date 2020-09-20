import logging
from shutil import copyfile,chown
from os import chmod,path,stat
from stat import S_IMODE
from grp import getgrgid
from pwd import getpwuid
from hashlib import md5

## Class to copy files

class FileCopier:
  _files = []
  _files_modified = False

  def __init__(self, files):
    self._files = files

  def _calculate_md5(self, file_path):
    with open(file_path, "rb") as f:
      return md5(f.read()).hexdigest()

  def _convert_mode_to_int(self, mode):
    oct_str = '0o' + str(mode)
    return int(oct_str, 8)

  def _file_needs_update(self, file_config):
    if not path.exists(file_config.get_dest()):
      return True
    if self._calculate_md5(file_config.get_src()) != self._calculate_md5(file_config.get_dest()):
      return True
    dest_stat = stat(file_config.get_dest())
    if S_IMODE(dest_stat.st_mode) != self._convert_mode_to_int(file_config.get_mode()):
      return True
    dest_grp = getgrgid(dest_stat.st_gid) 
    if dest_grp.gr_name != file_config.get_group():
      return True
    dest_owner = getpwuid(dest_stat.st_uid)
    if dest_owner.pw_name != file_config.get_owner():
      return True

    return False

  def copy_files(self):
    for f in self._files:
      if self._file_needs_update(f):
        logging.info("Copying " + f.get_name())
        copyfile(f.get_src(), f.get_dest())
        chown(f.get_dest(), f.get_owner(), f.get_group())
        chmod(f.get_dest(), self._convert_mode_to_int(f.get_mode()))
        self._files_modified = True
      else:
        logging.info("File " + f.get_name() + " does not need updating, skipping")
      
    return True

  def files_modified(self):
    return self._files_modified
