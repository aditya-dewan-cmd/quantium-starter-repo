import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load the sales data
df = pd.read_csv("formatted_sales_data.csv")

# Convert date to datetime
df["date"] = pd.to_datetime(df["date"])

# Add sales from all regions for each date
daily_sales = df.groupby("date", as_index=False)["sales"].sum()

# Sort by date
daily_sales = daily_sales.sort_values("date")

# Create the line chart
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

# Mark the price increase date
fig.add_vline(
    x=pd.Timestamp("2021-01-15"),
    line_dash="dash",
    annotation_text="Price Increase",
    annotation_position="top"
)

# Create the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)