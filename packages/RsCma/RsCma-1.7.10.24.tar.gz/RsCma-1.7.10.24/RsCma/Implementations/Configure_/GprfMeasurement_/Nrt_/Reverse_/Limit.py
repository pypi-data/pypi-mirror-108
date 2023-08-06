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
			- Return_Loss: bool: OFF | ON
			- Reflection: bool: OFF | ON
			- Swr: bool: OFF | ON"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Power'),
			ArgStruct.scalar_bool('Return_Loss'),
			ArgStruct.scalar_bool('Reflection'),
			ArgStruct.scalar_bool('Swr')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Power: bool = None
			self.Return_Loss: bool = None
			self.Reflection: bool = None
			self.Swr: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.get_enable() \n
		Enables/disables the limit check for the reverse direction results. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.set_enable(value = EnableStruct()) \n
		Enables/disables the limit check for the reverse direction results. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:ENABle', value)

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
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:POWer \n
		Snippet: value: PowerStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.get_power() \n
		Configures limits for the reverse power results. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:POWer \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.set_power(value = PowerStruct()) \n
		Configures limits for the reverse power results. \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:POWer', value)

	# noinspection PyTypeChecker
	class RlossStruct(StructBase):
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

	def get_rloss(self) -> RlossStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:RLOSs \n
		Snippet: value: RlossStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.get_rloss() \n
		Configures limits for the return loss results. \n
			:return: structure: for return value, see the help for RlossStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:RLOSs?', self.__class__.RlossStruct())

	def set_rloss(self, value: RlossStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:RLOSs \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.set_rloss(value = RlossStruct()) \n
		Configures limits for the return loss results. \n
			:param value: see the help for RlossStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:RLOSs', value)

	# noinspection PyTypeChecker
	class ReflectionStruct(StructBase):
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

	def get_reflection(self) -> ReflectionStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:REFLection \n
		Snippet: value: ReflectionStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.get_reflection() \n
		Configures limits for the reflection results. \n
			:return: structure: for return value, see the help for ReflectionStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:REFLection?', self.__class__.ReflectionStruct())

	def set_reflection(self, value: ReflectionStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:REFLection \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.set_reflection(value = ReflectionStruct()) \n
		Configures limits for the reflection results. \n
			:param value: see the help for ReflectionStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:REFLection', value)

	# noinspection PyTypeChecker
	class SwrStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lower: float: Range: 1 to 50
			- Upper: float: Range: 1 to 50"""
		__meta_args_list = [
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lower: float = None
			self.Upper: float = None

	def get_swr(self) -> SwrStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR \n
		Snippet: value: SwrStruct = driver.configure.gprfMeasurement.nrt.reverse.limit.get_swr() \n
		Configures limits for the SWR results. \n
			:return: structure: for return value, see the help for SwrStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR?', self.__class__.SwrStruct())

	def set_swr(self, value: SwrStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR \n
		Snippet: driver.configure.gprfMeasurement.nrt.reverse.limit.set_swr(value = SwrStruct()) \n
		Configures limits for the SWR results. \n
			:param value: see the help for SwrStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:NRT:REVerse:LIMit:SWR', value)
