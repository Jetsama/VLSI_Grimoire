from typing import Dict, Optional
import hdl21 as h
from hdl21.module import ModuleAttr


h.Module. __init_subclass__ = lambda: None
def location_function(self, x: float, y: float):
    self.x = x
    self.y = y
    # return self
class Schematic(h.Module):
    def __init__(self, name: Optional[str] = None):

        self.locations: Dict[str, ModuleAttr] = dict()
        super().__init__(name=name)
    
    def add(self, val: ModuleAttr, name: Optional[str] = None) -> ModuleAttr:
        
        returnval= super().add(val, name=name)
    
        if isinstance(val, h.Signal):
            #check if val is a port
            val.location = location_function
        if isinstance(val, h.Instance):
            val._specialcases.append("x")
            val._specialcases.append("y")
            val._specialcases.append("rotation")
    pass
    @property
    def max_width(self):
        pass
    @property
    def max_height(self):
        pass
        # for 
def layouter_example(module:h.Module) -> Schematic:
    sch = Schematic(name=f"{module.name}_sch")
    for port in module.ports.values():
        sch.add(port)
        port.location(0,0)  # Dummy location
    return sch

import svg
def print_schematic(schematic:Schematic):
    scale = 100

    elements = []
    max_height = 7
    max_width = 7
    #draw ports
    for port in schematic.ports.values():
        width = 1
        height = 1
        
        x_location = port.x #+ width/2
        y_location = port.y #+ height/2
        port_shape = svg.Rect(
            x=x_location*scale, y=y_location*scale,
            width=width*scale, height=height*scale,
            stroke="black",
            # fill="transparent",
            stroke_width=0.1*scale,
        )
        elements.append(port_shape)
    for instance in schematic.instances.values():
        #get symbol
        width = 1
        height = 1
        x_location = instance.x #+ width/2
        y_location = instance.y #+ height/2
        port_shape = svg.Rect(
            x=x_location*scale, y=y_location*scale,
            width=width*scale, height=height*scale,
            stroke="grey",
            fill="grey",
            stroke_width=0.1*scale,
        )
        elements.append(port_shape)
        pass

    #draw grid
    for row in range(int(max_height+1)):
        line = svg.Line(
            x1=0,
            y1=row*scale,
            x2=max_width*scale,
            y2=row*scale,
            stroke="lightgray",
            stroke_width=0.05*scale,
        )
        elements.append(line)
    for col in range(int(max_width+1)):
        line = svg.Line(
            x1=col*scale,
            y1=0,
            x2=col*scale,
            y2=max_height*scale,
            stroke="lightgray",
            stroke_width=0.05*scale,
        )
        elements.append(line)
        
    with open("test_schematic.svg", "w") as f:
        f.write(str(svg.SVG(
            width=max_width*scale,
            height=max_height*scale,
            elements= elements
            ))
        )


class Symbol:
    def __init__(self,width,height):
        self.pin_locations = {}
        self.width = width
        self.height = height
        self.shapes = []
        pass
    pass
# class SymbolInstance:
#     def __init__(self):
#         pass
#     pass


if __name__ == "__main__":
    sch = Schematic(name="my_sch")
    port = h.Port(name="VDD")
    sch.add(port)
    port.x = 0
    port.y = 2
    # print_schematic(sch)
    # print(sch)


    inverter = Schematic(name="inverter")
    from hdl21.pdk import sample_pdk
    sample_pdk.Pmos.symbol = Symbol(width=1,height=3)

    sample_pdk.Nmos.symbol = Symbol(width=1,height=3)

    VDD = h.Port()
    inverter.add(VDD,"VDD")
    VDD.x = 3
    VDD.y = 0

    VSS = h.Port()
    inverter.add(VSS,"VSS")
    VSS.x = 3
    VSS.y = 6

    A = h.Port()
    inverter.add(A,"A")
    A.x = 0
    A.y = 3

    Y = h.Port()
    inverter.add(Y,"Y") 
    Y.x = 6
    Y.y = 3

    pmos =sample_pdk.Pmos()(d=Y, g=A, s=VDD, b=VDD)
    inverter.add(pmos,"pmos")
    pmos.x = 3
    pmos.y = 2

    nmos =sample_pdk.Nmos()(d=Y, g=A, s=VSS, b=VSS)
    inverter.add(nmos,"nmos")
    nmos.x = 3
    nmos.y = 4
    print_schematic(inverter)



