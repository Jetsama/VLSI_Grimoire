import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import PySpice.Logging.Logging as Logging
    logger = Logging.setup_logging()


    from PySpice.Spice.Netlist import Circuit
    # from PySpice.Unit import *

    circuit = Circuit('Test')

    circuit.raw_spice = '''
    Vinput in 0 10V
    R1 in out 9kOhm
    '''
    circuit.R(2, 'out', 0, raw_spice='1k')

    print(circuit)
    return (circuit,)


@app.cell
def _(circuit):
    from PySpice.Spice.NgSpice.Shared import NgSpiceShared
    ngspice = NgSpiceShared.new_instance()

    ngspice.load_circuit(circuit)
    ngspice.run()
    return (ngspice,)


@app.cell
def _(ngspice):
    plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
    print(plot)
    return

# @app.interactive
# def _():
#     import matplotlib.pyplot as plt
#     # import marimo as mo

#     plt.plot([1, 2])
#     marimo.mpl.interactive(plt.gcf())


if __name__ == "__main__":
    app.run()
