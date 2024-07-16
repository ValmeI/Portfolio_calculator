import plotly.graph_objs as go

# Generate static plot of total assets in portfolio. Make this Dynamic in the future.


# Create an empty dictionary
assets = {}

# Add the first set of keys and values to the dictionary
assets.update(
    {
        "Funderbeam Kokku": 8000,
        "LHV Võlakirjad": 2000,
        "Cleveron Aktsiad": 600,
        "Kinnisvara: Akadeemia 12 m2": 24500,
        "Kinnisvara: Maja ehitus": 51185,
    }
)

# Add the second set of keys and values to the dictionary
assets.update(
    {
        "Tallinna Kaubamaja": 3514,
        "EfTEN": 2124,
        "Apple": 11972,
        "Tesla": 3226,
        "AMD": 8713,
        "Microsoft": 4826,
        "Amazon": 7505,
        "Google": 4494,
        "NIO": 629,
        "Xpeng - ADR": 1215,
        "Nike": 1081,
        "Intel": 1004,
        "Snowflake": 938,
        "S&P500": 2194,
        "Berkshire Hathaway B": 662,
    }
)


kokku_varad = sum(assets.values())

# Create hover text for each asset
hover_text = [f"{label}: {value} EUR" for label, value in zip(assets.keys(), assets.values())]
label_text = [
    f"{label}: {value} EUR - {percent:.2f}%"
    for label, value, percent in zip(assets.keys(), assets.values(), [x / kokku_varad * 100 for x in assets.values()])
]

# Create the pie chart
fig = go.Figure(
    data=[go.Pie(labels=label_text, values=list(assets.values()), hoverinfo="percent+text", text=hover_text)]
)

# Update the layout for a cleaner look
fig.update_layout(title="Finance Portfolio Overview", showlegend=True)
# title to center
fig.update_layout(title_x=0.5)
fig.show()
