import hdl21 as h
import hdl21.sim as hs

from hdl21.pdk import sample_pdk




@h.module
class inverter():
    VDD = h.Port()
    VSS = h.Port()
    A = h.Port()
    Y = h.Port()

    pmos =sample_pdk.Pmos()(d=Y, g=A, s=VDD, b=VDD)
    nmos =sample_pdk.Nmos()(d=Y, g=A, s=VSS, b=VSS)
    
    # VDD.location(3,0)
    # VSS.location(3,6)
    # A.location(0,3)
    # Y.location(6,3)
    # pmos.location(3,1)
    # nmos.location(3,5)



# @hs.sim
# class inverter_tb_sim:
#     """# Mos Dc Operating Point Simulation Input"""
#     @h.module
#     class inverter_tb():
#         VSS = h.Port()  # The testbench interface: sole port VSS
#         vdc = h.Vdc(dc=1)(n=VSS)  # A DC voltage source

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


def main():
    """# Run the `inverter_tb` simulation."""

    # Set a few runtime options.
    # If you'd like a different simulator, this and the check below are the place to specify it!
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    results = MosDcopSim.run(opts)

    # Get the transistor drain current
    idd = abs(results["op"].data["i(v.xtop.vvdc)"])

    # Check that it's in the expected range
    # (There's nothing magic about these numbers; they're just past sim results.)
    assert idd > 115e-6
    assert idd < 117e-6


if __name__ == "__main__":
    main()