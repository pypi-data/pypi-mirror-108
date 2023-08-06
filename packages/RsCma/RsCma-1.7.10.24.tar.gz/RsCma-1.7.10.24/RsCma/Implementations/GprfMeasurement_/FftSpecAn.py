from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FftSpecAn:
	"""FftSpecAn commands group definition. 26 total commands, 7 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fftSpecAn", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .FftSpecAn_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .FftSpecAn_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def peaks(self):
		"""peaks commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_peaks'):
			from .FftSpecAn_.Peaks import Peaks
			self._peaks = Peaks(self._core, self._base)
		return self._peaks

	@property
	def power(self):
		"""power commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_power'):
			from .FftSpecAn_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def qcomponent(self):
		"""qcomponent commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_qcomponent'):
			from .FftSpecAn_.Qcomponent import Qcomponent
			self._qcomponent = Qcomponent(self._core, self._base)
		return self._qcomponent

	@property
	def icomponent(self):
		"""icomponent commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_icomponent'):
			from .FftSpecAn_.Icomponent import Icomponent
			self._icomponent = Icomponent(self._core, self._base)
		return self._icomponent

	@property
	def tdomain(self):
		"""tdomain commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tdomain'):
			from .FftSpecAn_.Tdomain import Tdomain
			self._tdomain = Tdomain(self._core, self._base)
		return self._tdomain

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.initiate() \n
		Starts or continues the FFT spectrum analyzer. \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.initiate_with_opc() \n
		Starts or continues the FFT spectrum analyzer. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.stop() \n
		Pauses the FFT spectrum analyzer. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.stop_with_opc() \n
		Pauses the FFT spectrum analyzer. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.abort() \n
		Stops the FFT spectrum analyzer. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:FFTSanalyzer \n
		Snippet: driver.gprfMeasurement.fftSpecAn.abort_with_opc() \n
		Stops the FFT spectrum analyzer. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:FFTSanalyzer')

	def clone(self) -> 'FftSpecAn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FftSpecAn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
