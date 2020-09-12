

import tkinter as tk


class GetWidgetAttributes:
    @staticmethod
    def get_attributes(widget):
        widg = widget
        keys = widg.keys()
        for key in keys:
            print("Attribute: {:<20}".format(key), end=' ')
            value = widg[key]
            vtype = type(value)
            print('Type: {:<30} Value: {}'.format(str(vtype), value))


if __name__ == '__main__':
    gw = GetWidgetAttributes()
    # For Example, find all attribute
    gw.get_attributes(tk.Button())