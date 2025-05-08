import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
async def _(mo):
    import micropip
    await micropip.install("pandas")
    await micropip.install("plotly")
    import plotly.express as px
    plot = mo.ui.plotly(
        px.scatter(x=[0, 1, 4, 9, 16], y=[0, 1, 2, 3, 4], width=600, height=300)
    )
    plot
    return


if __name__ == "__main__":
    app.run()
