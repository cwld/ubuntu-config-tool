import yaml



class InstallConfig:
  PACKAGES_ROOT="packages"
  PACKAGES_INSTALL="install"
  PACKAGES_REMOVE="remove"
  
  FILES_ROOT="files"

  _config = {}

  def load_yaml(self, yaml_buffer):
    self._config = yaml.load(yaml_buffer,Loader=yaml.SafeLoader)
    # TODO: yaml structure validation

  def get_install_packages(self):
    if self.PACKAGES_ROOT in self._config and self.PACKAGES_INSTALL in self._config[self.PACKAGES_ROOT]:
      return self._config[self.PACKAGES_ROOT][self.PACKAGES_INSTALL]
    return []
  
  def get_remove_packages(self):
    if self.PACKAGES_ROOT in self._config and self.PACKAGES_REMOVE in self._config[self.PACKAGES_ROOT]:
      return self._config[self.PACKAGES_ROOT][self.PACKAGES_REMOVE]
    return []
