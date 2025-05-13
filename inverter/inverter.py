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
def _():
    import subprocess
    def xschem_draw(file):
        subprocess.run(f"xschem --png --plotfile {file}.png {file}.sch --quit", shell=True, check=True)
    xschem_draw("inverter/inverter")
    return


@app.cell
def _(mo):
    mo.md(r"![testout.png](./inverter.png)")
    return


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


if __name__ == "__main__":
    app.run()
