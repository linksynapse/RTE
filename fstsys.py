import threading
import time
import eAccountsyc as EASys
import eHistorysyc as EHSys
import terminal as term
#import terminal as tm

lock = threading.Lock()
#x = threading.Thread(target=EASys.eAccountsycExec, args=[lock,])
#y = threading.Thread(target=EHSys.eHistorysycExec, args=[lock,])
z = threading.Thread(target=term.Read, args=[lock,])

try:
    z.start()

    while True:
        print('Start Sync Account')
        EASys.eAccountsycExec(lock)
        print('start sync History')
        EHSys.eHistorysycExec(lock)
        #x.start()
        #y.start()
        time.sleep(30)

except:
    time.sleep(15)