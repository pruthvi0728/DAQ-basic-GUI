import tkinter as tk
# from tkinter import messagebox
import threading
from datetime import time, datetime, timedelta

mt = tk.Tk()
mt.title("Time")
running = False
remaining_time = 0


def remain(e2):
    # remaining time display
    def rem():
        if running:
            global remaining_time
            if remaining_time != 0:
                print(remaining_time)
                remaining_time = remaining_time - 1
                e2.delete(0, tk.END)
                rem_time = timedelta(seconds=remaining_time)
                e2.insert(0, rem_time)
                e2.after(1000, rem)
            else:
                stop()
    rem()


def start(e2):
    global remaining_time
    global running
    running = True
    # calculation for remaining time
    stime = datetime.strptime(e1.get(), '%H:%M:%S').time()
    remaining_time = int(timedelta(hours=stime.hour, minutes=stime.minute, seconds=stime.second).total_seconds())
    remain(e2)
    Btn['state'] = 'disable'
    Btnstp['state'] = 'normal'


def stop():
    global running
    Btn['state'] = 'normal'
    Btnstp['state'] = 'disable'
    running = False


tk.Label(mt, text="Set Time").grid(row=0)
e1 = tk.Entry(mt)
e1.insert(0, str(time()))
e1.grid(row=0, column=1)

tk.Label(mt, text="remaining").grid(row=1)
e2 = tk.Entry(mt)
e2.grid(row=1, column=1)

Btn = tk.Button(mt, text="Start", command=lambda: start(e2))
Btn.grid(row=2, column=1)

Btnstp = tk.Button(mt, text="Stop", command=stop, state='disable')
Btnstp.grid(row=2, column=2)
mt.mainloop()
