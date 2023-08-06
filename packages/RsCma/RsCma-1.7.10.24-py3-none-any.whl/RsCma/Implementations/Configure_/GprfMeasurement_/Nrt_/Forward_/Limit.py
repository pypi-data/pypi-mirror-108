from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Power: bool: OFF | ON
			- Pep: bool: OFF | ON
			- Crest_Factor: bool: OFF | ON
			- Ccdf: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Power'),
			ArgStruct.scalar_bool('Pep'),
			ArgStruct.scalar_bool('Crest_Factor'),
			ArgStruct.scalar_bool('Ccdf')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power: bool = None
			self.Pep: bool = None
			self.Crest_Factor: bool = None
			self.Ccdf: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.nrt.forward.limit.get_enable() \n
		Enables/disables the limit check for the forward direction results. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.set_enable(value = EnableStruct()) \n
		Enables/disables the limit check for the forward direction results. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:ENABle', value)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lower: float: Range: Depends on sensor model , Unit: dBm
			- Upper: float: Range: Depends on sensor model , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get_power(self) -> PowerStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:POWer \n
		Snippet: value: PowerStruct = driver.configure.gprfMeasurement.nrt.forward.limit.get_power() \n
		Configures limits for the forward power results. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:POWer \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.set_power(value = PowerStruct()) \n
		Configures limits for the forward power results. \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:POWer', value)

	# noinspection PyTypeChecker
	class PepStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lower: float: Range: Depends on sensor model , Unit: dBm
			- Upper: float: Range: Depends on sensor model , Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get_pep(self) -> PepStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP \n
		Snippet: value: PepStruct = driver.configure.gprfMeasurement.nrt.forward.limit.get_pep() \n
		Configures limits for the PEP results. \n
			:return: structure: for return value, see the help for PepStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP?', self.__class__.PepStruct())

	def set_pep(self, value: PepStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.set_pep(value = PepStruct()) \n
		Configures limits for the PEP results. \n
			:param value: see the help for PepStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:PEP', value)

	# noinspection PyTypeChecker
	class CfactorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lower: float: Range: 0 dB to 50 dB, Unit: dB
			- Upper: float: Range: 0 dB to 50 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get_cfactor(self) -> CfactorStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor \n
		Snippet: value: CfactorStruct = driver.configure.gprfMeasurement.nrt.forward.limit.get_cfactor() \n
		Configures limits for the crest factor results. \n
			:return: structure: for return value, see the help for CfactorStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor?', self.__class__.CfactorStruct())

	def set_cfactor(self, value: CfactorStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.set_cfactor(value = CfactorStruct()) \n
		Configures limits for the crest factor results. \n
			:param value: see the help for CfactorStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CFACtor', value)

	# noinspection PyTypeChecker
	class CumulativeDistribFncStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lower: float: Range: 0 % to 100 %, Unit: %
			- Upper: float: Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get_cumulative_distrib_fnc(self) -> CumulativeDistribFncStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF \n
		Snippet: value: CumulativeDistribFncStruct = driver.configure.gprfMeasurement.nrt.forward.limit.get_cumulative_distrib_fnc() \n
		Configures limits for the CCDF results. \n
			:return: structure: for return value, see the help for CumulativeDistribFncStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF?', self.__class__.CumulativeDistribFncStruct())

	def set_cumulative_distrib_fnc(self, value: CumulativeDistribFncStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF \n
		Snippet: driver.configure.gprfMeasurement.nrt.forward.limit.set_cumulative_distrib_fnc(value = CumulativeDistribFncStruct()) \n
		Configures limits for the CCDF results. \n
			:param value: see the help for CumulativeDistribFncStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:FWARd:LIMit:CCDF', value)
