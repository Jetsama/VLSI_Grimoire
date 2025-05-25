import re
import hdl21
from hdl21 import Module

def parse_schematic(file_path):
    with open(file_path, 'r') as file:

        metadata = {}
        nodes = []
        components = []
        text = file.read().replace("\n", "")
        x = text.split("}")
        for i in range(len(x)):
            x[i] = x[i]+"}"
        for line in x:
            # Parse metadata
            if line.startswith("v {"):
                metadata_match = re.search(r"xschem version=(\S+) file_version=(\S+)", line)
                if metadata_match:
                    metadata['xschem_version'] = metadata_match.group(1)
                    metadata['file_version'] = metadata_match.group(2)

            # Parse nodes
            elif line.startswith("N"):
                node_match = re.search(r"N (-?\d+) (-?\d+) (-?\d+) (-?\d+) {lab=(\S+)}", line)
                if node_match:
                    nodes.append({
                        'x1': int(node_match.group(1)),
                        'y1': int(node_match.group(2)),
                        'x2': int(node_match.group(3)),
                        'y2': int(node_match.group(4)),
                        'label': node_match.group(5)
                    })

            # Parse components
            elif line.startswith("C"):
                component_match = re.search(r"C {(.+?)}", line)
                if component_match:
                    definition_line = next(x)
                    definition_match = re.search(r" (-?\d+) (-?\d+) (-?\d+) (-?\d+)", definition_line)
                    components.append({
                        'symbol': component_match.group(1),
                        'x': int(component_match.group(2)),
                        'y': int(component_match.group(3)),
                        'rotation': int(component_match.group(4)),
                        'mirror': int(component_match.group(5)),
                        'name': component_match.group(6)
                    })

    return {
        'metadata': metadata,
        'nodes': nodes,
        'components': components
    }

parse_schematic("inverter/inverter.sch")

# def load_xschem_design(file_path):
#     """
#     Load an Xschem design file and convert it to HDL21 format.
    
#     :param file_path: Path to the Xschem design file
#     :return: HDL21 design object
#     """
#     # This is a placeholder for the actual loading logic
#     # In practice, you would parse the Xschem file and extract modules, ports, and connections
#     # xschem_design = parse_xschem_file(file_path)
    
#     hdl_design = XschemDesign(file_path)
    
#     for module in xschem_design.modules:
#         hdl_module = Module(module.name)
#         for port in module.ports:
#             hdl_port = Port(port.name, port.direction, port.type)
#             hdl_module.add_port(hdl_port)
#         hdl_design.add_module(hdl_module)
    
#     for connection in xschem_design.connections:
#         hdl_connection = Connection(connection.source, connection.destination)
#         hdl_design.add_connection(hdl_connection)
    
#     return hdl_design

# class XschemDesign(Module):
#     def __init__(self, file_path):
#         file = open(file_path, 'r')
#         self.name = name
#         self.modules = []
#         self.connections = []

#     def add_module(self, module):
#         self.modules.append(module)

#     def add_connection(self, connection):
#         self.connections.append(connection)

#     def to_hdl21(self):
#         # Convert the design to HDL21 format
#         hdl_design = hdl21.Design(self.name)
#         for module in self.modules:
#             hdl_design.add_module(module.to_hdl21())
#         for connection in self.connections:
#             hdl_design.add_connection(connection.to_hdl21())
#         return hdl_design