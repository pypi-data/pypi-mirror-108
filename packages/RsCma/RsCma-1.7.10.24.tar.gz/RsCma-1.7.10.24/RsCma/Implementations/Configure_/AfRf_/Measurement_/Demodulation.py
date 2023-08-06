from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 35 total commands, 5 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodulation", core, parent)

	@property
	def frequency(self):
		"""frequency commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_frequency'):
			from .Demodulation_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def fmStereo(self):
		"""fmStereo commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fmStereo'):
			from .Demodulation_.FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._base)
		return self._fmStereo

	@property
	def modDepth(self):
		"""modDepth commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_modDepth'):
			from .Demodulation_.ModDepth import ModDepth
			self._modDepth = ModDepth(self._core, self._base)
		return self._modDepth

	@property
	def fdeviation(self):
		"""fdeviation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Demodulation_.Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._base)
		return self._fdeviation

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 8 commands."""
		if not hasattr(self, '_filterPy'):
			from .Demodulation_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	# noinspection PyTypeChecker
	class EnableStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Test_Left: bool: No parameter help available
			- Test_Right: bool: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Test_Left'),
			ArgStruct.scalar_bool('Test_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Test_Left: bool = None
			self.Test_Right: bool = None

	def get_enable(self) -> EnableStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle \n
		Snippet: value: EnableStruct = driver.configure.afRf.measurement.demodulation.get_enable() \n
		No command help available \n
			:return: structure: for return value, see the help for EnableStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle?', self.__class__.EnableStruct())

	def set_enable(self, value: EnableStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle \n
		Snippet: driver.configure.afRf.measurement.demodulation.set_enable(value = EnableStruct()) \n
		No command help available \n
			:param value: see the help for EnableStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:ENABle', value)

	# noinspection PyTypeChecker
	class GcouplingStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Coupling_Left: enums.GeneratorCoupling: OFF | GEN1 | GEN2 | GEN3 | GEN4 OFF No coupling GENn Coupled to audio generator n
			- Coupling_Right: enums.GeneratorCoupling: OFF | GEN2 | GEN4"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Coupling_Left', enums.GeneratorCoupling),
			ArgStruct.scalar_enum('Coupling_Right', enums.GeneratorCoupling)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Coupling_Left: enums.GeneratorCoupling = None
			self.Coupling_Right: enums.GeneratorCoupling = None

	# noinspection PyTypeChecker
	def get_gcoupling(self) -> GcouplingStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling \n
		Snippet: value: GcouplingStruct = driver.configure.afRf.measurement.demodulation.get_gcoupling() \n
		Couples the audio output paths of the demodulator to an internal signal generator.
			INTRO_CMD_HELP: For FM stereo, the settings configure the left and the right audio channel. Only the following combinations are allowed: \n
			- OFF, OFF
			- GEN1, GEN2
			- GEN3, GEN4
		For other modulation types, only <CouplingLeft> is relevant. <CouplingRight> has no effect. \n
			:return: structure: for return value, see the help for GcouplingStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling?', self.__class__.GcouplingStruct())

	def set_gcoupling(self, value: GcouplingStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling \n
		Snippet: driver.configure.afRf.measurement.demodulation.set_gcoupling(value = GcouplingStruct()) \n
		Couples the audio output paths of the demodulator to an internal signal generator.
			INTRO_CMD_HELP: For FM stereo, the settings configure the left and the right audio channel. Only the following combinations are allowed: \n
			- OFF, OFF
			- GEN1, GEN2
			- GEN3, GEN4
		For other modulation types, only <CouplingLeft> is relevant. <CouplingRight> has no effect. \n
			:param value: see the help for GcouplingStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:GCOupling', value)

	# noinspection PyTypeChecker
	class TmodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Tone_Mode_Left: enums.ToneMode: No parameter help available
			- Tone_Mode_Right: enums.ToneMode: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_enum('Tone_Mode_Left', enums.ToneMode),
			ArgStruct.scalar_enum('Tone_Mode_Right', enums.ToneMode)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Tone_Mode_Left: enums.ToneMode = None
			self.Tone_Mode_Right: enums.ToneMode = None

	# noinspection PyTypeChecker
	def get_tmode(self) -> TmodeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe \n
		Snippet: value: TmodeStruct = driver.configure.afRf.measurement.demodulation.get_tmode() \n
		No command help available \n
			:return: structure: for return value, see the help for TmodeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe?', self.__class__.TmodeStruct())

	def set_tmode(self, value: TmodeStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe \n
		Snippet: driver.configure.afRf.measurement.demodulation.set_tmode(value = TmodeStruct()) \n
		No command help available \n
			:param value: see the help for TmodeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:DEModulation:TMODe', value)

	# noinspection PyTypeChecker
	def get_value(self) -> enums.Demodulation:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation \n
		Snippet: value: enums.Demodulation = driver.configure.afRf.measurement.demodulation.get_value() \n
		Selects the type of demodulation to be performed. \n
			:return: demodulation: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		response = self._core.io.query_str('CONFigure:AFRF:MEASurement<Instance>:DEModulation?')
		return Conversions.str_to_scalar_enum(response, enums.Demodulation)

	def set_value(self, demodulation: enums.Demodulation) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:DEModulation \n
		Snippet: driver.configure.afRf.measurement.demodulation.set_value(demodulation = enums.Demodulation.AM) \n
		Selects the type of demodulation to be performed. \n
			:param demodulation: FMSTereo | FM | AM | USB | LSB | PM FMSTereo FM stereo multiplex signal FM, PM, AM Frequency / phase / amplitude modulation USB, LSB Single sideband modulation, upper / lower sideband
		"""
		param = Conversions.enum_scalar_to_str(demodulation, enums.Demodulation)
		self._core.io.write(f'CONFigure:AFRF:MEASurement<Instance>:DEModulation {param}')

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
