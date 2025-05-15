import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    """
    # Mos DC Operating Point Simulation 

    A simple, common spice-class simulation example using the built-in `sample` PDK.
    """

    import hdl21 as h
    import hdl21.sim as hs
    import vlsirtools.spice as vsp

    # Import the built-in sample PDK
    from hdl21.pdk import sample_pdk


    @hs.sim
    class MosDcopSim:
        """# Mos Dc Operating Point Simulation Input"""

        @h.module
        class Tb:
            """# Basic Mos Testbench"""

            VSS = h.Port()  # The testbench interface: sole port VSS
            vdc = h.Vdc(dc=1)(n=VSS)  # A DC voltage source

            # The transistor under test
            mos = sample_pdk.Nmos()(d=vdc.p, g=vdc.p, s=VSS, b=VSS)

        # Simulation Stimulus
        op = hs.Op()  # DC Operating Point Analysis
        mod = hs.Include(sample_pdk.install.models)  # Include the Models

    return MosDcopSim, h, hs, sample_pdk, vsp


@app.cell
def _(MosDcopSim, vsp):
    """# Run the `MosDcopSim` simulation."""

    # Set a few runtime options.
    # If you'd like a different simulator, this and the check below are the place to specify it!
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        # return

    # Run the simulation!
    results = MosDcopSim.run(opts)

    # Get the transistor drain current
    idd = abs(results["op"].data["i(v.xtop.vvdc)"])
    print(f"idd value is {idd}")
    # Check that it's in the expected range
    # (There's nothing magic about these numbers; they're just past sim results.)
    assert idd > 115e-6
    assert idd < 117e-6
    return


@app.cell
def _(h, hs, sample_pdk):
    @hs.sim
    class MosVGSSweepSim:
        """# Mos Dc Operating Point Simulation Input"""

        @h.module
        class Tb:
            """# Basic Mos Testbench"""
            VSS = h.Port()  # The testbench interface: sole port VSS
            vdc = h.Vdc(dc=1)(n=VSS)  # A DC voltage source

            # The transistor under test
            mos = sample_pdk.Nmos()(d=vdc.p, g=vdc.p, s=VSS, b=VSS)

        # Simulation Stimulus
        op = hs.Op()
        # op = hs.Dc(var="x", sweep=hs.LinearSweep(0, 1, 2), name="swpdc")
        mod = hs.Include(sample_pdk.install.models)  # Include the Models
    return (MosVGSSweepSim,)


@app.cell
def _(MosVGSSweepSim, vsp):
    opts2 = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch2",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    results2 = MosVGSSweepSim.run(opts2)
    idd2 = abs(results2["op"].data["i(v.xtop.vvdc)"])

    print(f"idd value is {idd2}")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
