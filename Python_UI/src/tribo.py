# -*- coding: utf-8 -*-
"""

@author: Jingnan Shi
@contact: jshi@g.hmc.edu


"""
from Tkinter import *
import tkMessageBox
from tkFileDialog import *

import ArduinoControl

class App:

    def __init__(self, master):

        self.dist = 0 # positive corresponds to left
        self.moveAmount = 1
        # initialize arduino port
        self.arduinoPort = ArduinoControl.getArduinoPort()

        self.master = master

        title = Label(master, text = "TriboHMC GUI", font=("Helvetica", 16))
        self.title = title
        
        # rpm and position labels
        Label(master, text="RPM").grid(row=1, sticky=W)
        Label(master, text="Distance from Center").grid(row=2, sticky=W)
        Label(master, text="Revolutions to rotate").grid(row=3, sticky=W)
        # rpm and dist and revs labels
        e_rpm = Entry(master)
        e_dist = Entry(master)
        e_revs = Entry(master)
        self.e_rpm = e_rpm
        self.e_dist = e_dist
        self.e_revs = e_revs
        # rpm and dist and revs go buttons
        rpm_go = Button(master, text="Go",
                        command=self.sendRPM,padx=3,pady=2,width=5)
        dist_go = Button(master, text="Go",
                         command=self.sendPOS,padx=3,pady=2,width=5)
        revs_go = Button(master, text="Go",
                         command=self.sendPOS,padx=3,pady=2,width=5)
         
        # Calibrate button
        cali = Button(master,text="Calibrate zero",command=self.calibrate)
        # stepper move buttons
        stepper_left = Button(master, text="Move to Left",
                              command=self.stepperToLeft)
        stepper_right = Button(master, text="Move to Right",
                               command=self.stepperToRight)
        # positioning the tk widgets
        self.title.grid(row = 0, column=1)
        e_rpm.grid(row=1, column=1)
        rpm_go.grid(row=1, column=2)
        e_dist.grid(row=2, column=1)
        dist_go.grid(row=2,column=2)
        e_revs.grid(row=3,column=1)
        revs_go.grid(row=3,column=2)
        cali.grid(row=3,column=3)
        stepper_left.grid(row=4,column=0)
        stepper_right.grid(row=4,column=1)

         # menu
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit" )
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.showAbout)
        menubar.add_cascade(label="Help", menu=helpmenu)

        master.config(menu=menubar)
        
    def calibrate(self):
        """ calibrate the zero position of the pin
        """
        self.dist = 0

    def sendRPM(self):
        """ send RPM to Aruduino master
        """
        try:
            rpm = int(self.e_rpm.get())
            if rpm > 200 or rpm < 0:
                tkMessageBox.showwarning("Invalid Value","Not in range:0-200")
                return -1
            self.rpm = rpm
            ArduinoControl.setRPM(rpm)
            return 1
        except ValueError:
            tkMessageBox.showwarning("Invalid Value","Not an Integer")
            return -1

    def sendPOS(self):
        """ send stepper motor pos to Aruino
        """
        try:
            dist = int(self.e_dist.get())
            if dist > 5 or dist < -5:
                tkMessageBox.showwarning("Invalid Value","Not in range:-5-5")
                return -1
            change = dist - self.dist
            self.dist = dist
            ArduinoControl.changePos(change) # move by the difference in intended distance and current distance
            return 1
        except ValueError:
            tkMessageBox.showwarning("Invalid Value","Not an Integer")
            return -1

    def sendREVS(self):
        """ send revolution contents
        """
        pass



    def stepperToLeft(self):
        """ stepper to the left
        """
        self.dist += self.moveAmount
        ArduinoControl.changePos(self.moveAmount)
        pass

    def stepperToRight(self):
        """ stepper to the right
        """
        self.dist -= self.moveAmount
        ArduinoControl.changePos(-1 * self.moveAmount)
        pass

    def showAbout(self):
        """ show about info
        """
        tkMessageBox.showinfo("About", """Tribometer Group E4 Section 3 Spring
                              2016, contact Jingnan Shi for questions -
                              jshi@g.hmc.edu""")



