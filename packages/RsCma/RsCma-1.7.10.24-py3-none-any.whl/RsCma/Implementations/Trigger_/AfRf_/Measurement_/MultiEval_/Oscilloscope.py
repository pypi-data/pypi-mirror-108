from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Oscilloscope:
	"""Oscilloscope commands group definition. 35 total commands, 4 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("oscilloscope", core, parent)

	@property
	def demodulation(self):
		"""demodulation commands group. 4 Sub-classes, 7 commands."""
		if not hasattr(self, '_demodulation'):
			from .Oscilloscope_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def audioInput(self):
		"""audioInput commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_audioInput'):
			from .Oscilloscope_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdif(self):
		"""spdif commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_spdif'):
			from .Oscilloscope_.Spdif import Spdif
			self._spdif = Spdif(self._core, self._base)
		return self._spdif

	@property
	def voip(self):
		"""voip commands group. 0 Sub-classes, 7 commands."""
		if not hasattr(self, '_voip'):
			from .Oscilloscope_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	# noinspection PyTypeChecker
	class TimeoutStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Enable: bool: OFF | ON Enables the timeout
			- Timeout: float: Time interval during which a trigger event must occur Range: 0.2 s to 30 s, Unit: s"""
		__meta_args_list = [
			ArgStruct.scalar_bool('Enable'),
			ArgStruct.scalar_float('Timeout')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Enable: bool = None
			self.Timeout: float = None

	def get_timeout(self) -> TimeoutStruct:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT \n
		Snippet: value: TimeoutStruct = driver.trigger.afRf.measurement.multiEval.oscilloscope.get_timeout() \n
		Configures a timeout for the trigger modes 'Single' and 'Normal'. \n
			:return: structure: for return value, see the help for TimeoutStruct structure arguments.
		"""
		return self._core.io.query_struct('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT?', self.__class__.TimeoutStruct())

	def set_timeout(self, value: TimeoutStruct) -> None:
		"""SCPI: TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT \n
		Snippet: driver.trigger.afRf.measurement.multiEval.oscilloscope.set_timeout(value = TimeoutStruct()) \n
		Configures a timeout for the trigger modes 'Single' and 'Normal'. \n
			:param value: see the help for TimeoutStruct structure arguments.
		"""
		self._core.io.write_struct('TRIGger:AFRF:MEASurement<Instance>:MEValuation:OSCilloscope:TOUT', value)

	def clone(self) -> 'Oscilloscope':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Oscilloscope(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
