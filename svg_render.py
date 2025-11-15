import copy
import svg


class svg_schematic:
    def __init__(self,schematic):
        file_path = file_path
        file_name = "test.svg"
    @property
    def svg(self):
        return svg.SVG(
                width=self.width,
                height=self.height,
                elements= self.elements
        )
    
class renderer_svg:
    def __init__(self,file_path):
        file_path = file_path
        file_name = "test.svg"
    def place_port(self,schematic,port):

        port_shape = svg.Rect(
            x=port.x, y=port.y,
            width=1, height=1,
            stroke="black",
            fill="transparent",
            stroke_width=0.1,
        )
        pass

    def place_instance(self,schematic,inst):
        pass

    def render_schematic(self,schematic):
        elements = []
        elements.append(new_shape)
        # first place ports
        for port in schematic.ports.values():
            self.place_port(schematic)
        # second place all instatnces
        for inst in schematic.insts.values():
            self.place_instance(schematic)
        # then route nets
        for net in schematic.nets.values():
            pass

    def render_schematic(self,schematic:schematic):
        elements = []
        scale = 1
        min_x= 1000
        min_y = 1000
        max_x = 1
        max_y= 1
        return svg.SVG(
                width=width,
                height=height,
                elements= elements
        )