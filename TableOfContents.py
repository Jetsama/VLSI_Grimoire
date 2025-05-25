import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"# Table of Contents")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        [MOSFET Examples]()
    
        [Inverter Example](/workspaces/VLSI_Grimoire/inverter/inverter.py)
        """
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
