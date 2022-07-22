#omar abuali 11923947
#amr shekha 11923707
#------------there is two defferent codes inside the file---------

import random
import threading
import queue

from threading import Lock, Condition
import time
import numpy as np

buffer_size = 6
buffer = [-1 for i in range(buffer_size)]
in_buffer = 0
out_buffer = 0
mutex = threading.Semaphore()
full = threading.Semaphore(buffer_size)
empty = threading.Semaphore(0)


def mean():
    global buffer_size, buffer, in_buffer, out_buffer
    global mutex, empty, full  # this functions for testing if its full or empty
    work_list = np.random.randint(1, 6, 5)  # this the list makes randoms numbers
    print(work_list)
    enter_numbers = 0
    counter = 0

    while enter_numbers < 6:
        empty.acquire()
        mutex.acquire()

        counter += 1
        buffer[in_buffer] = counter
        in_buffer = (in_buffer + 1) % buffer_size
        print("data produced : ", counter)

        mutex.release()
        full.release()
        time.sleep(1)
        enter_numbers += 1


def switch(condition, lock):
    global buffer_size, buffer, in_buffer, out_buffer
    global mutex, empty, full
    out_numbers = 0

    while out_numbers < 5:
        lock.acquire()
        full.acquire()
        mutex.acquire()
        time.sleep(2)
        print("sending data....!")
        item = buffer[out_buffer]
        out_numbers = (out_buffer + 1) % buffer_size
        print("items :", item)
        mutex.release()
        empty.release()
        lock.release()
        time.sleep(1)
        out_numbers += 1
        with condition:  # notify_all threads
            condition.notify()  # notify all threads waiting on the condition


lock = Lock()
condition = Condition()
print("main thread waiting for data....!")
with condition:
    for i in range(5):  # for create five switches
        t = threading.Thread(name="Switch", target=mean)
        t.start()
        print(f"{t.name} number {i} created")
        condition.wait()
#--------------------------from here start the second solution we dont know wich one is True------------------------

global mlist
global slist
global size

size = 20
lock = Lock()
slist = []
mlist = []

lock = threading.Lock()
def switchmain(lock):
    global slist, mlistm, size
    mlist = [1, 2, 3, 4, 5]
    slist = []

    while True:
            for x in range(size):
                if int(x) in mlist:
                    time.sleep(1)
                    slist.insert(x, x)
                    print("after add the number =" ,slist)
                    time.sleep(0.5)
                    if len(slist) == 5:
                        slist.remove(x)
                        print("after delete random nubmer : " ,slist)
                        time.sleep(0.9)
                with condition:  # notify_all threads
                    condition.notify_all()


lock = Lock()
condition = Condition()
with condition:
    for i in range(5):
        s = threading.Thread(target=switchmain, args=(lock,))
        s.start()
        s.join()
        condition.wait()
