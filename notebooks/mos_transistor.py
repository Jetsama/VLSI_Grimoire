import marimo
__generated_with = "0.13.6"
app = marimo.App(width="medium", html_head_file="head.html")

import js

print("Hello world!")
print(js)
script = js.document.createElement("script");
script.src = "/ngspice.js"
js.document.body.appendChild(script);

script = js.document.createElement("p");
script.innerHTML = "TEST TEST TEST!"
js.document.body.appendChild(script);

@app.cell
def _(mo):
    mo.md(r"# MOS transistor example")
    return


@app.cell
def _(mo):
    mo.md(r"Showing a simple MOS example using marimo and a simulator.")
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
    # import js
    # import pyodide
    # pyodide.send("load_ngspice", {"src": "/ngspice.js"})
    # from pyscript import window, document
    script = js.document.createElement("script");
    script.src = "/ngspice.js"
    script.type = "text/javascript"
    js.document.body.appendChild(script);
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        _esm = """
        function render({ model, el }) {
        let button = document.createElement("button");
        button.innerHTML = `count is ${model.get("value")}`;
        button.addEventListener("click", () => {
            model.set("value", model.get("value") + 1);
            model.save_changes();
        });
        model.on("change:value", () => {
            button.innerHTML = `count is ${model.get("value")}`;
        });
        el.classList.add("counter-widget");
        el.appendChild(button);
        }
        export default { render };
        """
        _css = """
        .counter-widget button { color: white; font-size: 1.75rem; background-color: #ea580c; padding: 0.5rem 1rem; border: none; border-radius: 0.25rem; }
        .counter-widget button:hover { background-color: #9a3412; }
        """
        value = traitlets.Int(0).tag(sync=True)

    CounterWidget(value=42)
    return


@app.cell
def _(mo):
    mo.md(r"Test of respice!")
    return


@app.cell
def _():
    from respice.analysis import Circuit
    from respice.components import CurrentSourceDC, R, C

    # Define components for our circuit.
    R1 = R(100)
    R2 = R(200)
    C3 = C(10e-6)
    R4 = R(200)
    R5 = R(100)
    Isrc = CurrentSourceDC(0.1)

    # Construct the circuit. All circuits are just
    # Digraphs allowing multiple edges. On each edge
    # one component.
    wheatstone_bridge = Circuit()
    wheatstone_bridge.add(R1, 0, 1)
    wheatstone_bridge.add(R2, 0, 2)
    wheatstone_bridge.add(C3, 1, 2)
    wheatstone_bridge.add(R4, 1, 3)
    wheatstone_bridge.add(R5, 2, 3)
    wheatstone_bridge.add(Isrc, 3, 0)

    # Simulate! From t1 = 0ms to t2 = 5ms with 100 steps.
    simulation = wheatstone_bridge.simulate(0, 0.005, 100)
    simulation.plot()

    return


if __name__ == "__main__":

    app.run()
