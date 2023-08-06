from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fsk:
	"""Fsk commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fsk", core, parent)

	# noinspection PyTypeChecker
	class BreateStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Limit: bool: OFF | ON Range: 0 to 100
			- Lower: int: Range: 0 to 100
			- Upper: int: Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Limit'),
			ArgStruct.scalar_int('Lower'),
			ArgStruct.scalar_int('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Limit: bool = None
			self.Lower: int = None
			self.Upper: int = None

	def get_breate(self) -> BreateStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DATA:LIMit:FSK:BREate \n
		Snippet: value: BreateStruct = driver.configure.afRf.measurement.data.limit.fsk.get_breate() \n
		Enables a limit check and sets the upper limit for the bit error rate. \n
			:return: structure: for return value, see the help for BreateStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DATA:LIMit:FSK:BREate?', self.__class__.BreateStruct())

	def set_breate(self, value: BreateStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DATA:LIMit:FSK:BREate \n
		Snippet: driver.configure.afRf.measurement.data.limit.fsk.set_breate(value = BreateStruct()) \n
		Enables a limit check and sets the upper limit for the bit error rate. \n
			:param value: see the help for BreateStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DATA:LIMit:FSK:BREate', value)
