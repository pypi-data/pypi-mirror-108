from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Demodulation:
	"""Demodulation commands group definition. 16 total commands, 3 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("demodulation", core, parent)

	@property
	def fdeviation(self):
		"""fdeviation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Demodulation_.Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._base)
		return self._fdeviation

	@property
	def pdeviation(self):
		"""pdeviation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pdeviation'):
			from .Demodulation_.Pdeviation import Pdeviation
			self._pdeviation = Pdeviation(self._core, self._base)
		return self._pdeviation

	@property
	def fmStereo(self):
		"""fmStereo commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_fmStereo'):
			from .Demodulation_.FmStereo import FmStereo
			self._fmStereo = FmStereo(self._core, self._base)
		return self._fmStereo

	# noinspection PyTypeChecker
	class ThDistortionStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper THD limit Range: 0.001 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_th_distortion(self) -> ThDistortionStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDistortion \n
		Snippet: value: ThDistortionStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_th_distortion() \n
		Configures a limit for the THD results, measured via the RF input path. \n
			:return: structure: for return value, see the help for ThDistortionStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDistortion?', self.__class__.ThDistortionStruct())

	def set_th_distortion(self, value: ThDistortionStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDistortion \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_th_distortion(value = ThDistortionStruct()) \n
		Configures a limit for the THD results, measured via the RF input path. \n
			:param value: see the help for ThDistortionStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDistortion', value)

	# noinspection PyTypeChecker
	class ThdNoiseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper THD+N limit Range: 0.001 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_thd_noise(self) -> ThdNoiseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDNoise \n
		Snippet: value: ThdNoiseStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_thd_noise() \n
		Configures a limit for the THD+N results, measured via the RF input path. \n
			:return: structure: for return value, see the help for ThdNoiseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDNoise?', self.__class__.ThdNoiseStruct())

	def set_thd_noise(self, value: ThdNoiseStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDNoise \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_thd_noise(value = ThdNoiseStruct()) \n
		Configures a limit for the THD+N results, measured via the RF input path. \n
			:param value: see the help for ThdNoiseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:THDNoise', value)

	# noinspection PyTypeChecker
	class SnRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower limit Range: 1 dB to 46 dB, Unit: dB
			- Upper: float: Upper limit Range: 1 dB to 46 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_sn_ratio(self) -> SnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNRatio \n
		Snippet: value: SnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_sn_ratio() \n
		Configures limits for all SNR results, measured via the RF input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:return: structure: for return value, see the help for SnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNRatio?', self.__class__.SnRatioStruct())

	def set_sn_ratio(self, value: SnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_sn_ratio(value = SnRatioStruct()) \n
		Configures limits for all SNR results, measured via the RF input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:param value: see the help for SnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNRatio', value)

	# noinspection PyTypeChecker
	class SnnRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Lower: float: No parameter help available
			- Upper: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_snn_ratio(self) -> SnnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNNRatio \n
		Snippet: value: SnnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_snn_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SnnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNNRatio?', self.__class__.SnnRatioStruct())

	def set_snn_ratio(self, value: SnnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_snn_ratio(value = SnnRatioStruct()) \n
		No command help available \n
			:param value: see the help for SnnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNNRatio', value)

	# noinspection PyTypeChecker
	class SinadStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower SINAD limit Range: 0 dB to 140 dB, Unit: dB
			- Upper: float: Upper SINAD limit Range: 0 dB to 140 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_sinad(self) -> SinadStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SINad \n
		Snippet: value: SinadStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_sinad() \n
		Configures limits for the SINAD results, measured via the RF input path. \n
			:return: structure: for return value, see the help for SinadStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SINad?', self.__class__.SinadStruct())

	def set_sinad(self, value: SinadStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SINad \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_sinad(value = SinadStruct()) \n
		Configures limits for the SINAD results, measured via the RF input path. \n
			:param value: see the help for SinadStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SINad', value)

	# noinspection PyTypeChecker
	class SndRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: No parameter help available
			- Lower: float: No parameter help available
			- Upper: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_snd_ratio(self) -> SndRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNDRatio \n
		Snippet: value: SndRatioStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.get_snd_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SndRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNDRatio?', self.__class__.SndRatioStruct())

	def set_snd_ratio(self, value: SndRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNDRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.set_snd_ratio(value = SndRatioStruct()) \n
		No command help available \n
			:param value: see the help for SndRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:SNDRatio', value)

	def clone(self) -> 'Demodulation':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Demodulation(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
