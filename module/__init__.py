from module import Accessories
from module import Config
from module import Data
from module import Log4s
from module import Native
from module import R3api
from module import RfidReader

CONF = Config.Config()
A22S = Accessories.Accessories(CONF)
DATA = Data.Manager(CONF)
LOG4S = Log4s.Log4s(CONF)
API = R3api.R3api(CONF)
RFRD = RfidReader.RfidReader(CONF)

NT_SYS_CPUID = Native.GetCPUID()
NT_SYS_PUBIP = Native.GetPublicIPaddress()
NT_SYS_NATIP = Native.GetNATIPaddress()
NT_SYS_HOSTN = Native.GetHostName()