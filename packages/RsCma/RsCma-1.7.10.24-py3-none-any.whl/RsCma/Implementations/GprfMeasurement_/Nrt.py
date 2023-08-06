from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nrt:
	"""Nrt commands group definition. 30 total commands, 3 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nrt", core, parent)

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Nrt_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def forward(self):
		"""forward commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_forward'):
			from .Nrt_.Forward import Forward
			self._forward = Forward(self._core, self._base)
		return self._forward

	@property
	def reverse(self):
		"""reverse commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_reverse'):
			from .Nrt_.Reverse import Reverse
			self._reverse = Reverse(self._core, self._base)
		return self._reverse

	def initiate(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.initiate() \n
		Starts or continues the NRT-Z measurement. \n
		"""
		self._core.io.write(f'INITiate:GPRF:MEASurement<Instance>:NRT')

	def initiate_with_opc(self) -> None:
		"""SCPI: INITiate:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.initiate_with_opc() \n
		Starts or continues the NRT-Z measurement. \n
		Same as initiate, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'INITiate:GPRF:MEASurement<Instance>:NRT')

	def stop(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.stop() \n
		Pauses the NRT-Z measurement. \n
		"""
		self._core.io.write(f'STOP:GPRF:MEASurement<Instance>:NRT')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.stop_with_opc() \n
		Pauses the NRT-Z measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:GPRF:MEASurement<Instance>:NRT')

	def abort(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.abort() \n
		Stops the NRT-Z measurement. \n
		"""
		self._core.io.write(f'ABORt:GPRF:MEASurement<Instance>:NRT')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:GPRF:MEASurement<Instance>:NRT \n
		Snippet: driver.gprfMeasurement.nrt.abort_with_opc() \n
		Stops the NRT-Z measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:GPRF:MEASurement<Instance>:NRT')

	def get_idn(self) -> str:
		"""SCPI: FETCh:GPRF:MEASurement<Instance>:NRT:IDN \n
		Snippet: value: str = driver.gprfMeasurement.nrt.get_idn() \n
		Queries the identification string of the connected external power sensor. \n
			:return: idn: String parameter
		"""
		response = self._core.io.query_str('FETCh:GPRF:MEASurement<Instance>:NRT:IDN?')
		return trim_str_response(response)

	def clone(self) -> 'Nrt':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nrt(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
