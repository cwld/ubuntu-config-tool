import apt
import logging

## Class for installing and removing apt packages

class PackageInstaller:
  _cache = {}
  _install_list = []
  _remove_list = []
  _packages_modified = False

  def __init__(self, install_list, remove_list):
    self._install_list = install_list
    self._remove_list = remove_list
    self._cache = apt.cache.Cache()
    self._cache.update()
    self._cache.open()
  
  def install_remove_packages(self):
    for pkg_name in self._install_list:
      if pkg_name not in self._cache:
        logging.info("Package " + pkg_name + " not found!")
        return False

      pkg = self._cache[pkg_name]
      if not pkg.is_installed:
        logging.info("Marking package " + pkg_name + " for install")
        self._packages_modified = True
        pkg.mark_install()
      else:
        logging.info("Package " + pkg_name + " already installed")

    for pkg_name in self._remove_list:
      if pkg_name not in self._cache:
        logging.info("Package " + pkg_name + " not found!")
        return False

      pkg = self._cache[pkg_name]
      if pkg.is_installed:
        logging.info("Marking package " + pkg_name + " for removal")
        self._packages_modified = True
        pkg.mark_delete()
      else:
        logging.info("Package " + pkg_name + " already removed")

    try:
      if self._packages_modified:
        self._cache.commit()
    except Exception as e:
      logging.info("Package installation failed: " + e.message)
      return False

    return True

  def packages_modified(self):
    return self._packages_modified
