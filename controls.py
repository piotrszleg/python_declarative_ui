from dataclasses import dataclass

def button(fun):
    fun.is_button=True
    return fun

@dataclass
class slider(object):
    tp:any
    min:any
    max:any