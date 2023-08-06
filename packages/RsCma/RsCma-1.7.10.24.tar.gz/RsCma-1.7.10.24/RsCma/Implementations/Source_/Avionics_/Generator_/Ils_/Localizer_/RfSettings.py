from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.StructBase import StructBase
from .......Internal.ArgStruct import ArgStruct
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RfSettings:
	"""RfSettings commands group definition. 4 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rfSettings", core, parent)

	@property
	def rfOut(self):
		"""rfOut commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rfOut'):
			from .RfSettings_.RfOut import RfOut
			self._rfOut = RfOut(self._core, self._base)
		return self._rfOut

	def get_frequency(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:FREQuency \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.rfSettings.get_frequency() \n
		Specifies the center frequency of the unmodulated RF carrier for the localizer signal. \n
			:return: freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, freq: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:FREQuency \n
		Snippet: driver.source.avionics.generator.ils.localizer.rfSettings.set_frequency(freq = 1.0) \n
		Specifies the center frequency of the unmodulated RF carrier for the localizer signal. \n
			:param freq: Range: 100 kHz to 3 GHz, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(freq)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:FREQuency {param}')

	# noinspection PyTypeChecker
	class ChannelStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Channel: int: Channel number Range: 18 to 56
			- Letter: enums.IlsLetter: X | Y Channel letter"""
		__meta_args_list = [
			ArgStruct.scalar_int('Channel'),
			ArgStruct.scalar_enum('Letter', enums.IlsLetter)]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Channel: int = None
			self.Letter: enums.IlsLetter = None

	def get_channel(self) -> ChannelStruct:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel \n
		Snippet: value: ChannelStruct = driver.source.avionics.generator.ils.localizer.rfSettings.get_channel() \n
		Selects the RF channel. Each channel is identified via a number and a letter, for example 18X. \n
			:return: structure: for return value, see the help for ChannelStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel?', self.__class__.ChannelStruct())

	def set_channel(self, value: ChannelStruct) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel \n
		Snippet: driver.source.avionics.generator.ils.localizer.rfSettings.set_channel(value = ChannelStruct()) \n
		Selects the RF channel. Each channel is identified via a number and a letter, for example 18X. \n
			:param value: see the help for ChannelStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:CHANnel', value)

	def get_level(self) -> float:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:LEVel \n
		Snippet: value: float = driver.source.avionics.generator.ils.localizer.rfSettings.get_level() \n
		Specifies the RMS level of the unmodulated RF carrier. The allowed range depends on several other settings, for example
		on the selected connector, the frequency and the external attenuation. For supported output level ranges, refer to the
		data sheet. \n
			:return: level: Unit: dBm
		"""
		response = self._core.io.query_str('SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:LEVel?')
		return Conversions.str_to_float(response)

	def set_level(self, level: float) -> None:
		"""SCPI: SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:LEVel \n
		Snippet: driver.source.avionics.generator.ils.localizer.rfSettings.set_level(level = 1.0) \n
		Specifies the RMS level of the unmodulated RF carrier. The allowed range depends on several other settings, for example
		on the selected connector, the frequency and the external attenuation. For supported output level ranges, refer to the
		data sheet. \n
			:param level: Unit: dBm
		"""
		param = Conversions.decimal_value_to_str(level)
		self._core.io.write(f'SOURce:AVIonics:GENerator<Instance>:ILS:LOCalizer:RFSettings:LEVel {param}')

	def clone(self) -> 'RfSettings':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = RfSettings(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group
