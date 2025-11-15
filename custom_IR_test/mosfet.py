
import schemdraw
from schemdraw import *

import schemdraw.elements as elm


schemdraw.use('svg')
schemdraw.svgconfig.text = 'text'
schemdraw.svgconfig.svg2 = False

import hdl21 as h

m = h.Module(name="MyModule")

from copy import deepcopy

@h.paramclass
class MosParams:
    m = h.Param(dtype=int, desc="Transistor Multiplier")

nmos = h.ExternalModule(
    name="nmos",
    desc="Nmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=MosParams,
)
pmos = h.ExternalModule(
    name="pmos",
    desc="Pmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=MosParams,
)
@h.module
class CapCell:
    """# Compensation Capacitor Cell"""
    symbol = elm.Capacitor
    p, n, VDD, VSS = 4 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class ResCell:
    """# Compensation Resistor Cell"""
    symbol = elm.Resistor
    p, n, sub = 3 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class Compensation:
    """# Single Ended RC Compensation Network"""

    a, b, VDD, VSS = 4 * h.Port()
    r = ResCell(p=a, sub=VDD)
    # r.layout = right()
    c = CapCell(p=r.n, n=b, VDD=VDD, VSS=VSS)

@h.module
class DiffOta:
# IO Interface
    VDD, VSS = 2 * h.Input()
    inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
    out = h.Diff(desc="Differential Output", port=True, role=h.Diff.Roles.SOURCE)
    vg, ibias = 2 * h.Input()

    # Internal Signals
    out1 = h.Diff(desc="First Stage Output")
    pbias = h.Signal(desc="Pmos Gate Bias")

    # Input Stage & CMFB Bias
    xbias_input = nmos(m=1)(g=vg, s=VSS, b=VSS)
    xinput_pair = h.Pair(nmos(m=10))(d=out1, g=inp, s=xbias_input.d, b=VSS)
    xinput_load = h.Pair(pmos(m=3))(d=out1, g=pbias, s=VDD, b=VDD)

    # Output Stage
    xpout = h.Pair(pmos(m=16))(d=out, g=out1, s=VDD, b=VDD)
    xnout = h.Pair(nmos(m=4))(d=out, g=ibias, s=VSS, b=VSS)

    # Biasing
    xndiode = nmos(m=1)(d=ibias, g=ibias, s=VSS, b=VSS)
    xnsrc = nmos(m=1)(d=pbias, g=ibias, s=VSS, b=VSS)
    xpdiode = pmos(m=6)(d=pbias, g=pbias, s=VDD, b=VDD)

    # Compensation Network
    xcomp = h.Pair(Compensation)(a=out, b=out1, VDD=VDD, VSS=VSS)

import sys
def main():
    h.netlist(DiffOta, sys.stdout)
    h.netlist(Compensation, sys.stdout)
    draw(Compensation)

drawing_dict = {
    "CapCell":elm.Capacitor,
    "ResCell":elm.Resistor
}

def draw(circuit):
    insts = {}
    nets = {}
    with schemdraw.Drawing(file="test_hd21.svg",show=False,transparent=False) as d:
        for name, inst in circuit.instances.items():
            # class_type = inst.of.name
            insts.update({name : drawing_dict[inst.of.name]()})
            for term_name, conn in inst.conns.items():
                nets.update({conn.name:getattr(insts[name],term_name)})
                pass
                # nets.update({name)
        for name, port in circuit.ports.items():
            print(port)
            elm.Tag().label(name).left()#.at("a")
        
        pass


if __name__ == "__main__":
    main()

# with schemdraw.Drawing(file="example.svg",show=False):
#     elm.Resistor().right().label('1Ω')
#     elm.Capacitor().down().label('10μF')
#     elm.Line().left()
#     elm.SourceSin().up().label('10V')
#     # elm.Resistor().label(r'$CLICk-ME$', href="#jump", color="blue")
#     # elm.Resistor().down().label(r'$RESET$', decoration="overline")


# with schemdraw.Drawing(file="5T.svg",show=False) as d:
#     # tail transistor
#     Q1 = elm.AnalogNFet().anchor('source').theta(0).reverse()
#     elm.Line().down().length(0.5)
#     ground = d.here
#     elm.Ground()

#     # input pair
#     elm.Line().left().length(1).at(Q1.drain)
#     Q2 = elm.AnalogNFet().anchor('source').theta(0).reverse()

#     elm.Dot().at(Q1.drain)
#     elm.Line().right().length(1)
#     Q3 = elm.AnalogNFet().anchor('source').theta(0)

#     # current mirror
#     Q4 = elm.AnalogPFet().anchor('drain').at(Q2.drain).theta(0)
#     Q5 = elm.AnalogPFet().anchor('drain').at(Q3.drain).theta(0).reverse()

#     elm.Line().right().at(Q4.gate).to(Q5.gate)

#     elm.Dot().at(0.5*(Q4.gate + Q5.gate))
#     elm.Line().down().toy(Q4.drain)
#     elm.Line().left().tox(Q4.drain)
#     elm.Dot()

#     # vcc connection
#     elm.Line().right().at(Q4.source).to(Q5.source)
#     elm.Dot().at(0.5*(Q4.source + Q5.source))
#     elm.Vdd()

#     # bias source
#     elm.Line().left().length(0.25).at(Q1.gate)
#     elm.SourceV().down().toy(ground).reverse().scale(0.5).label("Bias")
#     elm.Ground()

#     # signal labels
#     elm.Tag().at(Q2.gate).label("In+").left()
#     elm.Tag().at(Q3.gate).label("In−").right()
#     elm.Dot().at(Q3.drain)
#     elm.Line().right().tox(Q3.gate)
#     elm.Tag().right().label("Out").reverse()

#     # bias currents
#     elm.CurrentLabel(length=1.25, ofst=0.25).at(Q1).label("20µA")
#     elm.CurrentLabel(length=1.25, ofst=0.25).at(Q4).label("10µA")
#     elm.CurrentLabel(length=1.25, ofst=0.25).at(Q5).label("10µA")
# import hdl21 as h
# import hdl21.sim as hs
# import vlsirtools.spice as vsp

# # Import the built-in sample PDK
# from hdl21.pdk import sample_pdk

# @hs.sim
# class MosDcopSim:
#     """# Mos Dc Operating Point Simulation Input"""

#     @h.module
#     class Tb:
#         """# Basic Mos Testbench"""

#         VSS = h.Port()  # The testbench interface: sole port VSS
#         vdc = h.Vdc(dc=1)(n=VSS)  # A DC voltage source

#         # The transistor under test
#         mos = sample_pdk.Nmos()(d=vdc.p, g=vdc.p, s=VSS, b=VSS)

#     # Simulation Stimulus
#     op = hs.Op()  # DC Operating Point Analysis
#     mod = hs.Include(sample_pdk.install.models)  # Include the Models

# def main():
#     """# Run the `MosDcopSim` simulation."""

#     # Set a few runtime options.
#     # If you'd like a different simulator, this and the check below are the place to specify it!
#     opts = vsp.SimOptions(
#         simulator=WebAssembly_NGspice,
#         fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
#         rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
#     )
#     results = MosDcopSim.run(opts)


# # spice -> drawing
# # spice -> python
# # drawing -> spice

# # python -> spice
# # spice -> python

# # with schemdraw.Drawing():
# #     elm.Resistor().right().label('1Ω')
# #     elm.Capacitor().down().label('10μF')
# #     elm.Line().left()
# #     elm.SourceSin().up().label('10V')
# # class intermediate_representation_circuit:
# #     def __init__(self):
# #         self.name = "ethan"
# #         # print("hello {self.name}!")

# #         pass
# #     def draw(self):

# #         pass

# # #symbol
# # #schematic
# # #spice
# # #verilog
# # #lookup table?


# # test = intermediate_representation_circuit()
# # print(test.name)