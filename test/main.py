from tkinter import *
from tkinter.ttk import *
class window(Tk):
    def __init__(self,*args,**kwargs):
        Tk.__init__(self,*args,**kwargs)
        self.geometry("500x500")
        self._newExpenseRender()
        self.expenses = list()
        self.expenseTabParent = Notebook(self)
    def addExpense(self):
        n = {
            "name": self.newExpenseEntities['entry_name'].get(),
            "ammount": self.newExpenseEntities['entry_ammount'].get(),
            "repeat": self.newExpenseEntities['entry_repeat'].get()
        }

        self.expenses.append(n)
        self._showExpenseRender()
    def _newExpenseRender(self):
        self.newExpense = LabelFrame(self, text="new expense")
        labelParent= Frame(self.newExpense)
        entryParent= Frame(self.newExpense)
        self.newExpenseEntities = {
            "name": Label(labelParent, text="name:"),
            "ammount": Label(labelParent, text="ammount:"),
            "repeat": Label(labelParent, text="repeat:"),
            "entry_name": Entry(entryParent),
            "entry_ammount": Entry(entryParent),
            "entry_repeat": Entry(entryParent),
            "submit": Button(self.newExpense, command=self.addExpense, text='submit')
        }
        labelParent.grid(row=0, column=0)
        entryParent.grid(row=0, column=1)
        for key in self.newExpenseEntities.keys():
            if key != "submit":
                self.newExpenseEntities[key].pack(padx=2)
            else:
                self.newExpenseEntities[key].grid(column=1, row=1)
        self.newExpense.place(relx=0.01, rely= 0.01, anchor=NW)
    def _showExpenseRender(self):
        self.showExpense = LabelFrame(self, text="all expenses")
        if len(self.expenses) == 0:
            label = Label(self.showExpense, text="no expenses are available")
            return
        nameParent = Frame(self.showExpense)
        ammountParent = Frame(self.showExpense)
        repeatParent = Frame(self.showExpense)
        self.showExpenseEntities = {
            "name": [],
            "ammount": [],
            "repeat": []
        }
        nameParent.grid(column=0, row=0)
        ammountParent.grid(column=1, row=0)
        repeatParent.grid(column=2, row=0)
        for i in range(len(self.expenses)):
            currentExpense = self.expenses[i]
            keys = list(currentExpense.keys())
            
            if i == 0:
                for j in range(3):
                    if j == 0:
                        label = Label(nameParent, text="name")
                    if j == 1:
                        label = Label(ammountParent, text="ammount")
                    if j == 2:
                        label = Label(repeatParent, text="repeat")
                    label.grid(row=i, column=j, padx=2, pady=2)

            for j in range(3):
                if j == 0:
                    label = Button(nameParent, text=currentExpense[keys[j]], command=lambda: self.renderNewExpenseTab(i))
                if j == 1:
                    label = Label(ammountParent, text=currentExpense[keys[j]])
                if j == 2:
                    label = Label(repeatParent, text=currentExpense[keys[j]])
                self.showExpenseEntities[keys[j]].append(label)
                label.grid(row=i+1, column=j, padx=2, pady=2)

        self.showExpense.place(relx=0.9, rely=0.1, anchor=NE)
    def renderNewExpenseTab(self, index):
        tab = Frame(self.expenseTabParent)
        
                
                


        
achraf = window()
achraf.mainloop()

