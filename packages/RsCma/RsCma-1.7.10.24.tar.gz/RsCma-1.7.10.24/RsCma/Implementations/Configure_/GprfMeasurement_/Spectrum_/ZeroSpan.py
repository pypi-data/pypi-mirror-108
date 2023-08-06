from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class ZeroSpan:
	"""ZeroSpan commands group definition. 8 total commands, 3 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("zeroSpan", core, parent)

	@property
	def rbw(self):
		"""rbw commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_rbw'):
			from .ZeroSpan_.Rbw import Rbw
			self._rbw = Rbw(self._core, self._base)
		return self._rbw

	@property
	def vbw(self):
		"""vbw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_vbw'):
			from .ZeroSpan_.Vbw import Vbw
			self._vbw = Vbw(self._core, self._base)
		return self._vbw

	@property
	def marker(self):
		"""marker commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .ZeroSpan_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	def get_swt(self) -> float:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:SWT \n
		Snippet: value: float = driver.configure.gprfMeasurement.spectrum.zeroSpan.get_swt() \n
		Specifies the sweep time for the zero span mode. \n
			:return: sweep_time: Range: 500.5E-6 s to 2000 s, Unit: s
		"""
		response = self._core.io.query_str('CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:SWT?')
		return Conversions.str_to_float(response)

	def set_swt(self, sweep_time: float) -> None:
		"""SCPI: CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:SWT \n
		Snippet: driver.configure.gprfMeasurement.spectrum.zeroSpan.set_swt(sweep_time = 1.0) \n
		Specifies the sweep time for the zero span mode. \n
			:param sweep_time: Range: 500.5E-6 s to 2000 s, Unit: s
		"""
		param = Conversions.decimal_value_to_str(sweep_time)
		self._core.io.write(f'CONFigure:GPRF:MEASurement<Instance>:SPECtrum:ZSPan:SWT {param}')

	def clone(self) -> 'ZeroSpan':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = ZeroSpan(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
