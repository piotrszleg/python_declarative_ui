import functools
import tkinter as tk
from dataclasses import dataclass

def button(fun):
    fun.is_button=True
    return fun

@dataclass
class slider(object):
    tp:any
    min:any
    max:any

class tkinter_provider(tk.Frame):
    def __init__(self, obj, fields, master=None):
        if master==None:
            master = tk.Tk()
            super().__init__(master)
        self.toggles={}
        self.entries={}
        self.string_vars={}
        self.sliders={}
        self.obj=obj
        self.create_fields_ui(fields)

    def open(self):
        self.pack()
        self.mainloop()

    def update_toggle(self, toggle, value):
        if value: 
            toggle.config(relief="sunken")
        else:
            toggle.config(relief="raised")

    def toggle_handler(self, button, name):
        value=self.obj.__dict__["_"+name]=not self.obj.__dict__["_"+name]
        self.update_toggle(button, value)

    def button(self, name):
        self.obj.__class__.__dict__[name](self.obj)

    def property_set(self, name, obj, value):
        if name in self.toggles:
            self.update_toggle(self.toggles[name], value)
        if name in self.entries:
            self.string_vars[name].set(value)
        if name in self.sliders:
            self.sliders[name].set(value)
        self.obj.__dict__["_"+name]=value

    def property_get(self, name, obj):
        return obj.__dict__["_"+name]

    def int_entry_handler(self, name, text):
        try:
            if text=="":
                value=0
            else:
                value=int(text)
            self.entry_handler(name, value)
            return True
        except ValueError:
            # if casting to int causes error don't accept input
            return False

    def float_entry_handler(self, name, text):
        try:
            if text=="":
                value=0
            else:
                value=float(text)
            self.entry_handler(name, value)
            return True
        except ValueError:
            return False
    
    def entry_handler(self, name, text):
        self.obj.__dict__["_"+name]=text
        return True

    def slider_handler(self, name, value):
        self.obj.__dict__["_"+name]=value

    def make_line(self, name):
        line=tk.Label(self)
        tk.Label(line, text=name).pack(side="left")
        return line

    def make_entry(self, name, handler, default_value):
        default_value_str=str(default_value)
        # set to default value
        self.obj.__dict__["_"+name]=default_value_str
         # create label
        line=self.make_line(name)
        validation = self.register(functools.partial(handler, name))
        sv=tk.StringVar()
        sv.set(default_value_str)
        self.string_vars[name]=sv
        entry=tk.Entry(line, textvariable=sv, validate="key", validatecommand=(validation, '%P'))
        entry.pack(side="right")
        self.entries[name]=entry
        line.pack(side="top")

    def create_fields_ui(self, fields):
        for name, kind in fields.items():
            if kind==button:
                # add button calling the function
                handler=functools.partial(self.button, name)
                tk.Button(self, text=name, command=handler).pack(side="top")
                continue
            # this is a property
            # add getters and setters
            setattr(self.obj.__class__, name, property(functools.partial(self.property_get, name), functools.partial(self.property_set, name)))
            if kind==bool:
                # set to default value
                self.obj.__dict__["_"+name]=False
                # create label with text
                line=tk.Label(self)
                tk.Label(line, text=name).pack(side="left")
                # create button
                toggle_button=tk.Button(line, text="x")
                handler=functools.partial(self.toggle_handler, toggle_button, name)
                toggle_button.configure(command=handler)
                toggle_button.pack(side="right")
                self.toggles[name]=toggle_button
                line.pack(side="top")
            elif kind==str:
                self.make_entry(name, self.entry_handler, "")
            elif kind==int:
                self.make_entry(name, self.int_entry_handler, 0)
            elif kind==float:
                self.make_entry(name, self.float_entry_handler, 0.0)
            elif isinstance(kind, slider):
                line=self.make_line(name)
                var = tk.DoubleVar()
                handler=functools.partial(self.slider_handler, name)
                scale = tk.Scale(line, variable = var, orient=tk.HORIZONTAL, from_=kind.min, to=kind.max, command=handler)
                if kind.tp==float:
                    # by default resolution is 1
                    scale.configure(resolution=0.01)
                self.sliders[name]=scale
                scale.pack(side="right")
                line.pack(side="top")
            else:
                raise ValueError("Unknown field type")

def ui(cls):   
    @functools.wraps(cls)
    def ui_wrapper(*args, **kwargs):
        fields=cls.__annotations__.copy()
        for name, value in cls.__dict__.items():
            if callable(value) and "is_button" in value.__dict__:
                fields[name]=button
        obj=cls(*args, **kwargs)
        provider=tkinter_provider(obj, fields)
        obj.__dict__["close"]=provider.master.destroy
        provider.open()
        return obj
    return ui_wrapper

@ui
class App(object):
    name:str
    size:int
    scale:float
    enabled:bool
    
    probability:slider(float, 0.0, 12.0)

    @button
    def print_dict(self):
        print(self.__dict__)

    @button
    def disable(self):
       self.enabled=False

    @button
    def clear_name(self):
       self.name=""

    def close(self):
        pass # for linter

    @button
    def exit(self):
        self.close()

App()