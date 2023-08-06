from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Device:
	"""Device commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("device", core, parent)

	def set(self) -> None:
		"""SCPI: SYSTem:BASE:RESTart:DEVice \n
		Snippet: driver.system.base.restart.device.set() \n
		Restarts the instrument. \n
		"""
		self._core.io.write(f'SYSTem:BASE:RESTart:DEVice')

	def set_with_opc(self) -> None:
		"""SCPI: SYSTem:BASE:RESTart:DEVice \n
		Snippet: driver.system.base.restart.device.set_with_opc() \n
		Restarts the instrument. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SYSTem:BASE:RESTart:DEVice')
