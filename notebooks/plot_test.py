import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium", html_head_file="head.html")


@app.cell
def _(mo):
    mo.md(r"# Simple Plot Test")
    return


@app.cell
def _(mo):
    mo.md(r"Showing a simple plotting example using marimo.")
    return


@app.cell
def _():
    # import micropip
    # await micropip.install("pandas")
    # await micropip.install("plotly")
    import plotly
    #checking for updates
    import pandas
    import plotly.express as px
    import marimo as mo
    plot = mo.ui.plotly(
        px.scatter(x=[0, 1, 4, 9, 16], y=[0, 1, 2, 3, 4], width=600, height=300)
    )
    plot
    return (mo,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
