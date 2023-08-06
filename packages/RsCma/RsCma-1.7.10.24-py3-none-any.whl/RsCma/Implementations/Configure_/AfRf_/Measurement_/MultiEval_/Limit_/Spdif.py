from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Spdif:
	"""Spdif commands group definition. 6 total commands, 0 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("spdif", core, parent)

	# noinspection PyTypeChecker
	class ThDistortionStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Upper_Left: float: Upper THD limit for the left SPDIF channel Range: 0 % to 100 %, Unit: %
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Upper_Right: float: Upper THD limit for the right SPDIF channel Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Upper_Left: float = None
			self.Enable_Right: bool = None
			self.Upper_Right: float = None

	def get_th_distortion(self) -> ThDistortionStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion \n
		Snippet: value: ThDistortionStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_th_distortion() \n
		Configures limits for the THD results, measured via the SPDIF input path. \n
			:return: structure: for return value, see the help for ThDistortionStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion?', self.__class__.ThDistortionStruct())

	def set_th_distortion(self, value: ThDistortionStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_th_distortion(value = ThDistortionStruct()) \n
		Configures limits for the THD results, measured via the SPDIF input path. \n
			:param value: see the help for ThDistortionStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDistortion', value)

	# noinspection PyTypeChecker
	class ThdNoiseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Upper_Left: float: Upper THD+N limit for the left SPDIF channel Range: 0.001 % to 100 %, Unit: %
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Upper_Right: float: Upper THD+N limit for the right SPDIF channel Range: 0.001 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Upper_Left: float = None
			self.Enable_Right: bool = None
			self.Upper_Right: float = None

	def get_thd_noise(self) -> ThdNoiseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDNoise \n
		Snippet: value: ThdNoiseStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_thd_noise() \n
		Configures limits for the THD+N results, measured via the SPDIF input path. \n
			:return: structure: for return value, see the help for ThdNoiseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDNoise?', self.__class__.ThdNoiseStruct())

	def set_thd_noise(self, value: ThdNoiseStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDNoise \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_thd_noise(value = ThdNoiseStruct()) \n
		Configures limits for the THD+N results, measured via the SPDIF input path. \n
			:param value: see the help for ThdNoiseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:THDNoise', value)

	# noinspection PyTypeChecker
	class SnRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Lower_Left: float: Lower limit for the left SPDIF channel Range: 1 dB to 46 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Lower_Right: float: Lower limit for the right SPDIF channel Range: 1 dB to 46 dB, Unit: dB
			- Upper_Left: float: Upper limit for the left SPDIF channel Range: 1 dB to 46 dB, Unit: dB
			- Upper_Right: float: Upper limit for the right SPDIF channel Range: 1 dB to 46 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_sn_ratio(self) -> SnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio \n
		Snippet: value: SnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_sn_ratio() \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:return: structure: for return value, see the help for SnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio?', self.__class__.SnRatioStruct())

	def set_sn_ratio(self, value: SnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_sn_ratio(value = SnRatioStruct()) \n
		Configures limits for all SNR results, measured via the SPDIF input path. SNR results include S/N, (S+N) /N and (S+N+D)
		/N. \n
			:param value: see the help for SnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNRatio', value)

	# noinspection PyTypeChecker
	class SinadStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: OFF | ON Enables or disables the limit check for the left SPDIF channel
			- Lower_Left: float: Lower SINAD limit for the left SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Enable_Right: bool: OFF | ON Enables or disables the limit check for the right SPDIF channel
			- Lower_Right: float: Lower SINAD limit for the right SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Upper_Left: float: Upper SINAD limit for the left SPDIF channel Range: 0 dB to 140 dB, Unit: dB
			- Upper_Right: float: Upper SINAD limit for the right SPDIF channel Range: 0 dB to 140 dB, Unit: dB"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_sinad(self) -> SinadStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad \n
		Snippet: value: SinadStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_sinad() \n
		Configures limits for the SINAD results, measured via the SPDIF input path. \n
			:return: structure: for return value, see the help for SinadStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad?', self.__class__.SinadStruct())

	def set_sinad(self, value: SinadStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_sinad(value = SinadStruct()) \n
		Configures limits for the SINAD results, measured via the SPDIF input path. \n
			:param value: see the help for SinadStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SINad', value)

	# noinspection PyTypeChecker
	class SnnRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: No parameter help available
			- Lower_Left: float: No parameter help available
			- Enable_Right: bool: No parameter help available
			- Lower_Right: float: No parameter help available
			- Upper_Left: float: No parameter help available
			- Upper_Right: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_snn_ratio(self) -> SnnRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio \n
		Snippet: value: SnnRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_snn_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SnnRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio?', self.__class__.SnnRatioStruct())

	def set_snn_ratio(self, value: SnnRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_snn_ratio(value = SnnRatioStruct()) \n
		No command help available \n
			:param value: see the help for SnnRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNNRatio', value)

	# noinspection PyTypeChecker
	class SndRatioStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable_Left: bool: No parameter help available
			- Lower_Left: float: No parameter help available
			- Enable_Right: bool: No parameter help available
			- Lower_Right: float: No parameter help available
			- Upper_Left: float: No parameter help available
			- Upper_Right: float: No parameter help available"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable_Left'),
			ArgStruct.scalar_float('Lower_Left'),
			ArgStruct.scalar_bool('Enable_Right'),
			ArgStruct.scalar_float('Lower_Right'),
			ArgStruct.scalar_float('Upper_Left'),
			ArgStruct.scalar_float('Upper_Right')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable_Left: bool = None
			self.Lower_Left: float = None
			self.Enable_Right: bool = None
			self.Lower_Right: float = None
			self.Upper_Left: float = None
			self.Upper_Right: float = None

	def get_snd_ratio(self) -> SndRatioStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio \n
		Snippet: value: SndRatioStruct = driver.configure.afRf.measurement.multiEval.limit.spdif.get_snd_ratio() \n
		No command help available \n
			:return: structure: for return value, see the help for SndRatioStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio?', self.__class__.SndRatioStruct())

	def set_snd_ratio(self, value: SndRatioStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.spdif.set_snd_ratio(value = SndRatioStruct()) \n
		No command help available \n
			:param value: see the help for SndRatioStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:SIN:SNDRatio', value)
