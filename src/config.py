import yaml

class FileCopyConfig:
  FILE_ACCESS_ROOT="access"
  FILE_ACCESS_OWNER="owner"
  FILE_ACCESS_GROUP="group"
  FILE_ACCESS_MODE="mode"
  FILE_SRC="source"
  FILE_DEST="destination"
  FILE_RESTART="requiresRestart"

  _mode = 0
  _owner = ""
  _group = ""
  _src = ""
  _dest = ""
  _name = ""
  _requiresRestart = False
  
  def __init__(self, name, file_config):
    self._name=name
    self._src=file_config[self.FILE_SRC]
    self._dest=file_config[self.FILE_DEST]
    self._requiresRestart=file_config[self.FILE_RESTART]
    self._owner=file_config[self.FILE_ACCESS_ROOT][self.FILE_ACCESS_OWNER]
    self._mode=file_config[self.FILE_ACCESS_ROOT][self.FILE_ACCESS_MODE]
    self._group=file_config[self.FILE_ACCESS_ROOT][self.FILE_ACCESS_GROUP]

  def get_name(self):
    return self._name
  
  def get_src(self):
    return self._src

  def get_dest(self):
    return self._dest

  def get_restart(self):
    return self._requiresRestart

  def get_mode(self):
    return self._mode

  def get_group(self):
    return self._group

  def get_owner(self):
    return self._owner

class InstallConfig:
  PACKAGES_ROOT="packages"
  PACKAGES_INSTALL="install"
  PACKAGES_REMOVE="remove"
  
  FILES_ROOT="files"

  SERVICE_ROOT="service"
  SERVICE_RESTART="restartCommand"
  SERVICE_START="startCommand"

  _packages_install = []
  _packages_remove = []
  _files = []
  _restart_cmd=""
  _start_cmd=""

  def __init__(self, yaml_buffer):
    config = yaml.load(yaml_buffer,Loader=yaml.SafeLoader)
    if self.PACKAGES_ROOT in config and self.PACKAGES_INSTALL in config[self.PACKAGES_ROOT]:
      self._packages_install = config[self.PACKAGES_ROOT][self.PACKAGES_INSTALL]

    if self.PACKAGES_ROOT in config and self.PACKAGES_REMOVE in config[self.PACKAGES_ROOT]:
      self._packages_remove = config[self.PACKAGES_ROOT][self.PACKAGES_REMOVE]

    if self.FILES_ROOT in config:
      for f in config[self.FILES_ROOT]:
        name=list(f)[0]
        self._files.append(FileCopyConfig(name, f[name]))

    if self.SERVICE_ROOT in config:
      self._restart_cmd=config[self.SERVICE_ROOT][self.SERVICE_RESTART]
      self._start_cmd=config[self.SERVICE_ROOT][self.SERVICE_START]

    #TODO validate yaml structure

  def get_install_packages(self):
    return self._packages_install
  
  def get_remove_packages(self):
    return self._packages_remove

  def get_files(self):
    return self._files

  def get_restart_cmd(self):
    return self._restart_cmd
  
  def get_start_cmd(self):
    return self._start_cmd
