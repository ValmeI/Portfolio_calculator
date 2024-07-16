import plotly.graph_objs as go
from Valme import (
    JUR_FUNDERBEAM,
    JUR_USA_STOCKS,
    JUR_EUR_STOCKS,
    FYS_EUR_STOCKS,
    LHV_VOLAKIRI,
    BIGBANK_VOLAKIRI,
    HOLM_VOLAKIRI,
    LIVEN_VOLAKIRI,
    CLEVERON_AKTSIA,
)
from Aktsiad import stock_price_from_google
from Kinnisvara import Korter1_Hind
from Morr import LAHTSE_RAHA

symbol_to_name: dict = {
    "AAPL": "Apple",
    "TSLA": "Tesla",
    "AMD": "AMD",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "GOOGL": "Google",
    "NIO": "NIO",
    "XPEV": "Xpeng - ADR",
    "NKE": "Nike",
    "INTC": "Intel",
    "SNOW": "Snowflake",
    "IUSE.MI": "S&P 500",
    "BRK.B": "Berkshire Hathaway B",
    "QCOM": "Qualcomm",
    "TAL: TKM1T": "Tallinna Kaubamaja",
    "EFT1T": "EfTEN Real Estate Fund III",
}


jur_usa_stocks: dict = {
    stock_sym: round(stock_price_from_google(stock_sym, False) * stock_amount, 0)
    for stock_sym, stock_amount in JUR_USA_STOCKS.items()
}

jur_euro_stocks: dict = {
    stock_sym: round(stock_price_from_google(stock_sym, True) * stock_amount, 0)
    for stock_sym, stock_amount in JUR_EUR_STOCKS.items()
}

fys_euro_stocks: dict = {
    stock_sym: round(stock_price_from_google(stock_sym, True) * stock_amount, 0)
    for stock_sym, stock_amount in FYS_EUR_STOCKS.items()
}

# combine the two dictionaries
stocks_assets: dict = {**jur_euro_stocks, **fys_euro_stocks, **jur_usa_stocks}
stock_with_names_assets: dict = {symbol_to_name.get(key, key): value for key, value in stocks_assets.items()}
print(stock_with_names_assets)
# Create an empty dictionary
assets = {}

# Add the first set of keys and values to the dictionary
assets.update(
    {
        "Funderbeam Kokku": JUR_FUNDERBEAM,
        "LHV Võlakirjad": LHV_VOLAKIRI,
        "Bigbank Võlakirjad": BIGBANK_VOLAKIRI,
        "Holm Bank Võlakirjad": HOLM_VOLAKIRI,
        "Liven Võlakirjad": LIVEN_VOLAKIRI,
        "Cleveron Aktsiad": CLEVERON_AKTSIA,
        "Kinnisvara: Akadeemia 12 m2": Korter1_Hind,
        "Kinnisvara: Maja ehitus": LAHTSE_RAHA / 2,
    }
)

# Add the second set of keys and values to the dictionary
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
