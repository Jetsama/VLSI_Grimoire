import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium", html_head_file="head.html")


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
    return


@app.cell
def _():
    return


# app._unparsable_cell(
#     r"""
#     mo.md(r\"<kicanvas-embed src=\"https://raw.githubusercontent.com/Jetsama/DigitalLogicProject/refs/heads/main/PCBS/BOARD/BOARD.kicad_sch\" controls=\"basic\"> </kicanvas-embed>\")
#     """,
#     name="_"
# )


if __name__ == "__main__":
    app.run()
