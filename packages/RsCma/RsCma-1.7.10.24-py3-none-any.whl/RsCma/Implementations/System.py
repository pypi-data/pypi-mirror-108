from ..Internal.Core import Core
from ..Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class System:
	"""System commands group definition. 63 total commands, 9 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("system", core, parent)

	@property
	def base(self):
		"""base commands group. 10 Sub-classes, 5 commands."""
		if not hasattr(self, '_base'):
			from .System_.Base import Base
			self._base = Base(self._core, self._base)
		return self._base

	@property
	def deviceFootprint(self):
		"""deviceFootprint commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_deviceFootprint'):
			from .System_.DeviceFootprint import DeviceFootprint
			self._deviceFootprint = DeviceFootprint(self._core, self._base)
		return self._deviceFootprint

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .System_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	@property
	def error(self):
		"""error commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_error'):
			from .System_.Error import Error
			self._error = Error(self._core, self._base)
		return self._error

	@property
	def help(self):
		"""help commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_help'):
			from .System_.Help import Help
			self._help = Help(self._core, self._base)
		return self._help

	@property
	def update(self):
		"""update commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_update'):
			from .System_.Update import Update
			self._update = Update(self._core, self._base)
		return self._update

	@property
	def communicate(self):
		"""communicate commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_communicate'):
			from .System_.Communicate import Communicate
			self._communicate = Communicate(self._core, self._base)
		return self._communicate

	@property
	def option(self):
		"""option commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_option'):
			from .System_.Option import Option
			self._option = Option(self._core, self._base)
		return self._option

	@property
	def password(self):
		"""password commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_password'):
			from .System_.Password import Password
			self._password = Password(self._core, self._base)
		return self._password

	def preset(self) -> None:
		"""SCPI: SYSTem:PRESet \n
		Snippet: driver.system.preset() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		"""
		self._core.io.write(f'SYSTem:PRESet')

	def preset_with_opc(self) -> None:
		"""SCPI: SYSTem:PRESet \n
		Snippet: driver.system.preset_with_opc() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:PRESet')

	def preset_all(self) -> None:
		"""SCPI: SYSTem:PRESet:ALL \n
		Snippet: driver.system.preset_all() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		"""
		self._core.io.write(f'SYSTem:PRESet:ALL')

	def preset_all_with_opc(self) -> None:
		"""SCPI: SYSTem:PRESet:ALL \n
		Snippet: driver.system.preset_all_with_opc() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		Same as preset_all, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:PRESet:ALL')

	def preset_base(self) -> None:
		"""SCPI: SYSTem:PRESet:BASE \n
		Snippet: driver.system.preset_base() \n
		Presets or resets only the base settings, not the applications. \n
		"""
		self._core.io.write(f'SYSTem:PRESet:BASE')

	def preset_base_with_opc(self) -> None:
		"""SCPI: SYSTem:PRESet:BASE \n
		Snippet: driver.system.preset_base_with_opc() \n
		Presets or resets only the base settings, not the applications. \n
		Same as preset_base, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:PRESet:BASE')

	def reset(self) -> None:
		"""SCPI: SYSTem:RESet \n
		Snippet: driver.system.reset() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		"""
		self._core.io.write(f'SYSTem:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: SYSTem:RESet \n
		Snippet: driver.system.reset_with_opc() \n
		Presets or resets a selected application package in all scenarios. If <Application> is omitted, all applications are
		preset or reset. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:RESet')

	def reset_all(self) -> None:
		"""SCPI: SYSTem:RESet:ALL \n
		Snippet: driver.system.reset_all() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		"""
		self._core.io.write(f'SYSTem:RESet:ALL')

	def reset_all_with_opc(self) -> None:
		"""SCPI: SYSTem:RESet:ALL \n
		Snippet: driver.system.reset_all_with_opc() \n
		Presets or resets the base settings and all applications in all scenarios. \n
		Same as reset_all, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:RESet:ALL')

	def reset_base(self) -> None:
		"""SCPI: SYSTem:RESet:BASE \n
		Snippet: driver.system.reset_base() \n
		Presets or resets only the base settings, not the applications. \n
		"""
		self._core.io.write(f'SYSTem:RESet:BASE')

	def reset_base_with_opc(self) -> None:
		"""SCPI: SYSTem:RESet:BASE \n
		Snippet: driver.system.reset_base_with_opc() \n
		Presets or resets only the base settings, not the applications. \n
		Same as reset_base, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:RESet:BASE')

	def clone(self) -> 'System':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = System(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
