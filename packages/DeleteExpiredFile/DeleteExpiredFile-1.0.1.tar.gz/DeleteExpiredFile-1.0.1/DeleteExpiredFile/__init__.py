import os
import time
#from datetime import datetime as dt
import threading

def task(extentions,maxKeepHR):
    '''
    task(extentions,maxKeepHR)
    Ex:
    task(['.txt','.mp4'],0.05)
    ==>keep .txt and .mp4 files in 0.05Hr(3 minute) , delete the others
    
    '''
    for f in os.listdir():
        for ext in extentions:
            if f.find(ext)>=0:
                #mtime = time.ctime(os.path.getmtime(f))
                #ctime = time.ctime(os.path.getctime(f))
                keepHR = (time.time()-os.path.getmtime(f))/3600
                if  keepHR > maxKeepHR:
                    try:
                        os.remove(f)
                        print(f,'removed..')
                    except:print('io exception occured while remove file...')
def Routine(extentions,maxKeepHR,checkDuration=3):
    '''
    Routine(extentions,maxKeepHR,checkDuration)
    Ex:
    Routine(['.txt','.mp4'],0.05,5)
    
    1.keep .txt and .mp4 files in 0.05Hr(3 minute) , delete the others
    2.check every 5 sec ==>loop forever
    '''
    while True:
        task(extentions,maxKeepHR)
        time.sleep(checkDuration)
        
def Asyn(extentions,maxKeepHR,checkDuration):
    '''
    Asyn(extentions,maxKeepHR,checkDuration)
    Ex:
    t=Asyn(['.txt','.mp4'],0.05,5)
    #t.join() .... wait for the thead in main process
    
    1.keep .txt and .mp4 files in 0.05Hr(3 minute) , delete the others
    2.check every 5 sec
    3.execute asynchronously and return the thread
    '''
    t = threading.Thread(target = Routine,args=(extentions,maxKeepHR,checkDuration,))
    t.start()
    return t

                
#print("start...")
#extentions = ['.txt','.mp4']
#Routine(extentions,2)
#t=Asyn(extentions,0.05)
#t.join()