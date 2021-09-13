import threading
import eAccountsyc as EASys
import eHistorysyc as EHSys
#import terminal as tm

lock = threading.Lock()
x = threading.Thread(target=EASys.eAccountsycExec, args=[lock,])
y = threading.Thread(target=EHSys.eHistorysycExec, args=[lock,])
x.start()
y.start()