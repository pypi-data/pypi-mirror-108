#  Copyright (c) 2019-2021 ETH Zurich, SIS ID and HVL D-ITET
#
"""Devices subpackage."""

import sys

from .base import (  # noqa: F401
    Device,
    DeviceExistingException,
    DeviceSequenceMixin,
    DeviceFailuresException,
    SingleCommDevice,
)
from .crylas import (  # noqa: F401
    CryLasLaser,
    CryLasLaserConfig,
    CryLasLaserSerialCommunication,
    CryLasLaserSerialCommunicationConfig,
    CryLasLaserError,
    CryLasLaserNotReadyError,
    CryLasAttenuator,
    CryLasAttenuatorConfig,
    CryLasAttenuatorSerialCommunication,
    CryLasAttenuatorSerialCommunicationConfig,
    CryLasAttenuatorError,
)
from .ea_psi9000 import (  # noqa: F401
    PSI9000,
    PSI9000Config,
    PSI9000VisaCommunication,
    PSI9000VisaCommunicationConfig,
    PSI9000Error,
)
from .fug import (  # noqa: F401
    FuG,
    FuGConfig,
    FuGSerialCommunication,
    FuGSerialCommunicationConfig,
    FuGError,
    FuGErrorcodes,
    FuGDigitalVal,
    FuGTerminators,
    FuGPolarities,
    FuGReadbackChannels,
    FuGMonitorModes,
    FuGRampModes,
)
from .heinzinger import (  # noqa: F401
    HeinzingerDI,
    HeinzingerPNC,
    HeinzingerConfig,
    HeinzingerPNCError,
    HeinzingerPNCMaxVoltageExceededException,
    HeinzingerPNCMaxCurrentExceededException,
    HeinzingerPNCDeviceNotRecognizedException,
    HeinzingerSerialCommunication,
    HeinzingerSerialCommunicationConfig,
)

try:
    from .labjack import (  # noqa: F401
        LabJack,
        LabJackError,
        LabJackIdentifierDIOError,
    )
except (ImportError, ModuleNotFoundError):
    import warnings

    warnings.warn("To use labjack library install hvl with command "
                  "`pip install hvl_ccb[labjack]`.")

from .mbw973 import (  # noqa: F401
    MBW973,
    MBW973Config,
    MBW973ControlRunningException,
    MBW973PumpRunningException,
    MBW973Error,
    MBW973SerialCommunication,
    MBW973SerialCommunicationConfig,
)
from .newport import (  # noqa: F401
    NewportSMC100PP,
    NewportSMC100PPConfig,
    NewportStates,
    NewportSMC100PPSerialCommunication,
    NewportSMC100PPSerialCommunicationConfig,
    NewportConfigCommands,
    NewportMotorError,
    NewportControllerError,
    NewportSerialCommunicationError,
    NewportUncertainPositionError,
    NewportMotorPowerSupplyWasCutError,
)
from .pfeiffer_tpg import (  # noqa: F401
    PfeifferTPG,
    PfeifferTPGConfig,
    PfeifferTPGSerialCommunication,
    PfeifferTPGSerialCommunicationConfig,
    PfeifferTPGError,
)
from .rs_rto1024 import (  # noqa: F401
    RTO1024,
    RTO1024Error,
    RTO1024Config,
    RTO1024VisaCommunication,
    RTO1024VisaCommunicationConfig,
)
from .se_ils2t import (  # noqa: F401
    ILS2T,
    ILS2TConfig,
    ILS2TException,
    ILS2TModbusTcpCommunication,
    ILS2TModbusTcpCommunicationConfig,
    IoScanningModeValueError,
    ScalingFactorValueError,
)
from .sst_luminox import (  # noqa: F401
    Luminox,
    LuminoxConfig,
    LuminoxSerialCommunication,
    LuminoxSerialCommunicationConfig,
    LuminoxMeasurementType,
    LuminoxMeasurementTypeError,
    LuminoxOutputMode,
    LuminoxOutputModeError,
)
from .technix import (  # noqa: F401
    Technix,
    TechnixError,
    TechnixTelnetCommunication,
    TechnixSerialCommunication,
)
from .visa import (  # noqa: F401
    VisaDevice,
    VisaDeviceConfig,
)

if sys.platform == 'darwin':
    import warnings

    warnings.warn("libtiepie is not available for Darwin OSs")
else:
    try:
        from .tiepie.generator import (  # noqa: F401
            TiePieGeneratorConfig,
            TiePieGeneratorSignalType,
            TiePieGeneratorMixin,
        )
        from .tiepie.i2c import (  # noqa: F401
            TiePieI2CHostConfig,
            TiePieI2CHostMixin,
        )
        from .tiepie.oscilloscope import (  # noqa: F401
            TiePieOscilloscope,
            TiePieOscilloscopeConfig,
            TiePieOscilloscopeResolution,
            TiePieOscilloscopeAutoResolutionModes,
        )
        from .tiepie.base import (  # noqa: F401
            TiePieDeviceConfig,
            TiePieDeviceType,
            TiePieError,
            get_device_by_serial_number,
            _verify_via_libtiepie,
        )
        from .tiepie.channel import (  # noqa: F401
            TiePieOscilloscopeChannelCoupling,
            TiePieOscilloscopeChannelConfig,
            TiePieOscilloscopeRange,
            TiePieOscilloscopeTriggerKind,
            TiePieOscilloscopeTriggerLevelMode,
        )
        from .tiepie.device import (  # noqa: F401
            TiePieHS5,
            TiePieHS6,
            TiePieWS5,
        )
    except (ImportError, ModuleNotFoundError):
        import warnings

        warnings.warn("To use libtiepie library install hvl with command "
                      "`pip install hvl_ccb[tiepie]`.")
