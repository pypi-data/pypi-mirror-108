from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tones:
	"""Tones commands group definition. 9 total commands, 2 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tones", core, parent)

	@property
	def scal(self):
		"""scal commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_scal'):
			from .Tones_.Scal import Scal
			self._scal = Scal(self._core, self._base)
		return self._scal

	@property
	def dcs(self):
		"""dcs commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_dcs'):
			from .Tones_.Dcs import Dcs
			self._dcs = Dcs(self._core, self._base)
		return self._dcs

	# noinspection PyTypeChecker
	class DigPauseStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower pause limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper pause limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_dig_pause(self) -> DigPauseStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause \n
		Snippet: value: DigPauseStruct = driver.configure.afRf.measurement.multiEval.limit.tones.get_dig_pause() \n
		Configures limits for the pause between two tones of an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:return: structure: for return value, see the help for DigPauseStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause?', self.__class__.DigPauseStruct())

	def set_dig_pause(self, value: DigPauseStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.set_dig_pause(value = DigPauseStruct()) \n
		Configures limits for the pause between two tones of an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:param value: see the help for DigPauseStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGPause', value)

	# noinspection PyTypeChecker
	class DigtimeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower digit-duration limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper digit-duration limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_digtime(self) -> DigtimeStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime \n
		Snippet: value: DigtimeStruct = driver.configure.afRf.measurement.multiEval.limit.tones.get_digtime() \n
		Configures limits for the digit duration in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:return: structure: for return value, see the help for DigtimeStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime?', self.__class__.DigtimeStruct())

	def set_digtime(self, value: DigtimeStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.set_digtime(value = DigtimeStruct()) \n
		Configures limits for the digit duration in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:param value: see the help for DigtimeStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:DIGTime', value)

	# noinspection PyTypeChecker
	class FdeviationStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables or disables the limit check
			- Lower: float: Lower frequency-deviation limit Range: -100 % to 0 %, Unit: %
			- Upper: float: Upper frequency-deviation limit Range: 0 % to 100 %, Unit: %"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Lower'),
			ArgStruct.scalar_float('Upper')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Lower: float = None
			self.Upper: float = None

	def get_fdeviation(self) -> FdeviationStruct:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:FDEViation \n
		Snippet: value: FdeviationStruct = driver.configure.afRf.measurement.multiEval.limit.tones.get_fdeviation() \n
		Configures limits for the frequency deviation of tones in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:return: structure: for return value, see the help for FdeviationStruct structure arguments.
		"""
		return self._core.io.query_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:FDEViation?', self.__class__.FdeviationStruct())

	def set_fdeviation(self, value: FdeviationStruct) -> None:
		"""SCPI: CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:FDEViation \n
		Snippet: driver.configure.afRf.measurement.multiEval.limit.tones.set_fdeviation(value = FdeviationStruct()) \n
		Configures limits for the frequency deviation of tones in an analyzed tone sequence (DTMF, free dialing and SelCall) . \n
			:param value: see the help for FdeviationStruct structure arguments.
		"""
		self._core.io.write_struct('CONFigure:AFRF:MEASurement<Instance>:MEValuation:LIMit:TONes:FDEViation', value)

	def clone(self) -> 'Tones':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tones(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
