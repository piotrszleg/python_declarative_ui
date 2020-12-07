import functools
from tkinter_provider import tkinter_provider
from controls import button, slider

def ui(cls, ui_provider=tkinter_provider):   
    @functools.wraps(cls)
    def ui_wrapper(*args, **kwargs):
        fields=cls.__annotations__.copy()
        for name, value in cls.__dict__.items():
            if callable(value) and "is_button" in value.__dict__:
                fields[name]=button
        # create the instance
        obj=cls(*args, **kwargs)
        # create ui provider
        provider=ui_provider(obj, fields)
        # give class a method for closing the ui
        obj.__dict__["close"]=provider.master.destroy
        provider.open()
        return obj
    return ui_wrapper