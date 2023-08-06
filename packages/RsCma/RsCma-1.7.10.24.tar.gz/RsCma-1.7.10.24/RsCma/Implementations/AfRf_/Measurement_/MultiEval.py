from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class MultiEval:
	"""MultiEval commands group definition. 530 total commands, 14 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("multiEval", core, parent)

	@property
	def audioInput(self):
		"""audioInput commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_audioInput'):
			from .MultiEval_.AudioInput import AudioInput
			self._audioInput = AudioInput(self._core, self._base)
		return self._audioInput

	@property
	def spdifLeft(self):
		"""spdifLeft commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifLeft'):
			from .MultiEval_.SpdifLeft import SpdifLeft
			self._spdifLeft = SpdifLeft(self._core, self._base)
		return self._spdifLeft

	@property
	def spdifRight(self):
		"""spdifRight commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_spdifRight'):
			from .MultiEval_.SpdifRight import SpdifRight
			self._spdifRight = SpdifRight(self._core, self._base)
		return self._spdifRight

	@property
	def voip(self):
		"""voip commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_voip'):
			from .MultiEval_.Voip import Voip
			self._voip = Voip(self._core, self._base)
		return self._voip

	@property
	def demodLeft(self):
		"""demodLeft commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodLeft'):
			from .MultiEval_.DemodLeft import DemodLeft
			self._demodLeft = DemodLeft(self._core, self._base)
		return self._demodLeft

	@property
	def demodRight(self):
		"""demodRight commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodRight'):
			from .MultiEval_.DemodRight import DemodRight
			self._demodRight = DemodRight(self._core, self._base)
		return self._demodRight

	@property
	def demodulation(self):
		"""demodulation commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_demodulation'):
			from .MultiEval_.Demodulation import Demodulation
			self._demodulation = Demodulation(self._core, self._base)
		return self._demodulation

	@property
	def rfCarrier(self):
		"""rfCarrier commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfCarrier'):
			from .MultiEval_.RfCarrier import RfCarrier
			self._rfCarrier = RfCarrier(self._core, self._base)
		return self._rfCarrier

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .MultiEval_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def oscilloscope(self):
		"""oscilloscope commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_oscilloscope'):
			from .MultiEval_.Oscilloscope import Oscilloscope
			self._oscilloscope = Oscilloscope(self._core, self._base)
		return self._oscilloscope

	@property
	def signalQuality(self):
		"""signalQuality commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_signalQuality'):
			from .MultiEval_.SignalQuality import SignalQuality
			self._signalQuality = SignalQuality(self._core, self._base)
		return self._signalQuality

	@property
	def tones(self):
		"""tones commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_tones'):
			from .MultiEval_.Tones import Tones
			self._tones = Tones(self._core, self._base)
		return self._tones

	@property
	def fft(self):
		"""fft commands group. 8 Sub-classes, 0 commands."""
		if not hasattr(self, '_fft'):
			from .MultiEval_.Fft import Fft
			self._fft = Fft(self._core, self._base)
		return self._fft

	@property
	def mtones(self):
		"""mtones commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mtones'):
			from .MultiEval_.Mtones import Mtones
			self._mtones = Mtones(self._core, self._base)
		return self._mtones

	def initiate(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.initiate() \n
		Starts or continues the analyzer. \n
		"""
		self._core.io.write(f'INITiate:AFRF:MEASurement<Instance>:MEValuation')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.initiate_with_opc() \n
		Starts or continues the analyzer. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:AFRF:MEASurement<Instance>:MEValuation')

	def stop(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.stop() \n
		Pauses the analyzer. \n
		"""
		self._core.io.write(f'STOP:AFRF:MEASurement<Instance>:MEValuation')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.stop_with_opc() \n
		Pauses the analyzer. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:AFRF:MEASurement<Instance>:MEValuation')

	def abort(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.abort() \n
		Stops the analyzer. \n
		"""
		self._core.io.write(f'ABORt:AFRF:MEASurement<Instance>:MEValuation')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:AFRF:MEASurement<Instance>:MEValuation \n
		Snippet: driver.afRf.measurement.multiEval.abort_with_opc() \n
		Stops the analyzer. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:AFRF:MEASurement<Instance>:MEValuation')

	def clone(self) -> 'MultiEval':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = MultiEval(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
