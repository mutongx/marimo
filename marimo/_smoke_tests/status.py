# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
# ]
# ///
# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.8.11"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import time
    return mo, time


@app.cell
def __(mo):
    sleep_time_radio = mo.ui.radio(
        [".01", ".1", "1"], label="Sleep time", value=".01"
    )
    sleep_time_radio
    return sleep_time_radio,


@app.cell
def __(sleep_time_radio):
    sleep_time = float(sleep_time_radio.value)
    return sleep_time,


@app.cell
def __(mo):
    disabled_switch = mo.ui.switch(label="Disable progress bar")
    disabled_switch
    return disabled_switch,


@app.cell
def __(disabled_switch, mo, sleep_time, time):
    for _ in mo.status.progress_bar(
        range(10),
        title="Loading",
        subtitle="Please wait",
        disabled=disabled_switch.value,
    ):
        time.sleep(sleep_time)
    return


@app.cell
def __(disabled_switch, mo, sleep_time, time):
    for _ in mo.status.progress_bar(
        range(10),
        title="Loading",
        subtitle="Please wait",
        show_eta=True,
        show_rate=True,
        disabled=disabled_switch.value,
    ):
        time.sleep(sleep_time)
    return


@app.cell
def __(disabled_switch, mo, sleep_time, time):
    with mo.status.progress_bar(
        title="Loading",
        subtitle="Please wait",
        total=10,
        disabled=disabled_switch.value,
    ) as bar:
        for _ in range(10):
            time.sleep(sleep_time)
            bar.update()
    return bar,


@app.cell
def __(mo, sleep_time, time):
    with mo.status.spinner(title="Loading...", remove_on_exit=True) as _spinner:
        time.sleep(0.1)
        _spinner.update("Almost done")
        time.sleep(sleep_time)
    return


@app.cell
def __(mo, sleep_time, time):
    with mo.status.spinner(title="Loading...", remove_on_exit=True) as _spinner:
        time.sleep(sleep_time)
        _spinner.update("Almost done")
        time.sleep(sleep_time)
    mo.ui.table([1, 2, 3])
    return


@app.cell
def __(disabled_switch, mo, sleep_time, time):
    # Fast updates should be debounced for performance
    for i in mo.status.progress_bar(
        range(1000),
        disabled=disabled_switch.value,
    ):
        time.sleep(sleep_time / 10)
    return i,


if __name__ == "__main__":
    app.run()
