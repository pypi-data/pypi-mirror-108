from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cprotection:
	"""Cprotection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cprotection", core, parent)

	def reset(self) -> None:
		"""SCPI: CONFigure:BASE:CPRotection:RESet \n
		Snippet: driver.configure.base.cprotection.reset() \n
		Resets the protection circuit of the RF connectors. \n
		"""
		self._core.io.write(f'CONFigure:BASE:CPRotection:RESet')

	def reset_with_opc(self) -> None:
		"""SCPI: CONFigure:BASE:CPRotection:RESet \n
		Snippet: driver.configure.base.cprotection.reset_with_opc() \n
		Resets the protection circuit of the RF connectors. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'CONFigure:BASE:CPRotection:RESet')
