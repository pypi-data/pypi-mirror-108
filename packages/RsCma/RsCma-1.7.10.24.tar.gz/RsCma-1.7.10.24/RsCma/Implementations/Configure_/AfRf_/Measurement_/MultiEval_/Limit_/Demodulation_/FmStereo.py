from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal.StructBase import StructBase
from ........Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FmStereo:
	"""FmStereo commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fmStereo", core, parent)

	@property
	def mdeviation(self):
		"""mdeviation commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_mdeviation'):
			from .FmStereo_.Mdeviation import Mdeviation
			self._mdeviation = Mdeviation(self._core, self._base)
		return self._mdeviation

	# noinspection PyTypeChecker
	class AdeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper audio deviation limit Range: 0 Hz to 100 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_adeviation(self) -> AdeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation \n
		Snippet: value: AdeviationStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.get_adeviation() \n
		Configures a limit for the audio deviation results, measured for FM stereo. \n
			:return: structure: for return value, see the help for AdeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation?', self.__class__.AdeviationStruct())

	def set_adeviation(self, value: AdeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.set_adeviation(value = AdeviationStruct()) \n
		Configures a limit for the audio deviation results, measured for FM stereo. \n
			:param value: see the help for AdeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:ADEViation', value)

	# noinspection PyTypeChecker
	class PiDeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper pilot deviation limit Range: 0 Hz to 10 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_pi_deviation(self) -> PiDeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PIDeviation \n
		Snippet: value: PiDeviationStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.get_pi_deviation() \n
		Configures a limit for the pilot deviation results, measured for FM stereo. \n
			:return: structure: for return value, see the help for PiDeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PIDeviation?', self.__class__.PiDeviationStruct())

	def set_pi_deviation(self, value: PiDeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PIDeviation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.set_pi_deviation(value = PiDeviationStruct()) \n
		Configures a limit for the pilot deviation results, measured for FM stereo. \n
			:param value: see the help for PiDeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PIDeviation', value)

	# noinspection PyTypeChecker
	class PfErrorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower frequency error limit Range: -100 Hz to 0 Hz, Unit: Hz
			- Upper: float: Upper frequency error limit You can skip this setting. The Upper value equals always the Lower value times -1 (same absolute value, opposite sign) . Range: 0 Hz to 100 Hz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_pf_error(self) -> PfErrorStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PFERror \n
		Snippet: value: PfErrorStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.get_pf_error() \n
		Configures limits for the pilot frequency error, measured for FM stereo. \n
			:return: structure: for return value, see the help for PfErrorStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PFERror?', self.__class__.PfErrorStruct())

	def set_pf_error(self, value: PfErrorStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PFERror \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.set_pf_error(value = PfErrorStruct()) \n
		Configures limits for the pilot frequency error, measured for FM stereo. \n
			:param value: see the help for PfErrorStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:PFERror', value)

	# noinspection PyTypeChecker
	class RdsDeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Upper: float: Upper RDS deviation limit Range: 0 Hz to 10 kHz, Unit: Hz"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Upper: float = None

	def get_rds_deviation(self) -> RdsDeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:RDSDeviation \n
		Snippet: value: RdsDeviationStruct = driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.get_rds_deviation() \n
		Configures a limit for the RDS deviation, measured for FM stereo. \n
			:return: structure: for return value, see the help for RdsDeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:RDSDeviation?', self.__class__.RdsDeviationStruct())

	def set_rds_deviation(self, value: RdsDeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:RDSDeviation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.demodulation.fmStereo.set_rds_deviation(value = RdsDeviationStruct()) \n
		Configures a limit for the RDS deviation, measured for FM stereo. \n
			:param value: see the help for RdsDeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:DEModulation:FMSTereo:RDSDeviation', value)

	def clone(self) -> 'FmStereo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FmStereo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
