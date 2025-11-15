import marimo

__generated_with = "0.17.8"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # Inverter (NOT gate)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    In digital logic an inverter, or NOT gate, flips the state. It is the same as its english conterpart.

    | A | NOT(A) |
    |---|---|
    | FALSE | TRUE |
    | TRUE | FALSE |

    Instead of writing TRUE/FALSE we can use 1/0 instead. This has many benifits for logic, but that can be seen in later sections.
    | A | NOT(A) |
    |---|---|
    | 0 | 1 |
    | 1 | 0 |

    Here's an implemntation of a not gate using a python function!
    """)
    return


@app.function
def not_gate(value:bool):
    return not value


@app.cell
def _():
    for A in [False,True]:
        print(f"Input: {A}, Output:{not_gate(A)}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    Not very remarkable function to be honest. But I guess that makes sense as it only has two potential outputs.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## So.... uh... what about the VLSI stuff?
    Oh, right. Well that looks like this!

    image of digital logic symbol

    or maybe...

    ```verilog
    not(A,Y)
    ```
    and...

    schematic

    oh and can't forget ...

    layout
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### What is happening?
    You may (should) be confused about any/all of the previous examples if new to VLSI. While technically all of these are a NOT gate used in VLSI, they are used in different ways.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Abstraction with a side of onions
    As a general rule, engineers, like most people, do not like going insane. To curb insanity and increase productivity, engineers use abstractions.

    Here is an example of abstraction of a car:
    Image
    drawing
    sketch
    child drawing
    word: car

    Digital logic

    Similar to onions, and orgres, VLSI has layers. And what things look like depends on which layer you're intrested in.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Why? I wouldn't mind going a little insane

    #### Switching implementations
    If you want to switch from implementing your design in VLSI to minecraft, [water](https://www.youtube.com/watch?v=IxXaizglscw), or even [physical desk toy](https://github.com/Jetsama/DigitalLogicProject), the work to switch becomes much easier! This is because all implementation detail is stored in a lower level that can be updated without changing the higher level details. Although, depending on the medium, higher level changes could still be necessary.

    Even in VLSI swithcing between processes is made much easier by abstracting your design.

    #### Automation
    A design, has to be able to go to the lowest level implementation. For simple designs this may be possible, ......

    #### Clarity and collaboration
    Although you may not care about the insanity, higher levels of abstraction can also help others from going mad. Which allows for easier divisioning of work to sub-projects.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
