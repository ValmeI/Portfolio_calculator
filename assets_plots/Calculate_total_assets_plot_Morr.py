import plotly.graph_objs as go




from aktsiad import StockManager

from portfolio_owners.morr import (
    LAHTSE_ARVUTUSLIK_VAARTUS,
    MORR_EUR_STOCKS,
    TAHTAJALINE_HOIUS,
    VOLAKIRJAD_KOKKU,
    MORR_RAHA,
)

margit_plot_stocks_manager = StockManager("Margit_plot")

symbol_to_name: dict = {
    "TSM1T.TL": "Tallinna Sadam",
    "TKM1T.TL": "Tallinna Kaubamaja",
    "EFT1T": "EfTEN Real Estate Fund III",
    "EFT1T.TL": "EfTEN Real Estate Fund III",
    "EXXT.ETF": "ETF NASDAQ100",
    "EXXT.DE": "ETF NASDAQ100",
    "SPYW.DE": "ETF S&P 500",
}


fys_euro_stocks: dict = {
    stock_sym: int(round(margit_plot_stocks_manager.get_stock_price_for_plot(stock_sym, True) * stock_amount, 0))
    for stock_sym, stock_amount in MORR_EUR_STOCKS.items()
}

stocks_assets: dict = {**fys_euro_stocks}
stock_with_names_assets: dict = {symbol_to_name.get(key, key): value for key, value in stocks_assets.items()}
print(stock_with_names_assets)


assets = {
    "Võlakirjad kokku": VOLAKIRJAD_KOKKU,
    "kinnisvara: Maja ehitus": LAHTSE_ARVUTUSLIK_VAARTUS / 2,
    "Tähtajaline hoius": TAHTAJALINE_HOIUS,
    "Vaba Raha": MORR_RAHA,
}

assets.update({**stock_with_names_assets})

kokku_varad = sum(assets.values())

# Create hover text for each asset
hover_text = [f"{label}: {value} EUR" for label, value in zip(assets.keys(), assets.values())]
label_text = [
    f"{label}: {value} EUR - {percent:.2f}%"
    for label, value, percent in zip(assets.keys(), assets.values(), [x / kokku_varad * 100 for x in assets.values()])
]

# Create the pie chart
fig = go.Figure(data=[go.Pie(labels=label_text, values=list(assets.values()), hoverinfo="percent+text", text=hover_text)])

# Update the layout for a cleaner look
fig.update_layout(title="Finance Portfolio Overview", showlegend=True)

# Add the total amount as an annotation
fig.add_annotation(
    text=f"Total: {round(kokku_varad)} EUR",
    x=0.5,  # Position in the middle
    y=-0.1,  # Position below the pie chart
    showarrow=False,
    font=dict(size=16),
    xref="paper",
    yref="paper",
)

# title to center
fig.update_layout(title_x=0.5)
fig.show()
