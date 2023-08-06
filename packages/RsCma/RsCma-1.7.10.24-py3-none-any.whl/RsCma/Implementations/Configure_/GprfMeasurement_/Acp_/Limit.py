from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Limit:
	"""Limit commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("limit", core, parent)

	@property
	def obw(self):
		"""obw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_obw'):
			from .Limit_.Obw import Obw
			self._obw = Obw(self._core, self._base)
		return self._obw

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Ch_0: bool: OFF | ON Absolute power limit checks for the designated channel '0'
			- Enable_Ch_1: bool: OFF | ON ACLR limit check for the neighbor channels '+1' and '-1'
			- Enable_Ch_2: bool: OFF | ON ACLR limit check for the neighbor channels '+2' and '-2'"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Ch_0'),
			ArgStruct.scalar_bool('Enable_Ch_1'),
			ArgStruct.scalar_bool('Enable_Ch_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Ch_0: bool = None
			self.Enable_Ch_1: bool = None
			self.Enable_Ch_2: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle \n
		Snippet: value: EnableStruct = driver.configure.gprfMeasurement.acp.limit.get_enable() \n
		Enables or disables the ACLR and power limit checks. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.set_enable(value = EnableStruct()) \n
		Enables or disables the ACLR and power limit checks. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ENABle', value)

	# noinspection PyTypeChecker
	class AclrStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit_Ch_1: float: Upper ACLR limit for the channels '+1' and '-1' Range: -80 dB to 10 dB, Unit: dB
			- Limit_Ch_2: float: Upper ACLR limit for the channels '+2' and '-2' Range: -80 dB to 10 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_float('Limit_Ch_1'),
			ArgStruct.scalar_float('Limit_Ch_2')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit_Ch_1: float = None
			self.Limit_Ch_2: float = None

	def get_aclr(self) -> AclrStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR \n
		Snippet: value: AclrStruct = driver.configure.gprfMeasurement.acp.limit.get_aclr() \n
		Configures upper limits for the measured ACLR values. \n
			:return: structure: for return value, see the help for AclrStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR?', self.__class__.AclrStruct())

	def set_aclr(self, value: AclrStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.set_aclr(value = AclrStruct()) \n
		Configures upper limits for the measured ACLR values. \n
			:param value: see the help for AclrStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:ACLR', value)

	# noinspection PyTypeChecker
	class PowerStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Limit_Lower: float: Lower power limit Range: -130 dBm to 55 dBm, Unit: dBm
			- Limit_Upper: float: Upper power limit Range: -130 dBm to 55 dBm, Unit: dBm"""
		__meta_args_list = [
			ArgStruct.scalar_float('Limit_Lower'),
			ArgStruct.scalar_float('Limit_Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Limit_Lower: float = None
			self.Limit_Upper: float = None

	def get_power(self) -> PowerStruct:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer \n
		Snippet: value: PowerStruct = driver.configure.gprfMeasurement.acp.limit.get_power() \n
		Configures limits for the absolute power measured in the designated channel. \n
			:return: structure: for return value, see the help for PowerStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer?', self.__class__.PowerStruct())

	def set_power(self, value: PowerStruct) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer \n
		Snippet: driver.configure.gprfMeasurement.acp.limit.set_power(value = PowerStruct()) \n
		Configures limits for the absolute power measured in the designated channel. \n
			:param value: see the help for PowerStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:GPRF:MEASurement<Instance>:ACP:LIMit:POWer', value)

	def clone(self) -> 'Limit':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Limit(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
