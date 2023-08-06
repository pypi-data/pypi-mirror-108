from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, window=repcap.Window.Default) -> None:
		"""SCPI: DISPlay[:WINDow<1-n>]:SELect \n
		Snippet: driver.display.window.select.set(window = repcap.Window.Default) \n
		No command help available \n
			:param window: optional repeated capability selector. Default value: Win1 (settable in the interface 'Window')"""
		window_cmd_val = self._base.get_repcap_cmd_value(window, repcap.Window)
		self._core.io.write(f'DISPlay:WINDow{window_cmd_val}:SELect')

	def set_with_opc(self, window=repcap.Window.Default) -> None:
		window_cmd_val = self._base.get_repcap_cmd_value(window, repcap.Window)
		"""SCPI: DISPlay[:WINDow<1-n>]:SELect \n
		Snippet: driver.display.window.select.set_with_opc(window = repcap.Window.Default) \n
		No command help available \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
			:param window: optional repeated capability selector. Default value: Win1 (settable in the interface 'Window')"""
		self._core.io.write_with_opc(f'DISPlay:WINDow{window_cmd_val}:SELect')
