import tkinter as tk
from datetime import time, datetime, timedelta


mt = tk.Tk()
mt.title("Toggle")


class ToggleDO:

    def __init__(self, btndo, gpio):
        self.btndo = btndo
        self.gpio = gpio
        self.btndo.config(command=self.toggle)

    def toggle(self):
        if self.btndo.config('text')[-1] == 'ON':
            self.btndo.config(text='OFF')
            print(str(self.gpio) + ' OFF')
            # GPIO.output(25, GPIO.LOW)
        else:
            self.btndo.config(text='ON')
            print(str(self.gpio) + ' ON')
            # GPIO.output(25, GPIO.HIGH)


class Remaining:
    def __init__(self, entry1, entry2, btnstart, btnstop, btndo, gpio):
        self.running = False
        self.remaining_time = 0
        self.entry1 = entry1
        self.entry2 = entry2
        self.btnstart = btnstart
        self.btnstop = btnstop
        self.btnstart.config(command=lambda: self.start())
        self.btnstop.config(command=self.stop)

        self.btndo = btndo
        self.gpio = gpio
        self.tdo = ToggleDO(self.btndo, self.gpio)

    def remain(self):
        # remaining time display
        def rem():
            if self.running:
                if self.remaining_time != 0:
                    self.remaining_time = self.remaining_time - 1
                    self.entry2.delete(0, tk.END)
                    rem_time = timedelta(seconds=self.remaining_time)
                    self.entry2.insert(0, rem_time)
                    self.entry2.after(1000, rem)
                else:
                    self.stop()
        rem()

    def start(self):
        self.running = True
        # calculation for remaining time
        stime = datetime.strptime(self.entry1.get(), '%H:%M:%S').time()
        self.remaining_time = int(timedelta(hours=stime.hour, minutes=stime.minute, seconds=stime.second).total_seconds())
        self.remain()
        self.btnstart['state'] = 'disable'
        self.btnstop['state'] = 'normal'
        self.btndo['state'] = 'disable'
        if self.btndo.config('text')[-1] == 'ON' or self.btndo.config('text')[-1] == 'OFF':
            self.btndo.config(text='ON')
            print(str(self.gpio) + ' ON')
            # GPIO.output(25, GPIO.HIGH)

    def stop(self):
        self.btnstart['state'] = 'normal'
        self.btnstop['state'] = 'disable'
        self.running = False
        self.btndo['state'] = 'normal'
        if self.btndo.config('text')[-1] == 'ON' or self.btndo.config('text')[-1] == 'OFF':
            self.btndo.config(text='OFF')
            print(str(self.gpio) + ' OFF')
            # GPIO.output(25, GPIO.LOW)


# This is for DO button 1
tk.Label(mt, text="DO 1").grid(column=0, row=1, padx=10, pady=10)
do1 = tk.Button(mt, text="OFF", width=12)
do1.grid(row=1, column=1)
# tdo1 = ToggleDO(do1, gpio=25)

# this is for Time
tk.Label(mt, text="Set Time").grid(row=1, column=2)
e1 = tk.Entry(mt)
e1.insert(0, str(time()))
e1.grid(row=1, column=3)

Btn1 = tk.Button(mt, text="Start")
Btn1.grid(row=1, column=4)

tk.Label(mt, text="remaining").grid(row=1, column=5)
e2 = tk.Entry(mt)
e2.grid(row=1, column=6)

Btnstp1 = tk.Button(mt, text="Stop", state='disable')
Btnstp1.grid(row=1, column=7)
rem = Remaining(e1, e2, Btn1, Btnstp1, do1, gpio=25)



# this is for DO button 2
tk.Label(mt, text="DO 2").grid(column=0, row=2, padx=10, pady=10)
do2 = tk.Button(mt, text="OFF", width=12)
do2.grid(row=2, column=1)
#tdo2 = ToggleDO(do2, gpio=17)

# this is for Time 2
tk.Label(mt, text="Set Time").grid(row=2, column=2)
e11 = tk.Entry(mt)
e11.insert(0, str(time()))
e11.grid(row=2, column=3)

Btn2 = tk.Button(mt, text="Start")
Btn2.grid(row=2, column=4)

tk.Label(mt, text="remaining").grid(row=2, column=5)
e21 = tk.Entry(mt)
e21.grid(row=2, column=6)

Btnstp2 = tk.Button(mt, text="Stop", state='disable')
Btnstp2.grid(row=2, column=7)
rem1 = Remaining(e11, e21, Btn2, Btnstp2, do2, gpio=17)

# Main Loop
mt.mainloop()
