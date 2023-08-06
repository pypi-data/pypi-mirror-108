from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Voip:
	"""Voip commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("voip", core, parent)

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDistortion \n
		Snippet: value: ThDistortionStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_th_distortion() \n
		Configures limits for the THD results, measured via the VoIP input path. \n
			:return: structure: for return value, see the help for ThDistortionStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDistortion?', self.__class__.ThDistortionStruct())

	def set_th_distortion(self, value: ThDistortionStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDistortion \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_th_distortion(value = ThDistortionStruct()) \n
		Configures limits for the THD results, measured via the VoIP input path. \n
			:param value: see the help for ThDistortionStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDistortion', value)

	# noinspection PyTypeChecker
	class ThdNoiseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper THD+N limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_thd_noise(self) -> ThdNoiseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDNoise \n
		Snippet: value: ThdNoiseStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_thd_noise() \n
		Configures limits for the THD+N results, measured via the VoIP input path. \n
			:return: structure: for return value, see the help for ThdNoiseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDNoise?', self.__class__.ThdNoiseStruct())

	def set_thd_noise(self, value: ThdNoiseStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDNoise \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_thd_noise(value = ThdNoiseStruct()) \n
		Configures limits for the THD+N results, measured via the VoIP input path. \n
			:param value: see the help for ThdNoiseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:THDNoise', value)

	# noinspection PyTypeChecker
	class SnRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower limit Range: 0 dB to 140 dB, Unit: dB
			- Upper: float: Upper limit Range: 0 dB to 140 dB, Unit: dB"""
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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNRatio \n
		Snippet: value: SnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_sn_ratio() \n
		Configures limits for all SNR results, measured via the VoIP input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:return: structure: for return value, see the help for SnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNRatio?', self.__class__.SnRatioStruct())

	def set_sn_ratio(self, value: SnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_sn_ratio(value = SnRatioStruct()) \n
		Configures limits for all SNR results, measured via the VoIP input path. SNR results include S/N, (S+N) /N and (S+N+D) /N. \n
			:param value: see the help for SnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNRatio', value)

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNNRatio \n
		Snippet: value: SnnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_snn_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SnnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNNRatio?', self.__class__.SnnRatioStruct())

	def set_snn_ratio(self, value: SnnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_snn_ratio(value = SnnRatioStruct()) \n
		No command help available \n
			:param value: see the help for SnnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNNRatio', value)

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNDRatio \n
		Snippet: value: SndRatioStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_snd_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SndRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNDRatio?', self.__class__.SndRatioStruct())

	def set_snd_ratio(self, value: SndRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNDRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_snd_ratio(value = SndRatioStruct()) \n
		No command help available \n
			:param value: see the help for SndRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SNDRatio', value)

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
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SINad \n
		Snippet: value: SinadStruct = driver.configure.afRf.measurement.multiEval.limit.voip.get_sinad() \n
		Configures limits for the SINAD results, measured via the VoIP input path. \n
			:return: structure: for return value, see the help for SinadStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SINad?', self.__class__.SinadStruct())

	def set_sinad(self, value: SinadStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SINad \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.voip.set_sinad(value = SinadStruct()) \n
		Configures limits for the SINAD results, measured via the VoIP input path. \n
			:param value: see the help for SinadStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:VOIP:SINad', value)
