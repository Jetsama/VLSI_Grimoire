import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"## Inverter Demo")
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    import subprocess
    def xschem_draw(path,file):
        subprocess.run(f"xschem --png --plotfile {path}/{file}.png {path}/{file}.sch --quit", shell=True, check=True)
        _src = (
        f"{path}/{file}.png"
        )
        return mo.image(src=_src)
    xschem_draw("inverter","inverter")

    return (subprocess,)


@app.cell
def _(mo):
    mo.md(
        r"""
        Using Xschem we can create a simple inverter example. First steps are creating a 2 fet circuit. 
        We start by placing the sky130 fets from the "/foss/pdks" folder.
        Then the IO from the default library.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"We can now netlist using xschem!")
    return


@app.cell
def _(subprocess):
    def xschem_netlist(path,file):
        command = f"xschem --netlist --spice {path}/{file}.sch --netlist_path {path} -N {file}.spice --quit"
        subprocess.run(command, shell=True, check=True)
    
    xschem_netlist("inverter","inverter")

    return


@app.cell
def _(mo):
    slider = mo.ui.slider(1, 10)
    mo.md(f"Choose a value: {slider}")
    return


@app.cell
def _(mo):
    mo.md(r"Finally use the netslist in pyspice to simulate!")
    return


@app.cell
def _():
    import hdl21 as h
    import hdl21.sim as hs
    import vlsirtools.spice as vsp

    return


@app.cell
def _():
    from PySpice.Spice.NgSpice.Shared import NgSpiceShared
    ngspice = NgSpiceShared.new_instance()
    file = open("inverter/inverter.spice", 'r')
    circuit = file.read()
    print(circuit)
    ngspice.load_circuit(circuit)
    # fhdjhfdj.voltage = slider.value
    ngspice.run()
    return


if __name__ == "__main__":
    app.run()
