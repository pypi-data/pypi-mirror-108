from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 26 total commands, 3 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdif", core, parent)

	@property
	def level(self):
		"""level commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_level'):
			from .Spdif_.Level import Level
			self._level = Level(self._core, self._base)
		return self._level

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Spdif_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 6 commands."""
		if not hasattr(self, '_filterPy'):
			from .Spdif_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Test_Left: bool: OFF | ON Switches the left channel off or on
			- Test_Right: bool: OFF | ON Switches the right channel off or on"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Test_Left'),
			ArgStruct.scalar_bool('Test_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Test_Left: bool = None
			self.Test_Right: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.spdif.get_enable() \n
		Enables or disables the channels of the SPDIF IN connector. \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:ENABle \n
		Snippet: driver.configure.afRf.measurement.spdif.set_enable(value = EnableStruct()) \n
		Enables or disables the channels of the SPDIF IN connector. \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:ENABle', value)

	# noinspection PyTypeChecker
	class GcouplingStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Coupling_Left: enums.GeneratorCoupling: OFF | GEN1 | GEN3 OFF No coupling of left channel GENn Left channel coupled to audio generator n
			- Coupling_Right: enums.GeneratorCoupling: OFF | GEN2 | GEN4 OFF No coupling of right channel GENn Right channel coupled to audio generator n"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Coupling_Left', enums.GeneratorCoupling),
			ArgStruct.scalar_enum('Coupling_Right', enums.GeneratorCoupling)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Coupling_Left: enums.GeneratorCoupling = None
			self.Coupling_Right: enums.GeneratorCoupling = None

	# noinspection PyTypeChecker
	def get_gcoupling(self) -> GcouplingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling \n
		Snippet: value: GcouplingStruct = driver.configure.afRf.measurement.spdif.get_gcoupling() \n
		Couples the channels of the SPDIF IN connector to an internal signal generator. The combinations GEN1+GEN4 and GEN3+GEN2
		are not allowed. \n
			:return: structure: for return value, see the help for GcouplingStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling?', self.__class__.GcouplingStruct())

	def set_gcoupling(self, value: GcouplingStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling \n
		Snippet: driver.configure.afRf.measurement.spdif.set_gcoupling(value = GcouplingStruct()) \n
		Couples the channels of the SPDIF IN connector to an internal signal generator. The combinations GEN1+GEN4 and GEN3+GEN2
		are not allowed. \n
			:param value: see the help for GcouplingStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:GCOupling', value)

	# noinspection PyTypeChecker
	class TmodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Tone_Mode_Left: enums.ToneMode: No parameter help available
			- Tone_Mode_Right: enums.DigitalToneMode: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Tone_Mode_Left', enums.ToneMode),
			ArgStruct.scalar_enum('Tone_Mode_Right', enums.DigitalToneMode)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tone_Mode_Left: enums.ToneMode = None
			self.Tone_Mode_Right: enums.DigitalToneMode = None

	# noinspection PyTypeChecker
	def get_tmode(self) -> TmodeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:TMODe \n
		Snippet: value: TmodeStruct = driver.configure.afRf.measurement.spdif.get_tmode() \n
		No command help available \n
			:return: structure: for return value, see the help for TmodeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:TMODe?', self.__class__.TmodeStruct())

	def set_tmode(self, value: TmodeStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:SIN:TMODe \n
		Snippet: driver.configure.afRf.measurement.spdif.set_tmode(value = TmodeStruct()) \n
		No command help available \n
			:param value: see the help for TmodeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:SIN:TMODe', value)

	def clone(self) -> 'Spdif':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Spdif(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
