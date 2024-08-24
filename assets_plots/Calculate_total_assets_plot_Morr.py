import plotly.graph_objs as go
from Aktsiad import get_stock_price
from Morr import (
    LAHTSE_RAHA,
    MORR_EUR_STOCKS,
    TAHTAJALINE_HOIUS,
    LHV_VOLAKIRI,
    BIGBANK_VOLAKIRI,
    HOLM_VOLAKIRI,
    LIVEN_VOLAKIRI,
    INBANK_VOLAKIRI,
    MORR_RAHA,
)

symbol_to_name: dict = {
    "TSM1T": "Tallinna Sadam",
    "TAL: TKM1T": "Tallinna Kaubamaja",
    "EFT1T": "EfTEN Real Estate Fund III",
    "EXXT.DE": "ETF NASDAQ100",
    "SPYW.DE": "ETF S&P 500",
}


fys_euro_stocks: dict = {
    stock_sym: int(round(get_stock_price(stock_sym, True) * stock_amount, 0))
    for stock_sym, stock_amount in MORR_EUR_STOCKS.items()
}

# combine the two dictionaries
stocks_assets: dict = {**fys_euro_stocks}
stock_with_names_assets: dict = {symbol_to_name.get(key, key): value for key, value in stocks_assets.items()}
print(stock_with_names_assets)


assets = {
    "LHV Võlakirjad": LHV_VOLAKIRI,
    "Bigbank Võlakirjad": BIGBANK_VOLAKIRI,
    "Holm Bank Võlakirjad": HOLM_VOLAKIRI,
    "InBank Võlakirjad": INBANK_VOLAKIRI,
    "Liven Võlakirjad": LIVEN_VOLAKIRI,
    "Kinnisvara: Maja ehitus": LAHTSE_RAHA / 2,
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
fig = go.Figure(
    data=[go.Pie(labels=label_text, values=list(assets.values()), hoverinfo="percent+text", text=hover_text)]
)

# Update the layout for a cleaner look
fig.update_layout(title="Finance Portfolio Overview", showlegend=True)
# title to center
fig.update_layout(title_x=0.5)
fig.show()
