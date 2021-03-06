#!/usr/bin/python3

import time
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import datetime as dt
import csv
from ttkthemes import ThemedStyle

import Adafruit_MCP4725
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BCM)

doPinlist = [25, 17, 18, 27, 22, 23, 24, 10]
diPinlist = [5, 6, 13, 19, 26, 16, 20, 21]
di_data = [0, 0, 0, 0, 0, 0, 0, 0]

for i in doPinlist:
    GPIO.setup(i, GPIO.OUT)
    GPIO.output(i, GPIO.LOW)

for i in diPinlist:
    GPIO.setup(i, GPIO.IN)

serial_data = ""
filter_data = ""
update_period = 5
serial_object = None
main = Tk()
main.title("Citriot DAQ")

# Setting Theme
style = ThemedStyle(main)
# style.set_theme("breeze")
style.set_theme("radiance")


class ToggleDO:
    def __init__(self, btndo, gpio):
        self.btndo = btndo
        self.gpio = gpio
        self.btndo.config(command=self.toggle)

    def toggle(self):
        if self.btndo.config("text")[-1] == "ON":
            self.btndo.config(text="OFF")
            # print(str(self.gpio) + " OFF")
            GPIO.output(self.gpio, GPIO.LOW)
        else:
            self.btndo.config(text="ON")
            # print(str(self.gpio) + " ON")
            GPIO.output(self.gpio, GPIO.HIGH)


class Remaining:
    def __init__(self, entry1, entry2, btnstart, btnstop, btndo, gpio):
        self.running = False
        self.remaining_time = 0
        self.entry1 = entry1
        self.entry2 = entry2
        self.btnstart = btnstart
        self.btnstop = btnstop
        self.btnstart.config(command=lambda: self.start(r=0))
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
                    rem_time = dt.timedelta(seconds=self.remaining_time)
                    self.entry2.insert(0, rem_time)
                    self.entry2.after(1000, rem)
                else:
                    self.stop()

        rem()

    def remain_new(self):
        def rem():
            if self.running:
                if self.remaining_time != 0:
                    self.remaining_time = self.remaining_time - 1
                    rem_time = dt.timedelta(seconds=self.remaining_time)
                    self.entry2.delete(0, tk.END)
                    self.entry2.insert(0, rem_time)
                    main.update()
                    time.sleep(1)
                    rem()
                else:
                    self.stop()

        rem()

    def start(self, r):
        self.running = True
        # calculation for remaining time
        try:
            if self.entry1.get() == "00:00:00":
                raise ValueError()
            stime = dt.datetime.strptime(self.entry1.get(), "%H:%M:%S").time()
            self.remaining_time = int(
                dt.timedelta(
                    hours=stime.hour, minutes=stime.minute, seconds=stime.second
                ).total_seconds()
            )
            if r:
                self.btnstart["state"] = "disable"
                self.btnstop["state"] = "normal"
                self.btndo["state"] = "disable"

                self.btndo.config(text="ON")
                # self.btnstop['style'] = "stp.TButton"    # button color
                # print(str(self.gpio) + " ON")
                GPIO.output(self.gpio, GPIO.HIGH)
                self.remain_new()
            else:
                self.remain()
                self.btnstart["state"] = "disable"
                self.btnstop["state"] = "normal"
                self.btndo["state"] = "disable"
                # self.btnstop['style'] = "stp.TButton"    # button color
                self.btndo.config(text="ON")
                # print(str(self.gpio) + " ON")
                GPIO.output(self.gpio, GPIO.HIGH)
        except ValueError:
            messagebox.showinfo("Error", "Enter value in non zero hh:mm:ss format only")
        except:
            messagebox.showinfo("Error", "Something went wrong")

    def stop(self):
        self.btnstart["state"] = "normal"
        self.btnstop["state"] = "disable"
        self.running = False
        self.btndo["state"] = "normal"
        self.btndo.config(text="OFF")
        # self.btnstop['style'] = "Instp.TButton"
        # print(str(self.gpio) + " OFF")
        GPIO.output(self.gpio, GPIO.LOW)


class CheckBox(Remaining):
    def __init__(self, entry1, entry2, btnstart, btnstop):
        self.running = False
        self.remaining_time = 0
        self.entry1 = entry1
        self.entry2 = entry2
        self.btnstart = btnstart
        self.btnstop = btnstop
        self.btnstart.config(command=lambda: self.start())
        self.btnstop.config(command=self.stop)

    def start(self):
        self.running = True
        # calculation for remaining time
        try:
            if self.entry1.get() == "00:00:00":
                raise ValueError()
            stime = dt.datetime.strptime(self.entry1.get(), "%H:%M:%S").time()
            self.remaining_time = int(
                dt.timedelta(
                    hours=stime.hour, minutes=stime.minute, seconds=stime.second
                ).total_seconds()
            )
            self.remain()
            self.btnstart["state"] = "disable"
            self.btnstop["state"] = "normal"
            if cb1.get() == 1:
                self.btnctrl(Btn1, Btnstp1, do1, dis=1)
                self.dobtnctrl(do1, gpio=25, flag=1)
            if cb2.get() == 1:
                self.btnctrl(Btn2, Btnstp2, do2, dis=1)
                self.dobtnctrl(do2, gpio=17, flag=1)
            if cb3.get() == 1:
                self.btnctrl(Btn3, Btnstp3, do3, dis=1)
                self.dobtnctrl(do3, gpio=18, flag=1)
            if cb4.get() == 1:
                self.btnctrl(Btn4, Btnstp4, do4, dis=1)
                self.dobtnctrl(do4, gpio=27, flag=1)
            if cb5.get() == 1:
                self.btnctrl(Btn5, Btnstp5, do5, dis=1)
                self.dobtnctrl(do5, gpio=22, flag=1)
            if cb6.get() == 1:
                self.btnctrl(Btn6, Btnstp6, do6, dis=1)
                self.dobtnctrl(do6, gpio=23, flag=1)
            if cb7.get() == 1:
                self.btnctrl(Btn7, Btnstp7, do7, dis=1)
                self.dobtnctrl(do7, gpio=24, flag=1)
            if cb8.get() == 1:
                self.btnctrl(Btn8, Btnstp8, do8, dis=1)
                self.dobtnctrl(do8, gpio=10, flag=1)
        except ValueError:
            messagebox.showinfo("Error", "Enter value in non zero hh:mm:ss format only")
        except:
            messagebox.showinfo("Error", "Something went wrong")

    def dobtnctrl(self, btncdo, gpio, flag):
        if flag:
            btncdo.config(text="ON")
            # print(str(gpio) + " ON")
            GPIO.output(gpio, GPIO.HIGH)
        else:
            btncdo.config(text="OFF")
            # print(str(gpio) + " OFF")
            GPIO.output(gpio, GPIO.LOW)

    def stop(self):
        self.btnstart["state"] = "normal"
        self.btnstop["state"] = "disable"
        self.running = False
        if cb1.get() == 1:
            self.btnctrl(Btn1, Btnstp1, do1, dis=0)
            self.dobtnctrl(do1, gpio=25, flag=0)
        if cb2.get() == 1:
            self.btnctrl(Btn2, Btnstp2, do2, dis=0)
            self.dobtnctrl(do2, gpio=17, flag=0)
        if cb3.get() == 1:
            self.btnctrl(Btn3, Btnstp3, do3, dis=0)
            self.dobtnctrl(do3, gpio=18, flag=0)
        if cb4.get() == 1:
            self.btnctrl(Btn4, Btnstp4, do4, dis=0)
            self.dobtnctrl(do4, gpio=27, flag=0)
        if cb5.get() == 1:
            self.btnctrl(Btn5, Btnstp5, do5, dis=0)
            self.dobtnctrl(do5, gpio=22, flag=0)
        if cb6.get() == 1:
            self.btnctrl(Btn6, Btnstp6, do6, dis=0)
            self.dobtnctrl(do6, gpio=23, flag=0)
        if cb7.get() == 1:
            self.btnctrl(Btn7, Btnstp7, do7, dis=0)
            self.dobtnctrl(do7, gpio=24, flag=0)
        if cb8.get() == 1:
            self.btnctrl(Btn8, Btnstp8, do8, dis=0)
            self.dobtnctrl(do8, gpio=10, flag=0)

    def btnctrl(self, btncs, btncstp, btncdo, dis):
        if dis:
            btncs["state"] = "disable"
            btncstp["state"] = "disable"
            btncdo["state"] = "disable"
        else:
            btncs["state"] = "normal"
            btncstp["state"] = "normal"
            btncdo["state"] = "normal"


class AOcontrol:
    def __init__(
        self,
        aominvolt,
        aominramptime,
        aominholdtime,
        aosetcycle,
        aostart,
        aomaxvolt,
        aomaxramptime,
        aomaxholdtime,
        aoremaincycle,
        aostop,
        dec,
    ):
        self.aominvolt = aominvolt
        self.aominramptime = aominramptime
        self.aominholdtime = aominholdtime
        self.aosetcycle = aosetcycle
        self.aomaxvolt = aomaxvolt
        self.aomaxramptime = aomaxramptime
        self.aomaxholdtime = aomaxholdtime
        self.aoremaincycle = aoremaincycle
        self.aostart = aostart
        self.aostop = aostop
        self.dec = dec
        self.running = False
        self.running_ok = True
        self.running_cycle = False
        self.remaining = 0
        self.remaining_time = 0
        self.dec.set_voltage(0)
        # self.AOTrd = threading.Thread(target=self.start)  # +++++++++++
        # self.AOTrd.daemon = True
        # self.aostart.config(command=lambda: self.AOTrd.start())  # ++++++++++
        self.aostart.config(command=lambda: self.start())
        self.aostop.config(command=self.stop)

    def remain_cycle_new(self):
        try:
            for self.r in range(self.remaining):
                if self.running_cycle:
                    self.rem_time = self.remaining - self.r - 1
                    self.aoremaincycle.delete(0, tk.END)
                    self.aoremaincycle.insert(0, self.rem_time)
                    main.update()
                    self.setdec()
                else:
                    break
        finally:
            self.stop()

    def start(self):
        self.running_cycle = True
        self.aostart["state"] = "disable"
        self.aostop["state"] = "normal"
        self.remaining = int(self.aosetcycle.get())
        self.AOTrd = threading.Thread(target=self.remain_cycle_new)  # --------
        self.AOTrd.start()  # ----------
        # self.remain_cycle_new() # +++++++++++++

    def stop(self):
        self.running_cycle = False
        self.aostart["state"] = "normal"
        self.aostop["state"] = "disable"
        self.setdecstp()

    def remain_new(self):
        def rem():
            if self.running:
                if self.remaining_time != 0:
                    self.remaining_time = self.remaining_time - 1
                    main.update()
                    time.sleep(1)
                    rem()
                else:
                    self.setstp_remain_new()

        rem()

    def setstp_remain_new(self):
        self.running = False
        # print("Loop Stoped")

    def setdec(self):
        self.running_ok = True
        try:
            if self.validate(self.aominvolt) and self.validate(self.aomaxvolt):
                if (
                    self.aominramptime.get() == "00:00:00"
                    and self.aominholdtime.get() == "00:00:00"
                ):
                    raise ValueError()
                if (
                    self.aomaxramptime.get() == "00:00:00"
                    and self.aomaxholdtime.get() == "00:00:00"
                ):
                    raise ValueError()

                aominholdtime = dt.datetime.strptime(
                    self.aominholdtime.get(), "%H:%M:%S"
                ).time()

                self.remaining_time = int(
                    dt.timedelta(
                        hours=aominholdtime.hour,
                        minutes=aominholdtime.minute,
                        seconds=aominholdtime.second,
                    ).total_seconds()
                )

                self.running = True
                if self.running_ok:
                    self.minvoltramp()

                # print("Min Volt hold start")
                if self.running_ok:
                    self.remain_new()
                # print("Min Volt hold stop")

                self.running = True

                if self.running_ok:
                    self.maxvoltramp()

                aomaxholdtime = dt.datetime.strptime(
                    self.aomaxholdtime.get(), "%H:%M:%S"
                ).time()

                self.remaining_time = int(
                    dt.timedelta(
                        hours=aomaxholdtime.hour,
                        minutes=aomaxholdtime.minute,
                        seconds=aomaxholdtime.second,
                    ).total_seconds()
                )

                # print("Max Volt hold start")
                if self.running_ok:
                    self.remain_new()
                # print("Max Volt hold stop")
        except ValueError:
            messagebox.showinfo("Error", "Enter value in non zero hh:mm:ss format only")
        except:
            messagebox.showinfo("Error", "Something went wrong")

    def minvoltramp(self):
        if self.running:
            # print("Min Volt Ramp")
            self.get_aominramptime = dt.datetime.strptime(
                self.aominramptime.get(), "%H:%M:%S"
            ).time()
            self.minvoltramp_total = int(
                dt.timedelta(
                    hours=self.get_aominramptime.hour,
                    minutes=self.get_aominramptime.minute,
                    seconds=self.get_aominramptime.second,
                ).total_seconds()
            )
            # min volt -----------------
            self.minvoltramp_volt = round(float(self.aominvolt.get()), 2)
            self.minvoltramp_incvolt = self.minvoltramp_volt / self.minvoltramp_total
            self.minvoltramp_tmp_volt = 0
            while self.minvoltramp_tmp_volt <= self.minvoltramp_volt:
                if self.running:
                    self.minvoltramp_xdec = int(
                        (self.minvoltramp_tmp_volt / 5.11) * 4096
                    )
                    self.dec.set_voltage(self.minvoltramp_xdec)
                    # print(self.minvoltramp_tmp_volt, self.minvoltramp_xdec)
                    main.update()
                    time.sleep(1)
                    self.minvoltramp_tmp_volt += self.minvoltramp_incvolt
                else:
                    break

    def maxvoltramp(self):
        if self.running:
            # print("Max Volt Ramp")
            self.get_aomaxramptime = dt.datetime.strptime(
                self.aomaxramptime.get(), "%H:%M:%S"
            ).time()
            self.maxvoltramp_ramp_total = int(
                dt.timedelta(
                    hours=self.get_aomaxramptime.hour,
                    minutes=self.get_aomaxramptime.minute,
                    seconds=self.get_aomaxramptime.second,
                ).total_seconds()
            )
            # max volt -----------------
            self.maxvoltramp_minvolt = round(float(self.aominvolt.get()), 2)
            self.maxvoltramp_volt = round(float(self.aomaxvolt.get()), 2)
            self.maxvoltramp_incvolt = (
                self.maxvoltramp_volt - self.maxvoltramp_minvolt
            ) / self.maxvoltramp_ramp_total
            self.maxvoltramp_tmp_volt = self.maxvoltramp_minvolt
            while self.maxvoltramp_tmp_volt <= self.maxvoltramp_volt:
                if self.running:
                    self.maxvoltramp_xdec = int(
                        (self.maxvoltramp_tmp_volt / 5.11) * 4096
                    )
                    self.dec.set_voltage(self.maxvoltramp_xdec)
                    # print(self.maxvoltramp_tmp_volt, self.maxvoltramp_xdec)
                    main.update()
                    time.sleep(1)
                    self.maxvoltramp_tmp_volt += self.maxvoltramp_incvolt
                else:
                    break

    def setdecstp(self):
        self.running = False
        self.running_ok = False
        self.dec.set_voltage(0)
        # print("stop 0")

    def validate(self, entry):
        try:
            self.volt = float(entry.get())
            if self.volt < 0 or self.volt > 5:
                messagebox.showinfo("Error", "Voltage only between 0 to 5")
                return False
            else:
                return True
        except ValueError:
            messagebox.showinfo("Error", "Voltage only between 0 to 5")
            return False


class Cycle:
    def __init__(self, entry1, entry2, btnstart, btnstop):
        self.entry1 = entry1
        self.entry2 = entry2
        self.remaining = 0
        self.btnstart = btnstart
        self.btnstop = btnstop
        self.running = False
        self.btnstart.config(command=lambda: self.start())
        self.btnstop.config(command=self.stop)

    def remain_new(self):
        cy = [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8]
        re = [rem1, rem2, rem3, rem4, rem5, rem6, rem7, rem8]

        for r in range(self.remaining):
            if self.running:
                rem_time = self.remaining - r - 1
                self.entry2.delete(0, tk.END)
                self.entry2.insert(0, rem_time)
                main.update()
                i = 0
                for c in cy:
                    if self.running:
                        if c.get() == 1:
                            re[i].start(r=1)
                        i += 1
                    else:
                        break
            else:
                break

    def start(self):
        self.running = True
        # Btng['state'] = 'disable'
        self.btnstart["state"] = "disable"
        self.btnstop["state"] = "normal"
        self.remaining = int(self.entry1.get())
        self.remain_new()
        self.stop()

    def stop(self):
        self.running = False
        # Btng['state'] = 'normal'
        self.btnstart["state"] = "normal"
        self.btnstop["state"] = "disable"
        cy = [cb1, cb2, cb3, cb4, cb5, cb6, cb7, cb8]
        re = [rem1, rem2, rem3, rem4, rem5, rem6, rem7, rem8]
        for r, c in zip(re, cy):
            if c.get() == 1:
                r.stop()


# gives weight to the cells in the grid
rows = 0
while rows < 50:
    main.rowconfigure(rows, weight=1)
    main.columnconfigure(rows, weight=1)
    rows += 1


def connect():
    """The function initiates the Connection to the UART device with the Port and Buad fed through the Entry
    boxes in the application.
    The radio button selects the platform, as the serial object has different key phrases
    for Linux and Windows. Some Exceptions have been made to prevent the app from crashing,
    such as blank entry fields and value errors, this is due to the state-less-ness of the
    UART device, the device sends data at regular intervals irrespective of the master's state.
    The other Parts are self explanatory.
    """

    version_ = button_var.get()

    global serial_object
    global csvfilename

    baud = 9600
    try:
        serial_object = serial.Serial("/dev/ttyACM0", baud)

    except:
        print("Can't open port ACM0")

    # For File Creating Whenever click on Connect
    nowfile = dt.datetime.now()
    csvfilename = (
        "CITRIOT_DATASHEET_" + str(nowfile.strftime("%Y_%b_%d_%H_%M_%S")) + ".csv"
    )

    try:
        with open(
            "/home/pi/Desktop/DATASHEET/" + csvfilename, "w", newline=""
        ) as datafile:
            writer = csv.writer(datafile)
            writer.writerow(
                [
                    "Timestamp",
                    "Thermocouple_1",
                    "Thermocouple_2",
                    "Thermocouple_3",
                    "Thermocouple_4",
                    "Thermocouple_5",
                    "Thermocouple_6",
                    "Thermocouple_7",
                    "Thermocouple_8",
                    "Analog_1",
                    "Analog_2",
                    "Analog_3",
                    "Analog_4",
                    "Analog_5",
                    "Analog_6",
                    "Analog_7",
                    "Analog_8",
                    "Digital_1",
                    "Digital_2",
                    "Digital_3",
                    "Digital_4",
                    "Digital_5",
                    "Digital_6",
                    "Digital_7",
                    "Digital_8",
                ]
            )

            messagebox.showinfo("Data", "Data is Saving...")
    except:
        messagebox.showinfo("Error", "Something went wrong in file creation")

    # connectbtn['state'] = 'disable'
    # disconnectbtn['state'] = 'normal'

    t1 = threading.Thread(target=get_data)
    t1.daemon = True
    t1.start()


def get_data():
    """This function serves the purpose of collecting data from the serial object and storing
    the filtered data into a global variable.
    The function has been put into a thread since the serial event is a blocking function.
    """
    global serial_object
    global filter_data
    global di_data
    global csvfilename
    # di_data = [0, 0, 0, 0, 0, 0, 0, 0]
    while 1:
        try:
            serial_data = serial_object.readline()
            serial_data = serial_data.decode("utf-8")
            serial_data.rstrip("\r\n")
            # serial_data = serial_object.readline()

            filter_data = serial_data.split(",")
            for i in range(len(filter_data)):
                if float(filter_data[i]) > 500.00 or float(filter_data[i]) == 0:
                    filter_data[i] = "NAN"

            for i in range(len(diPinlist)):
                di_data[i] = GPIO.input(diPinlist[i])
                if di_data[i] == 1:
                    di_data[i] = "OFF"
                else:
                    di_data[i] = "ON"

            filter_data[15], filter_data[14], filter_data[13], filter_data[12] = (
                filter_data[12],
                filter_data[13],
                filter_data[14],
                filter_data[15],
            )
            # print(filter_data)
            datatimestamp = [str(dt.datetime.now())]
            datasave = datatimestamp + filter_data[:16] + di_data

            try:
                with open(
                    "/home/pi/Desktop/DATASHEET/" + csvfilename, "a", newline=""
                ) as datafile:
                    writer = csv.writer(datafile)
                    writer.writerow(datasave)
            except:
                messagebox.showinfo("Error", "Something went wrong in data storing")

        except TypeError:
            pass


def update_main():
    """" This function is an update function which is also threaded. The function assimilates the data
    and applies it to it corresponding progress bar. The text box is also updated every couple of seconds.
    A simple auto refresh function .after() could have been used, this has been avoid purposely due to
    various performance issues.
    """
    global filter_data
    global update_period
    global di_data

    # thermocouple component packing(label: text)
    thermocoupleText1.grid(column=2, row=1)
    thermocoupleText2.grid(column=2, row=2)
    thermocoupleText3.grid(column=2, row=3)
    thermocoupleText4.grid(column=2, row=4)
    thermocoupleText5.grid(column=2, row=5)
    thermocoupleText6.grid(column=2, row=6)
    thermocoupleText7.grid(column=2, row=7)
    thermocoupleText8.grid(column=2, row=8)

    diText1.grid(column=2, row=1)
    diText2.grid(column=2, row=2)
    diText3.grid(column=2, row=3)
    diText4.grid(column=2, row=4)
    diText5.grid(column=2, row=5)
    diText6.grid(column=2, row=6)
    diText7.grid(column=2, row=7)
    diText8.grid(column=2, row=8)

    new = time.time()
    global var
    while 1:
        if filter_data:

            var = 0
            var = filter_data[0]
            thermocoupleText1.config(text=filter_data[0])
            thermocoupleText2.config(text=filter_data[1])
            thermocoupleText3.config(text=filter_data[2])
            thermocoupleText4.config(text=filter_data[3])
            thermocoupleText5.config(text=filter_data[4])
            thermocoupleText6.config(text=filter_data[5])
            thermocoupleText7.config(text=filter_data[6])
            thermocoupleText8.config(text=filter_data[7])

            ai1currentvolt.config(text=filter_data[8])
            ai2currentvolt.config(text=filter_data[9])
            ai3currentvolt.config(text=filter_data[10])
            ai4currentvolt.config(text=filter_data[11])
            ai5currentvolt.config(text=filter_data[12])
            ai6currentvolt.config(text=filter_data[13])
            ai7currentvolt.config(text=filter_data[14])
            ai8currentvolt.config(text=filter_data[15])

            try:
                ai1measurevalue.config(
                    text=str(
                        round(
                            (float(ai1maxphy.get()) - float(ai1minphy.get()))
                            * (
                                (float(filter_data[8]) - float(ai1minvolt.get()))
                                / (float(ai1maxvolt.get()) - float(ai1minvolt.get()))
                            )
                            + float(ai1minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai2measurevalue.config(
                    text=str(
                        round(
                            (float(ai2maxphy.get()) - float(ai2minphy.get()))
                            * (
                                (float(filter_data[9]) - float(ai2minvolt.get()))
                                / (float(ai2maxvolt.get()) - float(ai2minvolt.get()))
                            )
                            + float(ai2minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai3measurevalue.config(
                    text=str(
                        round(
                            (float(ai3maxphy.get()) - float(ai3minphy.get()))
                            * (
                                (float(filter_data[10]) - float(ai3minvolt.get()))
                                / (float(ai3maxvolt.get()) - float(ai3minvolt.get()))
                            )
                            + float(ai3minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai4measurevalue.config(
                    text=str(
                        round(
                            (float(ai4maxphy.get()) - float(ai4minphy.get()))
                            * (
                                (float(filter_data[11]) - float(ai4minvolt.get()))
                                / (float(ai4maxvolt.get()) - float(ai4minvolt.get()))
                            )
                            + float(ai4minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai5measurevalue.config(
                    text=str(
                        round(
                            (float(ai5maxphy.get()) - float(ai5minphy.get()))
                            * (
                                (float(filter_data[12]) - float(ai5minvolt.get()))
                                / (float(ai5maxvolt.get()) - float(ai5minvolt.get()))
                            )
                            + float(ai5minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai6measurevalue.config(
                    text=str(
                        round(
                            (float(ai6maxphy.get()) - float(ai6minphy.get()))
                            * (
                                (float(filter_data[13]) - float(ai6minvolt.get()))
                                / (float(ai6maxvolt.get()) - float(ai6minvolt.get()))
                            )
                            + float(ai6minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai7measurevalue.config(
                    text=str(
                        round(
                            (float(ai7maxphy.get()) - float(ai7minphy.get()))
                            * (
                                (float(filter_data[14]) - float(ai7minvolt.get()))
                                / (float(ai7maxvolt.get()) - float(ai7minvolt.get()))
                            )
                            + float(ai7minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")
            try:
                ai8measurevalue.config(
                    text=str(
                        round(
                            (float(ai8maxphy.get()) - float(ai8minphy.get()))
                            * (
                                (float(filter_data[15]) - float(ai8minvolt.get()))
                                / (float(ai8maxvolt.get()) - float(ai8minvolt.get()))
                            )
                            + float(ai8minphy.get()),
                            2,
                        )
                    )
                )
            except ZeroDivisionError as ZDE:
                print(ZDE)
            except ValueError as VE:
                print(VE)
            except:
                print("Something went wrong in calculation of measure value")

            diText1.config(text=di_data[0])
            diText2.config(text=di_data[1])
            diText3.config(text=di_data[2])
            diText4.config(text=di_data[3])
            diText5.config(text=di_data[4])
            diText6.config(text=di_data[5])
            diText7.config(text=di_data[6])
            diText8.config(text=di_data[7])

            if time.time() - new >= update_period:
                new = time.time()


def disconnect():
    """
    This function is for disconnecting and quitting the application.
    Sometimes the application throws a couple of errors while it is being shut down, the fix isn't out yet
    but will be pushed to the repo once done.
    simple main.quit() calls.
    """
    global csvfilename

    try:
        serial_object.close()

    except AttributeError:
        print("Closed without Using it -_-")
    messagebox.showinfo("Data", "Data is Saved on " + csvfilename)
    # disconnectbtn['state'] = 'disable'
    # connectbtn['state'] = 'normal'
    main.quit()


if __name__ == "__main__":
    """
    The main loop consists of all the main objects and its placement.
    The Main loop handles all the widget placements.
    """
    global var
    global csvfilename
    # frames
    # frame_1 = Frame(height=285, width=480, bd=3, relief='groove').place(x=7, y=5)
    # frame_2 = Frame(height=150, width=480, bd=3, relief='groove').place(x=7, y=300)
    nb = ttk.Notebook(main)
    nb.grid(row=1, column=0, columnspan=50, rowspan=49, sticky="NESW")

    # About
    aboutPage = ttk.Frame(nb)
    nb.add(aboutPage, text="About")
    # image = PhotoImage(file="logo.gif")
    # L = Label(aboutPage, image=image).pack()
    ttk.Label(
        aboutPage, text="Citriot Data Acquisition System", font=("Helvetica", 24)
    ).pack(side="top", pady=5)

    try:
        image = Image.open("/home/pi/.DAQ/DAQ-basic-GUI/Logo2.png")
    except Exception:
        image = Image.open(r"C:\Users\Infinity\Desktop\Project\DAQ-basic-GUI\Logo2.png")
    # /home/pi/.DAQ/New/DAQ-basic-GUI/Logo2.png
    # /home/pi/Desktop/New/DAQ-basic-GUI/Logo2.png
    image = image.resize(
        (500, 250), Image.ANTIALIAS
    )  # The (250, 250) is (height, width)
    img = ImageTk.PhotoImage(image)
    panel = ttk.Label(aboutPage, image=img)
    panel.pack(
        pady=17
    )  # , padx=140, pady=50 , expand=True side="bottom", fill=BOTH, expand=True

    # DO
    doPage = ttk.Frame(nb)
    nb.add(doPage, text="Digital Output")

    ttk.Label(doPage, text="Set Time").grid(row=0, column=2)
    ttk.Label(doPage, text="Remaining").grid(row=0, column=4)

    # Creating variable for checkbox
    cb1 = tk.IntVar()
    cb2 = tk.IntVar()
    cb3 = tk.IntVar()
    cb4 = tk.IntVar()
    cb5 = tk.IntVar()
    cb6 = tk.IntVar()
    cb7 = tk.IntVar()
    cb8 = tk.IntVar()

    # DO1 Start
    ttk.Checkbutton(doPage, text="DO 1", variable=cb1).grid(column=0, row=1, padx=10)
    do1 = ttk.Button(doPage, text="OFF", width=5)
    do1.grid(row=1, column=1, padx=10)
    # tk.Label(doPage, text="Set Time").grid(row=1, column=2)
    e1 = ttk.Entry(doPage, width=11)
    e1.insert(0, str("00:00:00"))
    e1.grid(row=1, column=2, padx=10)

    Btn1 = ttk.Button(doPage, text="Start", width=5)
    Btn1.grid(row=1, column=3, padx=10)

    # tk.Label(doPage, text="remaining").grid(row=1, column=5)
    e12 = ttk.Entry(doPage, width=11)
    e12.grid(row=1, column=4, padx=10)

    Btnstp1 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp1.grid(row=1, column=5, padx=10)
    rem1 = Remaining(
        e1, e12, Btn1, Btnstp1, do1, gpio=25
    )  # here add GPIO pin number for toggle

    # DO2 Start
    ttk.Checkbutton(doPage, text="DO 2", variable=cb2).grid(column=0, row=2)
    do2 = ttk.Button(doPage, text="OFF", width=5)
    do2.grid(row=2, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=2, column=2)
    e2 = ttk.Entry(doPage, width=11)
    e2.insert(0, str("00:00:00"))
    e2.grid(row=2, column=2)

    Btn2 = ttk.Button(doPage, text="Start", width=5)
    Btn2.grid(row=2, column=3)

    # tk.Label(doPage, text="remaining").grid(row=2, column=5)
    e22 = ttk.Entry(doPage, width=11)
    e22.grid(row=2, column=4)

    Btnstp2 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp2.grid(row=2, column=5)
    rem2 = Remaining(
        e2, e22, Btn2, Btnstp2, do2, gpio=17
    )  # here add GPIO pin number for toggle

    # DO3 Start
    ttk.Checkbutton(doPage, text="DO 3", variable=cb3).grid(column=0, row=3)
    do3 = ttk.Button(doPage, text="OFF", width=5)
    do3.grid(row=3, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=3, column=2)
    e3 = ttk.Entry(doPage, width=11)
    e3.insert(0, str("00:00:00"))
    e3.grid(row=3, column=2)

    Btn3 = ttk.Button(doPage, text="Start", width=5)
    Btn3.grid(row=3, column=3)

    # tk.Label(doPage, text="remaining").grid(row=3, column=5)
    e32 = ttk.Entry(doPage, width=11)
    e32.grid(row=3, column=4)

    Btnstp3 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp3.grid(row=3, column=5)
    rem3 = Remaining(
        e3, e32, Btn3, Btnstp3, do3, gpio=18
    )  # here add GPIO pin number for toggle

    # DO4 Start
    ttk.Checkbutton(doPage, text="DO 4", variable=cb4).grid(column=0, row=4)
    do4 = ttk.Button(doPage, text="OFF", width=5)
    do4.grid(row=4, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=4, column=2)
    e4 = ttk.Entry(doPage, width=11)
    e4.insert(0, str("00:00:00"))
    e4.grid(row=4, column=2)

    Btn4 = ttk.Button(doPage, text="Start", width=5)
    Btn4.grid(row=4, column=3)

    # tk.Label(doPage, text="remaining").grid(row=4, column=5)
    e42 = ttk.Entry(doPage, width=11)
    e42.grid(row=4, column=4)

    Btnstp4 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp4.grid(row=4, column=5)
    rem4 = Remaining(
        e4, e42, Btn4, Btnstp4, do4, gpio=27
    )  # here add GPIO pin number for toggle

    # DO5 Start
    ttk.Checkbutton(doPage, text="DO 5", variable=cb5).grid(column=0, row=5)
    do5 = ttk.Button(doPage, text="OFF", width=5)
    do5.grid(row=5, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=5, column=2)
    e5 = ttk.Entry(doPage, width=11)
    e5.insert(0, str("00:00:00"))
    e5.grid(row=5, column=2)

    Btn5 = ttk.Button(doPage, text="Start", width=5)
    Btn5.grid(row=5, column=3)

    # tk.Label(doPage, text="remaining").grid(row=5, column=5)
    e52 = ttk.Entry(doPage, width=11)
    e52.grid(row=5, column=4)

    Btnstp5 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp5.grid(row=5, column=5)
    rem5 = Remaining(
        e5, e52, Btn5, Btnstp5, do5, gpio=22
    )  # here add GPIO pin number for toggle

    # DO6 Start
    ttk.Checkbutton(doPage, text="DO 6", variable=cb6).grid(column=0, row=6)
    do6 = ttk.Button(doPage, text="OFF", width=5)
    do6.grid(row=6, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=6, column=2)
    e6 = ttk.Entry(doPage, width=11)
    e6.insert(0, str("00:00:00"))
    e6.grid(row=6, column=2)

    Btn6 = ttk.Button(doPage, text="Start", width=5)
    Btn6.grid(row=6, column=3)

    # tk.Label(doPage, text="remaining").grid(row=6, column=5)
    e62 = ttk.Entry(doPage, width=11)
    e62.grid(row=6, column=4)

    Btnstp6 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp6.grid(row=6, column=5)
    rem6 = Remaining(
        e6, e62, Btn6, Btnstp6, do6, gpio=23
    )  # here add GPIO pin number for toggle

    # DO7 Start
    ttk.Checkbutton(doPage, text="DO 7", variable=cb7).grid(column=0, row=7)
    do7 = ttk.Button(doPage, text="OFF", width=5)
    do7.grid(row=7, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=7, column=2)
    e7 = ttk.Entry(doPage, width=11)
    e7.insert(0, str("00:00:00"))
    e7.grid(row=7, column=2)

    Btn7 = ttk.Button(doPage, text="Start", width=5)
    Btn7.grid(row=7, column=3)

    # tk.Label(doPage, text="remaining").grid(row=7, column=5)
    e72 = ttk.Entry(doPage, width=11)
    e72.grid(row=7, column=4)

    Btnstp7 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp7.grid(row=7, column=5)
    rem7 = Remaining(
        e7, e72, Btn7, Btnstp7, do7, gpio=24
    )  # here add GPIO pin number for toggle

    # DO8 Start
    ttk.Checkbutton(doPage, text="DO 8", variable=cb8).grid(column=0, row=8)
    do8 = ttk.Button(doPage, text="OFF", width=5)
    do8.grid(row=8, column=1)
    # tk.Label(doPage, text="Set Time").grid(row=8, column=2)
    e8 = ttk.Entry(doPage, width=11)
    e8.insert(0, str("00:00:00"))
    e8.grid(row=8, column=2)

    Btn8 = ttk.Button(doPage, text="Start", width=5)
    Btn8.grid(row=8, column=3)

    # tk.Label(doPage, text="remaining").grid(row=8, column=5)
    e82 = ttk.Entry(doPage, width=11)
    e82.grid(row=8, column=4)

    Btnstp8 = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstp8.grid(row=8, column=5)
    rem8 = Remaining(
        e8, e82, Btn8, Btnstp8, do8, gpio=10
    )  # here add GPIO pin number for toggle

    # # global Time
    # tk.Label(doPage, text="Set Time").grid(row=9, column=2)
    # eg1 = tk.Entry(doPage)
    # eg1.insert(0, str('00:00:00'))
    # eg1.grid(row=9, column=3)
    #
    # Btng = tk.Button(doPage, text="Start")
    # Btng.grid(row=9, column=4)
    #
    # tk.Label(doPage, text="remaining").grid(row=9, column=5)
    # eg2 = tk.Entry(doPage)
    # eg2.grid(row=9, column=6)
    #
    # Btnstpg = tk.Button(doPage, text="Stop", state='disable')
    # Btnstpg.grid(row=9, column=7)
    # gbl = CheckBox(eg1, eg2, Btng, Btnstpg)

    # cycle
    ttk.Label(doPage, text="Set Cycle").grid(row=9, column=1)
    eg1c = ttk.Entry(doPage, width=11)
    eg1c.insert(0, str("0"))
    eg1c.grid(row=9, column=2)

    Btngc = ttk.Button(doPage, text="Start", width=5)
    Btngc.grid(row=9, column=3)

    # tk.Label(doPage, text="remaining").grid(row=9, column=5)
    eg2c = ttk.Entry(doPage, width=11)
    eg2c.grid(row=9, column=4)

    Btnstpgc = ttk.Button(doPage, text="Stop", state="disable", width=5)
    Btnstpgc.grid(row=9, column=5)
    gblcy = Cycle(eg1c, eg2c, Btngc, Btnstpgc)

    # DI

    diPage = ttk.Frame(nb)
    nb.add(diPage, text="Digital Input")

    diText1 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText2 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText3 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText4 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText5 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText6 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText7 = ttk.Label(diPage, text="OFF", font=("Courier", 15))
    diText8 = ttk.Label(diPage, text="OFF", font=("Courier", 15))

    # Thermocouple
    thermocouplePage = ttk.Frame(nb)
    nb.add(thermocouplePage, text="Thermocouple")
    # nb.Label(main, text="Citriot Data Acquisition System").grid(row=5)

    thermocoupleText1 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText2 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText3 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText4 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText5 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText6 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText7 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )
    thermocoupleText8 = ttk.Label(
        thermocouplePage, text="Loading...", font=("Courier", 15)
    )

    # Analog Input
    analogPage = ttk.Frame(nb)
    nb.add(analogPage, text="Analog Input")

    ttk.Label(analogPage, text="Min Volt").grid(row=0, column=1)
    ttk.Label(analogPage, text="Min Phy Value").grid(row=0, column=2)
    ttk.Label(analogPage, text="Max Volt").grid(row=0, column=3)
    ttk.Label(analogPage, text="Max Phy Value").grid(row=0, column=4)
    ttk.Label(analogPage, text="Current Volt").grid(row=0, column=5)
    ttk.Label(analogPage, text="Measure Value").grid(row=0, column=6)

    # Creating variable for checkbox
    aicb1 = tk.IntVar()
    aicb2 = tk.IntVar()
    aicb3 = tk.IntVar()
    aicb4 = tk.IntVar()
    aicb5 = tk.IntVar()
    aicb6 = tk.IntVar()
    aicb7 = tk.IntVar()
    aicb8 = tk.IntVar()

    # AI1 Start
    ttk.Checkbutton(analogPage, text="AI 1", variable=aicb1).grid(
        column=0, row=1, padx=10, pady=5
    )

    ai1minvolt = ttk.Entry(analogPage, width=11)
    ai1minvolt.insert(0, str("0"))
    ai1minvolt.grid(row=1, column=1, padx=10)

    ai1minphy = ttk.Entry(analogPage, width=11)
    ai1minphy.insert(0, str("0"))
    ai1minphy.grid(row=1, column=2, padx=10)

    ai1maxvolt = ttk.Entry(analogPage, width=11)
    ai1maxvolt.insert(0, str("10"))
    ai1maxvolt.grid(row=1, column=3, padx=10)

    ai1maxphy = ttk.Entry(analogPage, width=11)
    ai1maxphy.insert(0, str("1000"))
    ai1maxphy.grid(row=1, column=4, padx=10)

    ai1currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai1currentvolt.grid(row=1, column=5, padx=10)

    ai1measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai1measurevalue.grid(row=1, column=6, padx=10)

    # AI2 Start
    ttk.Checkbutton(analogPage, text="AI 2", variable=aicb2).grid(
        column=0, row=2, padx=10, pady=5
    )

    ai2minvolt = ttk.Entry(analogPage, width=11)
    ai2minvolt.insert(0, str("5"))
    ai2minvolt.grid(row=2, column=1, padx=10)

    ai2minphy = ttk.Entry(analogPage, width=11)
    ai2minphy.insert(0, str("100"))
    ai2minphy.grid(row=2, column=2, padx=10)

    ai2maxvolt = ttk.Entry(analogPage, width=11)
    ai2maxvolt.insert(0, str("10"))
    ai2maxvolt.grid(row=2, column=3, padx=10)

    ai2maxphy = ttk.Entry(analogPage, width=11)
    ai2maxphy.insert(0, str("500"))
    ai2maxphy.grid(row=2, column=4, padx=10)

    ai2currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai2currentvolt.grid(row=2, column=5, padx=10)

    ai2measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai2measurevalue.grid(row=2, column=6, padx=10)

    # AI3 Start
    ttk.Checkbutton(analogPage, text="AI 3", variable=aicb3).grid(
        column=0, row=3, padx=10, pady=5
    )

    ai3minvolt = ttk.Entry(analogPage, width=11)
    ai3minvolt.insert(0, str("0"))
    ai3minvolt.grid(row=3, column=1, padx=10)

    ai3minphy = ttk.Entry(analogPage, width=11)
    ai3minphy.insert(0, str("0"))
    ai3minphy.grid(row=3, column=2, padx=10)

    ai3maxvolt = ttk.Entry(analogPage, width=11)
    ai3maxvolt.insert(0, str("10"))
    ai3maxvolt.grid(row=3, column=3, padx=10)

    ai3maxphy = ttk.Entry(analogPage, width=11)
    ai3maxphy.insert(0, str("100"))
    ai3maxphy.grid(row=3, column=4, padx=10)

    ai3currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai3currentvolt.grid(row=3, column=5, padx=10)

    ai3measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai3measurevalue.grid(row=3, column=6, padx=10)

    # AI4 Start
    ttk.Checkbutton(analogPage, text="AI 4", variable=aicb4).grid(
        column=0, row=4, padx=10, pady=5
    )

    ai4minvolt = ttk.Entry(analogPage, width=11)
    ai4minvolt.insert(0, str("0"))
    ai4minvolt.grid(row=4, column=1, padx=10)

    ai4minphy = ttk.Entry(analogPage, width=11)
    ai4minphy.insert(0, str("0"))
    ai4minphy.grid(row=4, column=2, padx=10)

    ai4maxvolt = ttk.Entry(analogPage, width=11)
    ai4maxvolt.insert(0, str("10"))
    ai4maxvolt.grid(row=4, column=3, padx=10)

    ai4maxphy = ttk.Entry(analogPage, width=11)
    ai4maxphy.insert(0, str("100"))
    ai4maxphy.grid(row=4, column=4, padx=10)

    ai4currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai4currentvolt.grid(row=4, column=5, padx=10)

    ai4measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai4measurevalue.grid(row=4, column=6, padx=10)

    # AI5 Start
    ttk.Checkbutton(analogPage, text="AI 5", variable=aicb5).grid(
        column=0, row=5, padx=10, pady=5
    )

    ai5minvolt = ttk.Entry(analogPage, width=11)
    ai5minvolt.insert(0, str("0"))
    ai5minvolt.grid(row=5, column=1, padx=10)

    ai5minphy = ttk.Entry(analogPage, width=11)
    ai5minphy.insert(0, str("0"))
    ai5minphy.grid(row=5, column=2, padx=10)

    ai5maxvolt = ttk.Entry(analogPage, width=11)
    ai5maxvolt.insert(0, str("10"))
    ai5maxvolt.grid(row=5, column=3, padx=10)

    ai5maxphy = ttk.Entry(analogPage, width=11)
    ai5maxphy.insert(0, str("100"))
    ai5maxphy.grid(row=5, column=4, padx=10)

    ai5currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai5currentvolt.grid(row=5, column=5, padx=10)

    ai5measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai5measurevalue.grid(row=5, column=6, padx=10)

    # AI6 Start
    ttk.Checkbutton(analogPage, text="AI 6", variable=aicb6).grid(
        column=0, row=6, padx=10, pady=5
    )

    ai6minvolt = ttk.Entry(analogPage, width=11)
    ai6minvolt.insert(0, str("0"))
    ai6minvolt.grid(row=6, column=1, padx=10)

    ai6minphy = ttk.Entry(analogPage, width=11)
    ai6minphy.insert(0, str("0"))
    ai6minphy.grid(row=6, column=2, padx=10)

    ai6maxvolt = ttk.Entry(analogPage, width=11)
    ai6maxvolt.insert(0, str("10"))
    ai6maxvolt.grid(row=6, column=3, padx=10)

    ai6maxphy = ttk.Entry(analogPage, width=11)
    ai6maxphy.insert(0, str("100"))
    ai6maxphy.grid(row=6, column=4, padx=10)

    ai6currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai6currentvolt.grid(row=6, column=5, padx=10)

    ai6measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai6measurevalue.grid(row=6, column=6, padx=10)

    # AI7 Start
    ttk.Checkbutton(analogPage, text="AI 7", variable=aicb7).grid(
        column=0, row=7, padx=10, pady=5
    )

    ai7minvolt = ttk.Entry(analogPage, width=11)
    ai7minvolt.insert(0, str("0"))
    ai7minvolt.grid(row=7, column=1, padx=10)

    ai7minphy = ttk.Entry(analogPage, width=11)
    ai7minphy.insert(0, str("0"))
    ai7minphy.grid(row=7, column=2, padx=10)

    ai7maxvolt = ttk.Entry(analogPage, width=11)
    ai7maxvolt.insert(0, str("10"))
    ai7maxvolt.grid(row=7, column=3, padx=10)

    ai7maxphy = ttk.Entry(analogPage, width=11)
    ai7maxphy.insert(0, str("100"))
    ai7maxphy.grid(row=7, column=4, padx=10)

    ai7currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai7currentvolt.grid(row=7, column=5, padx=10)

    ai7measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai7measurevalue.grid(row=7, column=6, padx=10)

    # AI8 Start
    ttk.Checkbutton(analogPage, text="AI 8", variable=aicb8).grid(
        column=0, row=8, padx=10, pady=5
    )

    ai8minvolt = ttk.Entry(analogPage, width=11)
    ai8minvolt.insert(0, str("0"))
    ai8minvolt.grid(row=8, column=1, padx=10)

    ai8minphy = ttk.Entry(analogPage, width=11)
    ai8minphy.insert(0, str("0"))
    ai8minphy.grid(row=8, column=2, padx=10)

    ai8maxvolt = ttk.Entry(analogPage, width=11)
    ai8maxvolt.insert(0, str("10"))
    ai8maxvolt.grid(row=8, column=3, padx=10)

    ai8maxphy = ttk.Entry(analogPage, width=11)
    ai8maxphy.insert(0, str("100"))
    ai8maxphy.grid(row=8, column=4, padx=10)

    ai8currentvolt = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai8currentvolt.grid(row=8, column=5, padx=10)

    ai8measurevalue = ttk.Label(analogPage, text="Loading...", font=("Courier", 11))
    ai8measurevalue.grid(row=8, column=6, padx=10)

    # Accelerometer
    # accelerometerPage = ttk.Frame(nb)
    # nb.add(accelerometerPage, text='Accelerometer')
    #
    # accText1x = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))
    # accText2x = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))
    # accText1y = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))
    # accText2y = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))
    # accText1z = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))
    # accText2z = ttk.Label(accelerometerPage, text='Loading...', font=("Courier", 20))

    # Analog Output
    ada = ttk.Frame(nb)
    nb.add(ada, text="Analog Output")

    # Create a DAC instance.
    # dac1 = 1
    # dac2 = 2
    dac1 = Adafruit_MCP4725.MCP4725(address=0x61, busnum=1)     # Address is i2c of that channel
    dac2 = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)     # Address is i2c of that channel

    ttk.Label(ada, text="Min").grid(row=0, column=1)
    ttk.Label(ada, text="Ramp Time").grid(row=0, column=2)
    ttk.Label(ada, text="Hold Time").grid(row=0, column=3)
    ttk.Label(ada, text="Cycle").grid(row=0, column=4)

    ao1minvolt = ttk.Entry(ada, width=11)
    ao1minvolt.insert(0, str("2"))
    ao1minvolt.grid(row=1, column=1, padx=10)

    ao1minramptime = ttk.Entry(ada, width=11)
    ao1minramptime.insert(0, str("00:00:05"))
    ao1minramptime.grid(row=1, column=2, padx=10)

    ao1minholdtime = ttk.Entry(ada, width=11)
    ao1minholdtime.insert(0, str("00:00:07"))
    ao1minholdtime.grid(row=1, column=3, padx=10)

    ao1setcycle = ttk.Entry(ada, width=11)
    ao1setcycle.insert(0, str("5"))
    ao1setcycle.grid(row=1, column=4, padx=10)

    ao1start = ttk.Button(ada, text="Start", width=5)
    ao1start.grid(row=1, column=5, padx=10)

    ttk.Label(ada, text=" AO 1 ").grid(column=0, row=2)

    ttk.Label(ada, text="Max").grid(row=2, column=1)
    ttk.Label(ada, text="Ramp Time").grid(row=2, column=2)
    ttk.Label(ada, text="Hold Time").grid(row=2, column=3)
    ttk.Label(ada, text="Remain Cycle").grid(row=2, column=4)

    ao1maxvolt = ttk.Entry(ada, width=11)
    ao1maxvolt.insert(0, str("4"))
    ao1maxvolt.grid(row=3, column=1, padx=10)

    ao1maxramptime = ttk.Entry(ada, width=11)
    ao1maxramptime.insert(0, str("00:00:08"))
    ao1maxramptime.grid(row=3, column=2, padx=10)

    ao1maxholdtime = ttk.Entry(ada, width=11)
    ao1maxholdtime.insert(0, str("00:00:10"))
    ao1maxholdtime.grid(row=3, column=3, padx=10)

    ao1remaincycle = ttk.Entry(ada, width=11)
    ao1remaincycle.insert(0, str("0"))
    ao1remaincycle.grid(row=3, column=4, padx=10)

    ao1stop = ttk.Button(ada, text="Stop", width=5)
    ao1stop.grid(row=3, column=5, padx=10)

    ao1obj = AOcontrol(
        ao1minvolt,
        ao1minramptime,
        ao1minholdtime,
        ao1setcycle,
        ao1start,
        ao1maxvolt,
        ao1maxramptime,
        ao1maxholdtime,
        ao1remaincycle,
        ao1stop,
        dac1,
    )

    ttk.Label(ada, text="Min").grid(row=5, column=1)
    ttk.Label(ada, text="Ramp Time").grid(row=5, column=2)
    ttk.Label(ada, text="Hold Time").grid(row=5, column=3)
    ttk.Label(ada, text="Cycle").grid(row=5, column=4)

    ao2minvolt = ttk.Entry(ada, width=11)
    ao2minvolt.insert(0, str("1"))
    ao2minvolt.grid(row=6, column=1, padx=10)

    ao2minramptime = ttk.Entry(ada, width=11)
    ao2minramptime.insert(0, str("00:00:05"))
    ao2minramptime.grid(row=6, column=2, padx=10)

    ao2minholdtime = ttk.Entry(ada, width=11)
    ao2minholdtime.insert(0, str("00:00:09"))
    ao2minholdtime.grid(row=6, column=3, padx=10)

    ao2setcycle = ttk.Entry(ada, width=11)
    ao2setcycle.insert(0, str("4"))
    ao2setcycle.grid(row=6, column=4, padx=10)

    ao2start = ttk.Button(ada, text="Start", width=5)
    ao2start.grid(row=6, column=5, padx=10)

    ttk.Label(ada, text=" AO 2 ").grid(column=0, row=7)

    ttk.Label(ada, text="Max").grid(row=7, column=1)
    ttk.Label(ada, text="Ramp Time").grid(row=7, column=2)
    ttk.Label(ada, text="Hold Time").grid(row=7, column=3)
    ttk.Label(ada, text="Remain Cycle").grid(row=7, column=4)

    ao2maxvolt = ttk.Entry(ada, width=11)
    ao2maxvolt.insert(0, str("5"))
    ao2maxvolt.grid(row=8, column=1, padx=10)

    ao2maxramptime = ttk.Entry(ada, width=11)
    ao2maxramptime.insert(0, str("00:00:07"))
    ao2maxramptime.grid(row=8, column=2, padx=10)

    ao2maxholdtime = ttk.Entry(ada, width=11)
    ao2maxholdtime.insert(0, str("00:00:10"))
    ao2maxholdtime.grid(row=8, column=3, padx=10)

    ao2remaincycle = ttk.Entry(ada, width=11)
    ao2remaincycle.insert(0, str("0"))
    ao2remaincycle.grid(row=8, column=4, padx=10)

    ao2stop = ttk.Button(ada, text="Stop", width=5)
    ao2stop.grid(row=8, column=5, padx=10)

    ao2obj = AOcontrol(
        ao2minvolt,
        ao2minramptime,
        ao2minholdtime,
        ao2setcycle,
        ao2start,
        ao2maxvolt,
        ao2maxramptime,
        ao2maxholdtime,
        ao2remaincycle,
        ao2stop,
        dac2,
    )

    # threads
    t2 = threading.Thread(target=update_main)
    t2.daemon = True
    t2.start()

    # Labels
    thermocoupleLabel1 = ttk.Label(
        thermocouplePage, text="Thermocouple 1: ", font=("Courier", 18)
    ).grid(column=1, row=1)
    thermocoupleLabel2 = ttk.Label(
        thermocouplePage, text="Thermocouple 2: ", font=("Courier", 18)
    ).grid(column=1, row=2)
    thermocoupleLabel3 = ttk.Label(
        thermocouplePage, text="Thermocouple 3: ", font=("Courier", 18)
    ).grid(column=1, row=3)
    thermocoupleLabel4 = ttk.Label(
        thermocouplePage, text="Thermocouple 4: ", font=("Courier", 18)
    ).grid(column=1, row=4)
    thermocoupleLabel5 = ttk.Label(
        thermocouplePage, text="Thermocouple 5: ", font=("Courier", 18)
    ).grid(column=1, row=5)
    thermocoupleLabel6 = ttk.Label(
        thermocouplePage, text="Thermocouple 6: ", font=("Courier", 18)
    ).grid(column=1, row=6)
    thermocoupleLabel7 = ttk.Label(
        thermocouplePage, text="Thermocouple 7: ", font=("Courier", 18)
    ).grid(column=1, row=7)
    thermocoupleLabel8 = ttk.Label(
        thermocouplePage, text="Thermocouple 8: ", font=("Courier", 18)
    ).grid(column=1, row=8)

    diLabel1 = ttk.Label(diPage, text="Digital Input 1: ", font=("Courier", 18)).grid(
        column=1, row=1
    )
    diLabel2 = ttk.Label(diPage, text="Digital Input 2: ", font=("Courier", 18)).grid(
        column=1, row=2
    )
    diLabel3 = ttk.Label(diPage, text="Digital Input 3: ", font=("Courier", 18)).grid(
        column=1, row=3
    )
    diLabel4 = ttk.Label(diPage, text="Digital Input 4: ", font=("Courier", 18)).grid(
        column=1, row=4
    )
    diLabel5 = ttk.Label(diPage, text="Digital Input 5: ", font=("Courier", 18)).grid(
        column=1, row=5
    )
    diLabel6 = ttk.Label(diPage, text="Digital Input 6: ", font=("Courier", 18)).grid(
        column=1, row=6
    )
    diLabel7 = ttk.Label(diPage, text="Digital Input 7: ", font=("Courier", 18)).grid(
        column=1, row=7
    )
    diLabel8 = ttk.Label(diPage, text="Digital Input 8: ", font=("Courier", 18)).grid(
        column=1, row=8
    )

    # acc1x = ttk.Label(accelerometerPage, text='Accelerometer1 X Axis').grid(column=1, row=1)
    # acc1y = ttk.Label(accelerometerPage, text='Accelerometer1 Y Axis').grid(column=1, row=2)
    # acc1z = ttk.Label(accelerometerPage, text='Accelerometer1 Z Axis').grid(column=1, row=3)
    # acc2x = ttk.Label(accelerometerPage, text='Accelerometer2 X Axis').grid(column=1, row=4)
    # acc2y = ttk.Label(accelerometerPage, text='Accelerometer2 Y Axis').grid(column=1, row=5)
    # acc2z = ttk.Label(accelerometerPage, text='Accelerometer2 Z Axis').grid(column=1, row=6)

    # progress_bars
    # Labels
    var = 10
    # print("FIlter data in _main_ -------------------------", filter_data)
    l1 = ttk.Label(text="he", textvariable=var)
    # label1.pack()

    progress_1 = ttk.Progressbar(
        thermocouplePage, orient=HORIZONTAL, mode="determinate", length=200, max=255
    )

    button_var = IntVar()

    connectbtn = ttk.Button(text="Connect", command=connect, width=10).place(
        x=10, y=372
    )
    disconnectbtn = ttk.Button(text="Disconnect", command=disconnect, width=10).place(
        x=149, y=372
    )

    # Defines and places the notebook widget

    # mainloop
    width_value = main.winfo_screenwidth()
    height_value = main.winfo_screenheight()
    main.geometry("%dx%d+0+0" % (width_value, height_value))
    # main.geometry('500x500')
    main.mainloop()
