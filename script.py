import sys
import logging
from typing import Optional
from collections.abc import Sequence
import subprocess

from mitmproxy import ctx

log = logging.getLogger(__name__)

class PIPInstaller:
  def __init__(self):
    self.__package_list = set()

  def __package_installation(self):
    if not self.__package_list:
      return

    log.info('Installing %d packages.', len(self.__package_list))
    subprocess.check_call([
      sys.executable, '-m', 'pip', 'install',
      '--',
      *self.__package_list,
    ])

  def load(self, loader):
    loader.add_option(
      name='extra_packages',
      typespec=Sequence[str],
      default=[],
      help='Installs extra packages to the environment.',
    )

  def configure(self, updates):
    if 'extra_packages' not in updates:
      return

    self.__package_list.update(ctx.options.extra_packages)
    self.__package_installation()

addons = [PIPInstaller()]
