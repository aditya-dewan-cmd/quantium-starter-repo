import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load the sales data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Create the Dash app
app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "marginBottom": "10px"
            }
        ),

        html.P(
            "Explore Pink Morsel sales by region",
            style={
                "textAlign": "center",
                "fontSize": "18px"
            }
        ),

        html.Div(
            [
                html.Label(
                    "Select Region:",
                    style={
                        "fontWeight": "bold",
                        "marginRight": "15px"
                    }
                ),

                dcc.RadioItems(
                    id="region-selector",
                    options=[
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                        {"label": "All", "value": "all"}
                    ],
                    value="all",
                    inline=True
                )
            ],
            style={
                "textAlign": "center",
                "marginBottom": "20px"
            }
        ),

        dcc.Graph(id="sales-chart")
    ],
    style={
        "maxWidth": "1100px",
        "margin": "auto",
        "padding": "30px"
    }
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-selector", "value")
)
def update_chart(selected_region):

    if selected_region == "all":
        filtered_df = df
    else:
        filtered_df = df[df["region"] == selected_region]

    daily_sales = (
        filtered_df
        .groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
    )

    fig = px.line(
        daily_sales,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Total Sales"
        }
    )

    fig.add_vline(
        x=pd.Timestamp("2021-01-15"),
        line_dash="dash",
        annotation_text="Price Increase",
        annotation_position="top"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font={"size": 14},
        title_x=0.5
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)