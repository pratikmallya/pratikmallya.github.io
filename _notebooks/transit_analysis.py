import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    mo.md(r"""
    ## Visualizing DOT Transit data

    This notebook extracts and shapes raw data from [DOT's Transit Ridership data], and generates interactive plots to allow anyone to explore this data.

    The raw data is shared by DOT in the form of a spreadsheet with several "sheets". We will be looking at the `upt` sheet, which contains data for Unlinked Passenger Trips [^1]

    [DOT's Transit Ridership data]: https://www.transit.dot.gov/sites/fta.dot.gov/files/2026-03/January%202026%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29_260302.xlsx
    [^1]: The number of passengers who board public transportation vehicles. Passengers are counted each time they board vehicles no matter how many vehicles they use to travel from their origin to their destination. From https://www.transit.dot.gov/ntd/national-transit-database-ntd-glossary
    """)

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lets see what the data looks like using duckdb. Use `DESCRIBE` on the data.
    """)
    return


@app.cell
def _():
    import duckdb

    DOT_TRANSIT_DATA_REMOTE="https://www.transit.dot.gov/sites/fta.dot.gov/files/2026-03/January%202026%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29_260302.xlsx"
    DOT_TRANSIT_DATA_LOCAL="/Users/pratikmallya/Downloads/ridership.xlsx"


    duckdb.sql(f"DESCRIBE FROM read_xlsx('{DOT_TRANSIT_DATA_LOCAL}', sheet='UPT')")
    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    299 columns, thats a lot! This is because there is one column for every month. This makes it quite difficult to plot this effectively. We need to transform this a little bit to make it more plot-friendly.

    One way to do this is to use the [SQL UNPIVOT] function to convert the columns into rows.

    [SQL UNPIVOT]: https://duckdb.org/docs/stable/sql/statements/unpivot
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First though, lets make it easier to query this data by creating a table from the data in the sheets:
    """)
    return


@app.cell
def _(duckdb):
    duckdb.sql("CREATE OR REPLACE TABLE upt AS SELECT * FROM read_xlsx('/Users/pratikmallya/Downloads/ridership.xlsx', sheet= 'UPT')")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, lets run the `UNPIVOT` command to massage the data into something easier to plot:
    """)
    return


@app.cell
def _(duckdb):
    duckdb.sql("""
        CREATE OR REPLACE TABLE upt_long AS
        UNPIVOT (
            SELECT "NTD ID", Agency, Mode, TOS, "UZA Name",
                   * EXCLUDE ("NTD ID", "Legacy NTD ID", Agency, 
                              "Mode/Type of Service Status", "Reporter Type", 
                              "UACE CD", "UZA Name", Mode, TOS, "3 Mode")
            FROM upt
        )
        ON COLUMNS(* EXCLUDE ("NTD ID", Agency, Mode, TOS, "UZA Name"))
        INTO NAME month VALUE upt
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lets look at the table we just created:
    """)
    return


@app.cell
def _(duckdb, mo, upt_long):
    mo.ui.table(duckdb.sql("SELECT * from upt_long"))
    return


@app.cell
def _(duckdb, upt_long):
    import pandas as pd
    import altair as alt

    # Get the full dataframe once
    df = duckdb.sql("""
        SELECT Agency, Mode, TOS, "UZA Name", month, upt
        FROM upt_long
    """).df()
    df['date'] = pd.to_datetime(df['month'], format='%m/%Y')

    return alt, df


@app.cell
def _(df, mo):
    # Cell 1: UZA dropdown
    uza_options = ['---'] + sorted(df['UZA Name'].unique().tolist())
    uza_dropdown = mo.ui.dropdown(
        options=uza_options,
        value='---',
        label='UZA'
    )
    return (uza_dropdown,)


@app.cell
def _(df, mo, uza_dropdown):
    # Cell 2: agency multiselect — depends on uza_dropdown
    available_agencies = sorted(
        df['Agency'].unique().tolist()
        if uza_dropdown.value == '---'
        else df[df['UZA Name'] == uza_dropdown.value]['Agency'].unique().tolist()
    )
    agency_multiselect = mo.ui.multiselect(
        options=available_agencies,
        value=available_agencies if uza_dropdown.value != '---' else available_agencies[:5],
        label='Select Agencies'
    )
    return (agency_multiselect,)


@app.cell
def _(df, mo):
    # Cell 3: mode multiselect — independent, doesn't cause resets
    mode_multiselect = mo.ui.multiselect(
        options=sorted(df['Mode'].unique().tolist()),
        value=['CR', 'MB'],
        label='Modes'
    )
    return (mode_multiselect,)


@app.cell
def _(mo):
    # Cell 4: year range slider — independent cell
    year_slider = mo.ui.range_slider(
        start=2002,
        stop=2026,
        value=[2015, 2026],
        label='Year Range'
    )
    return (year_slider,)


@app.cell
def _(
    agency_multiselect,
    alt,
    df,
    mo,
    mode_multiselect,
    uza_dropdown,
    year_slider,
):
    filtered = df[
        (df['Agency'].isin(agency_multiselect.value)) &
        (df['Mode'].isin(mode_multiselect.value)) &
        (df['date'].dt.year >= year_slider.value[0]) &
        (df['date'].dt.year <= year_slider.value[1])
    ]


    chart = alt.Chart(filtered).mark_line().encode(
        x=alt.X('date:T', title='Month'),
        y=alt.Y('upt:Q', title='Unlinked Passenger Trips'),
        color='Agency:N',  # color by agency instead of mode for comparison
        strokeDash='Mode:N',  # use line style to distinguish modes
        tooltip=['Agency', 'Mode', 'date:T', 'upt:Q']
    ).properties(
        title='Ridership Comparison',
        width=800,
        height=400
    ).interactive()

    mo.vstack([
        mo.hstack([uza_dropdown, agency_multiselect, mode_multiselect]),
        year_slider,
        chart
    ])
    return


if __name__ == "__main__":
    app.run()
