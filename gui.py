#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 6.2
#  in conjunction with Tcl version 8.6
#    Oct 14, 2021 03:47:19 PM CEST  platform: Linux

import sys
import threading
import time

import serial
import serial.tools.list_ports

try:
    import Tkinter as tk
    import Tkinter.scrolledtext as tks
except ImportError:
    import tkinter as tk
    import tkinter.scrolledtext as tks

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1(root)
    root.mainloop()


w = None

MIN_SPEED_HZ = 500
MAX_SPEED_HZ = 1500
BAUDRATE = 9600
TIMEOUT_SEC = 1


def valid_number(P):
    if str.isdigit(P) or P == "":
        return True
    else:
        return False


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])

        top.geometry("600x180+642+319")
        top.minsize(330, 180)
        top.maxsize(1905, 1050)
        top.resizable(0, 0)
        top.title("Motor steering")

        self.serial = serial.Serial()

        self.devices = []

        self.LabelPort = tk.Label(top)
        self.LabelPort.place(relx=0.017, rely=0.056, height=31, width=139)
        self.LabelPort.configure(text='''Select port:''')

        self.ComboboxPorts = ttk.Combobox(top)
        self.ComboboxPorts.place(relx=0.25, rely=0.056, relheight=0.172, relwidth=0.601)
        self.ComboboxPorts.configure(cursor="fleur")
        self.ComboboxPorts['state'] = 'readonly'
        self.scan_ports()

        self.Button21 = tk.Button(top, command=self.connect_to_port)
        self.Button21.place(relx=0.857, rely=0.056, height=33, width=33)
        self.Button21.configure(borderwidth="2")
        self.Button21.configure(text='▶')

        self.Button2 = tk.Button(top, command=self.scan_ports)
        self.Button2.place(relx=0.917, rely=0.056, height=33, width=33)
        self.Button2.configure(borderwidth="2")
        self.Button2.configure(text='↺')

        self.LabelSpeed = tk.Label(top)
        self.LabelSpeed.place(relx=0.017, rely=0.278, height=31, width=139)
        self.LabelSpeed.configure(activebackground="#f9f9f9")
        self.LabelSpeed.configure(text='''Speed: [Hz]''')

        vcmd = (top.register(valid_number))
        self.EntrySpeed = tk.Entry(top, validate='all', validatecommand=(vcmd, '%P'))
        self.EntrySpeed.place(relx=0.25, rely=0.278, height=33, relwidth=0.356)
        self.EntrySpeed.configure(background="white")
        self.EntrySpeed.configure(cursor="fleur")
        self.EntrySpeed.configure(font="TkFixedFont")

        self.ButtonSpeedSet = tk.Button(top, command=self.set_speed)
        self.ButtonSpeedSet.place(relx=0.618, rely=0.278, height=33, width=105)
        self.ButtonSpeedSet.configure(borderwidth="2")
        self.ButtonSpeedSet.configure(cursor="fleur")
        self.ButtonSpeedSet.configure(text='''Set''')

        self.ButtonSpeedStop = tk.Button(top, command=self.stop_motor)
        self.ButtonSpeedStop.place(relx=0.801, rely=0.278, height=31, width=105)
        self.ButtonSpeedStop.configure(activebackground="#f9f9f9")
        self.ButtonSpeedStop.configure(borderwidth="2")
        self.ButtonSpeedStop.configure(text='''STOP''')

        self.LabelDirection = tk.Label(top)
        self.LabelDirection.place(relx=0.017, rely=0.5, height=31, width=139)
        self.LabelDirection.configure(activebackground="#f9f9f9")
        self.LabelDirection.configure(text='''Direction:''')

        self.ComboboxDirection = ttk.Combobox(top)
        self.ComboboxDirection.place(relx=0.25, rely=0.5, relheight=0.172, relwidth=0.545)
        self.ComboboxDirection.set('CLOCKWISE')
        self.ComboboxDirection['values'] = ('CLOCKWISE', 'COUNTERCLOCKWISE')

        self.ButtonDirectionSet = tk.Button(top, command=self.change_direction)
        self.ButtonDirectionSet.place(relx=0.8, rely=0.5, height=33, width=105)
        self.ButtonDirectionSet.configure(activebackground="#f9f9f9")
        self.ButtonDirectionSet.configure(borderwidth="2")
        self.ButtonDirectionSet.configure(text='''Set''')

        self.Label2 = tks.ScrolledText(top)
        self.Label2.place(relx=0.017, rely=0.722, height=41, width=579)
        self.Label2.insert(tk.INSERT, "SELECT SERIAL PORT AND SEND ACTION")
        self.Label2.see(tk.END)

    def connect_to_port(self):
        if self.serial.isOpen():
            self.serial.close()
            self.log("connected")
            self.Button21.configure(text='▶')
        else:
            self.serial = serial.Serial(self.ComboboxPorts.get(), baudrate=BAUDRATE, timeout=TIMEOUT_SEC)
            threading.Thread(target=self.read_serial).start()
            self.log("disconnected")
            self.Button21.configure(text='D')

    def read_serial(self):
        while True:
            time.sleep(0.1)
            if self.serial.isOpen():
                line = self.serial.readline().decode('ascii').strip("\r\n")
                if line != "":
                    self.log(self.serial.name + " rcv: " + line)
            else:
                break

    def scan_ports(self):
        self.devices = [port.device for port in serial.tools.list_ports.comports()]
        if len(self.devices) > 0:
            self.ComboboxPorts.set(self.devices[0])
        self.ComboboxPorts['values'] = self.devices

    def log(self, msg: str):
        self.Label2.insert(tk.INSERT, "\n" + msg)
        self.Label2.see(tk.END)

    def send_message(self, data: str):
        if not self.serial.isOpen():
            self.log("SERIAL PORT UNCONNECTED - CONNECT IT WITH [▶] BUTTON")
            self.Button21.configure(text='▶')
            self.scan_ports()
        else:
            try:
                self.log(self.serial.name + " send: " + str(data))
                self.serial.write(data.encode())
            except serial.serialutil.SerialException:
                self.log("SERIAL PORT UNAVAILABLE CHANGE SERIAL OR CHECK CONNECTION")
                self.scan_ports()

    def set_speed(self):
        speed_entry = self.EntrySpeed.get()
        if speed_entry != "":
            speed = int(speed_entry)
            if MIN_SPEED_HZ <= speed <= MAX_SPEED_HZ:
                self.send_message(f"speed:{self.EntrySpeed.get()}")

    def stop_motor(self):
        self.send_message("stop")

    def change_direction(self):
        direction = self.ComboboxDirection.get()
        if direction == "CLOCKWISE":
            self.send_message("dir:CW")
        else:
            self.send_message("dir:CCW")


if __name__ == '__main__':
    vp_start_gui()
