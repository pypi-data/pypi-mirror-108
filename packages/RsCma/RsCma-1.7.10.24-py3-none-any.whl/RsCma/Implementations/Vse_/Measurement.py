from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measurement:
	"""Measurement commands group definition. 85 total commands, 19 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("measurement", core, parent)

	@property
	def dmr(self):
		"""dmr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dmr'):
			from .Measurement_.Dmr import Dmr
			self._dmr = Dmr(self._core, self._base)
		return self._dmr

	@property
	def nxdn(self):
		"""nxdn commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_nxdn'):
			from .Measurement_.Nxdn import Nxdn
			self._nxdn = Nxdn(self._core, self._base)
		return self._nxdn

	@property
	def tetra(self):
		"""tetra commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_tetra'):
			from .Measurement_.Tetra import Tetra
			self._tetra = Tetra(self._core, self._base)
		return self._tetra

	@property
	def dpmr(self):
		"""dpmr commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_dpmr'):
			from .Measurement_.Dpmr import Dpmr
			self._dpmr = Dpmr(self._core, self._base)
		return self._dpmr

	@property
	def lte(self):
		"""lte commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_lte'):
			from .Measurement_.Lte import Lte
			self._lte = Lte(self._core, self._base)
		return self._lte

	@property
	def state(self):
		"""state commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_state'):
			from .Measurement_.State import State
			self._state = State(self._core, self._base)
		return self._state

	@property
	def cons(self):
		"""cons commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_cons'):
			from .Measurement_.Cons import Cons
			self._cons = Cons(self._core, self._base)
		return self._cons

	@property
	def ediagram(self):
		"""ediagram commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ediagram'):
			from .Measurement_.Ediagram import Ediagram
			self._ediagram = Ediagram(self._core, self._base)
		return self._ediagram

	@property
	def powerVsTime(self):
		"""powerVsTime commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_powerVsTime'):
			from .Measurement_.PowerVsTime import PowerVsTime
			self._powerVsTime = PowerVsTime(self._core, self._base)
		return self._powerVsTime

	@property
	def perror(self):
		"""perror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_perror'):
			from .Measurement_.Perror import Perror
			self._perror = Perror(self._core, self._base)
		return self._perror

	@property
	def evm(self):
		"""evm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_evm'):
			from .Measurement_.Evm import Evm
			self._evm = Evm(self._core, self._base)
		return self._evm

	@property
	def ffError(self):
		"""ffError commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_ffError'):
			from .Measurement_.FfError import FfError
			self._ffError = FfError(self._core, self._base)
		return self._ffError

	@property
	def fdeviation(self):
		"""fdeviation commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdeviation'):
			from .Measurement_.Fdeviation import Fdeviation
			self._fdeviation = Fdeviation(self._core, self._base)
		return self._fdeviation

	@property
	def fdError(self):
		"""fdError commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_fdError'):
			from .Measurement_.FdError import FdError
			self._fdError = FdError(self._core, self._base)
		return self._fdError

	@property
	def merror(self):
		"""merror commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_merror'):
			from .Measurement_.Merror import Merror
			self._merror = Merror(self._core, self._base)
		return self._merror

	@property
	def ptFive(self):
		"""ptFive commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_ptFive'):
			from .Measurement_.PtFive import PtFive
			self._ptFive = PtFive(self._core, self._base)
		return self._ptFive

	@property
	def rfCarrier(self):
		"""rfCarrier commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_rfCarrier'):
			from .Measurement_.RfCarrier import RfCarrier
			self._rfCarrier = RfCarrier(self._core, self._base)
		return self._rfCarrier

	@property
	def sdistribute(self):
		"""sdistribute commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_sdistribute'):
			from .Measurement_.Sdistribute import Sdistribute
			self._sdistribute = Sdistribute(self._core, self._base)
		return self._sdistribute

	@property
	def spectrum(self):
		"""spectrum commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_spectrum'):
			from .Measurement_.Spectrum import Spectrum
			self._spectrum = Spectrum(self._core, self._base)
		return self._spectrum

	def stop(self) -> None:
		"""SCPI: STOP:VSE:MEASurement<Instance> \n
		Snippet: driver.vse.measurement.stop() \n
		Pauses the measurement. \n
		"""
		self._core.io.write(f'STOP:VSE:MEASurement<Instance>')

	def stop_with_opc(self) -> None:
		"""SCPI: STOP:VSE:MEASurement<Instance> \n
		Snippet: driver.vse.measurement.stop_with_opc() \n
		Pauses the measurement. \n
		Same as stop, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'STOP:VSE:MEASurement<Instance>')

	def abort(self) -> None:
		"""SCPI: ABORt:VSE:MEASurement<Instance> \n
		Snippet: driver.vse.measurement.abort() \n
		Stops the measurement. \n
		"""
		self._core.io.write(f'ABORt:VSE:MEASurement<Instance>')

	def abort_with_opc(self) -> None:
		"""SCPI: ABORt:VSE:MEASurement<Instance> \n
		Snippet: driver.vse.measurement.abort_with_opc() \n
		Stops the measurement. \n
		Same as abort, but waits for the operation to complete before continuing further. Use the RsCma.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'ABORt:VSE:MEASurement<Instance>')

	def clone(self) -> 'Measurement':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Measurement(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
