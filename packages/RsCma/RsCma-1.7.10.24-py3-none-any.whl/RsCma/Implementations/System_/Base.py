from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions
from ...Internal.Utilities import trim_str_response
from ...Internal.StructBase import StructBase
from ...Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Base:
	"""Base commands group definition. 25 total commands, 10 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("base", core, parent)

	@property
	def reference(self):
		"""reference commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_reference'):
			from .Base_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def gotsystem(self):
		"""gotsystem commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gotsystem'):
			from .Base_.Gotsystem import Gotsystem
			self._gotsystem = Gotsystem(self._core, self._base)
		return self._gotsystem

	@property
	def finish(self):
		"""finish commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_finish'):
			from .Base_.Finish import Finish
			self._finish = Finish(self._core, self._base)
		return self._finish

	@property
	def shutdown(self):
		"""shutdown commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_shutdown'):
			from .Base_.Shutdown import Shutdown
			self._shutdown = Shutdown(self._core, self._base)
		return self._shutdown

	@property
	def restart(self):
		"""restart commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_restart'):
			from .Base_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def device(self):
		"""device commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_device'):
			from .Base_.Device import Device
			self._device = Device(self._core, self._base)
		return self._device

	@property
	def time(self):
		"""time commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_time'):
			from .Base_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	@property
	def option(self):
		"""option commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_option'):
			from .Base_.Option import Option
			self._option = Option(self._core, self._base)
		return self._option

	@property
	def password(self):
		"""password commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_password'):
			from .Base_.Password import Password
			self._password = Password(self._core, self._base)
		return self._password

	@property
	def display(self):
		"""display commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_display'):
			from .Base_.Display import Display
			self._display = Display(self._core, self._base)
		return self._display

	def get_reliability(self) -> int:
		"""SCPI: SYSTem:BASE:RELiability \n
		Snippet: value: int = driver.system.base.get_reliability() \n
		Returns a reliability value, indicating errors detected by the base software. \n
			:return: value: See 'Reliability Indicator'
		"""
		response = self._core.io.query_str('SYSTem:BASE:RELiability?')
		return Conversions.str_to_int(response)

	def get_did(self) -> str:
		"""SCPI: SYSTem:BASE:DID \n
		Snippet: value: str = driver.system.base.get_did() \n
		No command help available \n
			:return: device_id: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:DID?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	class DateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Year: int: No parameter help available
			- Month: int: No parameter help available
			- Day: int: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_int('Year'),
			ArgStruct.scalar_int('Month'),
			ArgStruct.scalar_int('Day')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Year: int = None
			self.Month: int = None
			self.Day: int = None

	def get_date(self) -> DateStruct:
		"""SCPI: SYSTem:BASE:DATE \n
		Snippet: value: DateStruct = driver.system.base.get_date() \n
		No command help available \n
			:return: structure: for return value, see the help for DateStruct structure arguments.
		"""
		return self._core.io.query_struct('SYSTem:BASE:DATE?', self.__class__.DateStruct())

	def set_date(self, value: DateStruct) -> None:
		"""SCPI: SYSTem:BASE:DATE \n
		Snippet: driver.system.base.set_date(value = DateStruct()) \n
		No command help available \n
			:param value: see the help for DateStruct structure arguments.
		"""
		self._core.io.write_struct('SYSTem:BASE:DATE', value)

	def get_klock(self) -> bool:
		"""SCPI: SYSTem:BASE:KLOCk \n
		Snippet: value: bool = driver.system.base.get_klock() \n
		No command help available \n
			:return: klock: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:KLOCk?')
		return Conversions.str_to_bool(response)

	def set_klock(self, klock: bool) -> None:
		"""SCPI: SYSTem:BASE:KLOCk \n
		Snippet: driver.system.base.set_klock(klock = False) \n
		No command help available \n
			:param klock: No help available
		"""
		param = Conversions.bool_to_str(klock)
		self._core.io.write(f'SYSTem:BASE:KLOCk {param}')

	def get_version(self) -> float:
		"""SCPI: SYSTem:BASE:VERSion \n
		Snippet: value: float = driver.system.base.get_version() \n
		No command help available \n
			:return: version: No help available
		"""
		response = self._core.io.query_str('SYSTem:BASE:VERSion?')
		return Conversions.str_to_float(response)

	def clone(self) -> 'Base':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Base(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
