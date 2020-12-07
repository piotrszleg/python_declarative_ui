# Python UI annotation

Allows for creating user interfaces using class declarations and attributes.

Currently it uses tkinter as user interface implementation.

Created as an experiment with meta-programming in Python an inspired by Unity3D's component inspector generation.

# Running
Pass `example.py` to your Python 3 interpreter.

# Example

```python
import functools
from ui import ui
from controls import button, slider

@ui
class App(object):
    name:str
    size:int
    scale:float
    enabled:bool
    
    probability : slider(float, 0.0, 12.0)

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
        pass # define this function so that linter won't complain

    @button
    def exit(self):
        self.close()

App()
```