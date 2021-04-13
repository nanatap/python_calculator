"""Header documentation:

This application is providing simple and scientific calculators.
GUI - Tkinter version: 8.5
Python version: 3.8.5
Application has the file menu and the help menu.
In file menu you will find navigation between simple calculator, scientific calculator and termination of the program.
In help menu is the brief info about this program and log file with all the calculations included. If you have not done
any operations and go ahead to view log file, it will give you an error message.
At the top of the program I have imported necessary libraries, defined and tkinter and called the calculator class.
There are two classes one for calculator and its own functions and another for log file frame.
You can find more detailed information on each function.

"""

import random
import tkinter
from tkinter import *
import operator
import tkinter.messagebox
import math
import time


def main():
    root = Tk()
    Calculator(root)
    root.mainloop()

class Calculator(Frame):
    """This class is for simple and scientific calculators and its own nav bar."""

    entry = None

    def __init__(self, master):
        super().__init__()
        self.file_name = None
        self.master = master
        self.master.geometry("350x300")
        self.config(bg="black")
        self.master.config(bg="black")

        self.init_menu()
        self.init_simple_calc()

    def clear_frame(self):
        """This function clears the frame"""

        for widget in self.winfo_children():
            widget.destroy()
        self.pack_forget()

    def switch_to_scientific(self):
        self.clear_frame()
        self.init_scientific_calc()

    def switch_to_simple(self):
        self.clear_frame()
        self.init_simple_calc()

    def write_log_file(self, log):
        """
        Write message to log file
        :param log: message to log
        :return: None
        """
        if not self.file_name:
            self.file_name = str(int(time.time()))

        with open(self.file_name + ".txt", "a") as my_file:
            my_file.write(log + "\n")

    def view_logs(self):
        """This function is responsible for opening log file, if there is no
        operations done in calculator, it will create an error message box for the user
        or else it will open the log file, read each line and present it in the view log
        text area with the title of timestamp.
        """

        if not self.file_name:
            tkinter.messagebox.showerror("Error", "No log file generated!")
            return

        t = tkinter.Toplevel(self)
        t.title(self.file_name)
        text = tkinter.Text(t, height=30, width=50)
        read_file = open(self.file_name + ".txt", 'r')
        lines = read_file.readlines()
        for i in lines:
            text.insert(tkinter.END, i)
        text.pack()

    @staticmethod
    def on_click():

        tkinter.messagebox.showinfo("About calculator",
                                    "This calculator is built with a help of Python3 and Tkinter GUI. " 
                                    "\nSimple description: \n1) Simple calculator with four different operations,\n "
                                    "2) Scientific calculator with: Sin, Cos, tan, rand,\n"
                                    "3) Navigation system in file menu and help menu,\n "
                                    "4) Log files for calculation history.\n "
                                    "Versions: \n \n Application: 1.0.0 "
                                    "\n Dependencies:\n Python: 3.8.5 \n Tkinter: 8.5" 
                                    "\n \n Nanata Peradze")

    @staticmethod
    def client_exit():
        exit()

    def input(self, x):
        """ Function below is fired for all the numbers on press, it inserts the pressed digits to the screen."""

        self.entry.insert(len(self.entry.get()), str(x))

    def clear(self):
        self.entry.delete(0, len(self.entry.get()))

    def equals_op(self):
        """This function is called when equals sign is pressed, it gets the user input
        checks and executes operation.
        below we keep the current value on the screen in variable "numbers
        In ops dictionary we have all the operation functions
        for instance: If plus is chosen, ops dictionary is calling add function to do the operation.

        For loop is looping over operations array to get the correct operation in the given string, after operation
        is matched, string is split as the left and right side of the math operation, left side(first number) is
        kept in num1 and right side (second number) in num2. After defining math operator and splitting the string,
        ops is calling correct function to do the operation and the result is kept in variable 'result'
        """

        numbers = self.entry.get()

        if '--' in numbers:
            numbers = numbers.replace('--', "+")

        operations = ["+", "/", "*", "-"]

        ops = {
           "+": operator.add,
           "-": operator.sub,
           "*": operator.mul,
           "/": operator.truediv,
        }

        for i in operations:
            if i in numbers:
                numbersSplit = numbers.split(i)
                num1 = float(numbersSplit[0])
                num2 = float(numbersSplit[1])
                f = ops[i]
                result = f(num1, num2)
                self.clear()
                self.input(result)
                self.write_log_file(str(num1) + str(i) + str(num2) + "=" + str(result))

        sci_operations = ["sin", "cos", "tan", "rand"]

        ops = {
           "sin": math.sin,
           "cos": math.cos,
           "tan": math.tan,
        }

        for i in sci_operations:
            if i in numbers:
                value = numbers.replace(i, "")
                f = ops[i]
                result = f(float(value))
                self.clear()
                self.input(result)
                self.write_log_file(str(i) + str(value) + "=" + str(result))

    def generate_random(self):
        randomNum = random.randint(0, 100)
        self.clear()
        self.input(str(randomNum))
        self.write_log_file("rand=" + str(randomNum))

    def init_menu(self):
        """ Create file menu and help menu """

        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Simple Calculator", command=self.switch_to_simple)
        file.add_command(label="Scientific Calculator", command=self.switch_to_scientific)
        file.add_command(label="Terminate Application", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)

        HelpMenu = Menu(menu)
        HelpMenu.add_command(label="View Logs", command=self.view_logs)
        HelpMenu.add_command(label="About", command=self.on_click)
        menu.add_cascade(label="Help menu", menu=HelpMenu)

    def init_simple_calc(self):
        """ Creating grid, rows and columns for each button. """

        self.master.title("Calculator")

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        self.entry = Entry(self, width=30)
        self.entry.grid(row=0, columnspan=4)
        close = Button(self, text="Close", command=self.quit,padx=30, highlightbackground="black")
        close.grid(row=1, column=1)
        clear = Button(self, text='Clear', command=self.clear, padx=30, highlightbackground="black")
        clear.grid(row=1, column=2)

        row = ["7", "8", "9"]
        for i, elem in enumerate(row):
            first_row = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                               highlightbackground="black")
            first_row.grid(row=2, column=i)

        div = Button(self, text="/", command=lambda m="/": self.input(m), padx=20, highlightbackground="black")
        div.grid(row=2, column=3)

        row = ["4", "5", "6"]
        for i, elem in enumerate(row):
            secondRow = Button(self, text=elem, command=lambda m=elem: self.input(m),padx=20,
                               highlightbackground="black")
            secondRow.grid(row=3, column=i)

        mult = Button(self, text="*", command=lambda m="*": self.input(m), padx=20, highlightbackground="black")
        mult.grid(row=3, column=3)

        row = ["1", "2", "3"]
        for i, elem in enumerate(row):
            thirdRow = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                              highlightbackground="black")
            thirdRow.grid(row=4, column=i)

        minus = Button(self, text="-", command=lambda m="-": self.input(m), padx=20, highlightbackground="black")
        minus.grid(row=4, column=3)

        row = ["0", "."]
        for i, elem in enumerate(row):
            fourthRow = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                               highlightbackground="black")
            fourthRow.grid(row=5, column=i)

        plus = Button(self, text="+", command=lambda m="+": self.input(m), padx=20, highlightbackground="black")
        plus.grid(row=5, column=2)

        equ = Button(self, text="=", command=self.equals_op, padx=20, highlightbackground="black")
        equ.grid(row=5, column=3)

        self.pack()

    def init_scientific_calc(self):
        """ Creating grid, - (visual part) rows and columns for each button. """

        self.master.title("Scientific calculator")

        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)

        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)

        self.entry = Entry(self, width=35)
        self.entry.grid(row=0, columnspan=4)
        close = Button(self, text="Close", command=self.quit, padx=30, highlightbackground="black")
        close.grid(row=1, column=2)
        clear = Button(self, text='Clear', command=self.clear, padx=30, highlightbackground="black")
        clear.grid(row=1, column=1)

        row = ["7", "8", "9"]
        for i, elem in enumerate(row):
            first_row = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                               highlightbackground="black")
            first_row.grid(row=2, column=i)

        div = Button(self, text="sin", command=lambda m="sin": self.input(m), padx=20, highlightbackground="black")
        div.grid(row=2, column=3)

        row = ["4", "5", "6"]
        for i, elem in enumerate(row):
            secondRow = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                               highlightbackground="black")
            secondRow.grid(row=3, column=i)

        mult = Button(self, text="cos", command=lambda m="cos": self.input(m), padx=20, highlightbackground="black")
        mult.grid(row=3, column=3)

        row = ["1", "2", "3"]
        for i, elem in enumerate(row):
            thirdRow = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                              highlightbackground="black")
            thirdRow.grid(row=4, column=i)

        minus = Button(self, text="tan", command=lambda m="tan": self.input(m), padx=20, highlightbackground="black")
        minus.grid(row=4, column=3)

        row = ["0", "."]
        for i, elem in enumerate(row):
            fourthRow = Button(self, text=elem, command=lambda m=elem: self.input(m), padx=20,
                               highlightbackground="black")
            fourthRow.grid(row=5, column=i)

        plus = Button(self, text="rand", command=self.generate_random, padx=20, highlightbackground="black")
        plus.grid(row=5, column=2)

        equ = Button(self, text="=", command=self.equals_op, padx=20, highlightbackground="black")
        equ.grid(row=5, column=3)

        self.pack()


class Log(Frame):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        t = tkinter.Text(self, height=30, width=30)
        t.pack()
        tkinter.mainloop()


if __name__ == '__main__':
    main()
