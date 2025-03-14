from Excel_functions import year_to_year_percent


def calculate_family_portfolios_year_to_years(ignar_total_portfolio: int, morr_total_portfolio: int, kelly_total_portfolio: int) -> None:

    PORTFOLIO_FILTER_DATE = "01-01"
    print("===================================Ignar's=======================================")
    print(
        year_to_year_percent(
            excel_name="Portfell",
            mm_dd=PORTFOLIO_FILTER_DATE,
            todays_total_portfolio=ignar_total_portfolio,
            portfolio_history_column="F",
        )
    )
    print("=====================================Mörr's======================================")
    print(
        year_to_year_percent(
            excel_name="Portfell",
            mm_dd=PORTFOLIO_FILTER_DATE,
            todays_total_portfolio=morr_total_portfolio,
            portfolio_history_column="G",
            filter_nr_input=2000,
        )
    )
    print("=====================================Kelly's=====================================")
    print(
        year_to_year_percent(
            excel_name="Portfell",
            mm_dd=PORTFOLIO_FILTER_DATE,
            todays_total_portfolio=kelly_total_portfolio,
            portfolio_history_column="L",
            filter_nr_input=2,
        )
    )
    print("=================================================================================")
