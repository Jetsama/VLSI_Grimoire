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
    # testbench = '''
    # .lib /foss/pdks/sky130A/libs.tech/ngspice/sky130.lib.spice tt
    # XM1 IN IN VSS VSS sky130_fd_pr__nfet_01v8 L=0.15 W=1 nf=1 ad='int((nf+1)/2) * W/nf * 0.29' as='int((nf+2)/2) * W/nf * 0.29' pd='2*int((nf+1)/2) * (W/nf + 0.29)'
    # + ps='2*int((nf+2)/2) * (W/nf + 0.29)' nrd='0.29 / W' nrs='0.29 / W' sa=0 sb=0 sd=0 mult=1 m=1
    # XM2 IN IN VDD VDD sky130_fd_pr__pfet_01v8 L=0.15 W=1 nf=1 ad='int((nf+1)/2) * W/nf * 0.29' as='int((nf+2)/2) * W/nf * 0.29' pd='2*int((nf+1)/2) * (W/nf + 0.29)'
    # + ps='2*int((nf+2)/2) * (W/nf + 0.29)' nrd='0.29 / W' nrs='0.29 / W' sa=0 sb=0 sd=0 mult=1 m=1
    # **** begin user architecture code


    # '''

    # circuit = testbench
    circuit = circuit.replace(".end\n",
                              f"VDD VDD 0 1.8\nVSS VSS 0 0\nVIN IN 0 0\n.op \n.end\n"
                              #tran 50u 50m
                              )
    print(circuit)
    ngspice.load_circuit(circuit)
    # fhdjhfdj.voltage = slider.value
    ngspice.run()
    return (ngspice,)


@app.cell
def _(ngspice):
    print('Plots:', ngspice.plot_names)
    plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
    import matplotlib.pyplot as plt
    print(plot)
    fig, ax = plt.subplots()
    ax.plot(plot['vdd']._data)
    print(plot['vdd']._data)
    print(f"input: {plot['in']._data}")
    print(f"output: {plot['out']._data}")
    return


if __name__ == "__main__":
    app.run()
