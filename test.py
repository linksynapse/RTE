import Data
import Config
import SyS

config = Config.Config("Config/sys.conf")

Dao = Data.Manager(config)

print(SyS.GetCPUID())