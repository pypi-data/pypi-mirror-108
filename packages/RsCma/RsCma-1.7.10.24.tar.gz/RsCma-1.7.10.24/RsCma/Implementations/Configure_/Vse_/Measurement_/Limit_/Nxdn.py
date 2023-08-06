from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nxdn:
	"""Nxdn commands group definition. 5 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nxdn", core, parent)

	@property
	def ffError(self):
		"""ffError commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ffError'):
			from .Nxdn_.FfError import FfError
			self._ffError = FfError(self._core, self._base)
		return self._ffError

	@property
	def merror(self):
		"""merror commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_merror'):
			from .Nxdn_.Merror import Merror
			self._merror = Merror(self._core, self._base)
		return self._merror

	# noinspection PyTypeChecker
	class FdErrorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON
			- Limit: float: Range: 0 Hz to 1 MHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Limit')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Limit: float = None

	def get_fd_error(self) -> FdErrorStruct:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor \n
		Snippet: value: FdErrorStruct = driver.configure.vse.measurement.limit.nxdn.get_fd_error() \n
		Enables/disables limit evaluation and sets the upper limit for the FSK deviation error. \n
			:return: structure: for return value, see the help for FdErrorStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor?', self.__class__.FdErrorStruct())

	def set_fd_error(self, value: FdErrorStruct) -> None:
		"""SCPI: CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor \n
		Snippet: driver.configure.vse.measurement.limit.nxdn.set_fd_error(value = FdErrorStruct()) \n
		Enables/disables limit evaluation and sets the upper limit for the FSK deviation error. \n
			:param value: see the help for FdErrorStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:VSE:MEASurement<Instance>:LIMit:NXDN:FDERor', value)

	def clone(self) -> 'Nxdn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nxdn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
