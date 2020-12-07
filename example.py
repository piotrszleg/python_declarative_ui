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