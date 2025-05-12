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

    circuit = '''
    .title Voltage Multiplier

    .SUBCKT 1N4148 1 2
    *
    R1 1 2 5.827E+9
    D1 1 2 1N4148
    *
    .MODEL 1N4148 D
    + IS = 4.352E-9
    + N = 1.906
    + BV = 110
    + IBV = 0.0001
    + RS = 0.6458
    + CJO = 7.048E-13
    + VJ = 0.869
    + M = 0.03
    + FC = 0.5
    + TT = 3.48E-9
    .ENDS

    Vinput in 0 DC 0V AC 1V SIN(0V 10V 50Hz 0s 0Hz)
    C0 in 1 1mF
    X0 1 0 1N4148
    C1 0 2 1mF
    X1 2 1 1N4148
    C2 1 3 1mF
    X2 3 2 1N4148
    C3 2 4 1mF
    X3 4 3 1N4148
    C4 3 5 1mF
    X4 5 4 1N4148
    R1 5 6 1MegOhm
    .options TEMP = 25°C
    .options TNOM = 25°C
    .options filetype = binary
    .options NOINIT
    .ic
    .tran 0.0001s 0.4s 0s
    .end
    '''
    # circuit.R(2, 'out', 0, raw_spice='1k')

    print(circuit)
    return (circuit,)


@app.cell
def _(circuit):
    from PySpice.Spice.NgSpice.Shared import NgSpiceShared
    ngspice = NgSpiceShared.new_instance()
    print(circuit)

    ngspice.load_circuit(circuit)
    ngspice.run()
    return (ngspice,)


@app.cell
def _(ngspice):
    plot = ngspice.plot(simulation=None, plot_name=ngspice.last_plot)
    print(plot)
    return (plot,)


@app.cell
def _(plot):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot(plot['V(6)']._data)

    # ax.set(xlabel='time (s)', ylabel='voltage (mV)',
    #        title='About as simple as it gets, folks')
    ax.grid()

    ax
    return


if __name__ == "__main__":
    app.run()
