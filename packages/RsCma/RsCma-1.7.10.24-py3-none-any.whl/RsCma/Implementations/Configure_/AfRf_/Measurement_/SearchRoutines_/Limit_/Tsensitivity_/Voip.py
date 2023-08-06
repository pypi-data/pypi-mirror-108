from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voip", core, parent)

	# noinspection PyTypeChecker
	class LevelStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Upper: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_level(self) -> LevelStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel \n
		Snippet: value: LevelStruct = driver.configure.afRf.measurement.searchRoutines.limit.tsensitivity.voip.get_level() \n
		No command help available \n
			:return: structure: for return value, see the help for LevelStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel?', self.__class__.LevelStruct())

	def set_level(self, value: LevelStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel \n
		Snippet: driver.configure.afRf.measurement.searchRoutines.limit.tsensitivity.voip.set_level(value = LevelStruct()) \n
		No command help available \n
			:param value: see the help for LevelStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SROutines:LIMit:TSENsitivity:VOIP:LEVel', value)
