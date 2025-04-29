import sys
import time
import warnings
from datetime import date
import datetime
from colored import attr, fg
from dateutil.relativedelta import relativedelta
import excel_functions
import kinnisvara
from family import calculate_family_portfolios_year_to_years
import txt_write_move
from portfolio_owners import morr, kelly, valme
from excel_functions import column_width, HEADERS, need_new_excel_file, write_to_excel
from functions import diff_months
import utils

# to IGNORE: UserWarning: Cannot parse header or footer so it will be ignored'
# warn("""Cannot parse header or footer so it will be ignored""")'
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


if __name__ == "__main__" or __name__ == "Portfell_main":
    print(f'Programm: "{__file__}" käivitus: {datetime.datetime.now()}')
    start_time = time.time()
    start_date = datetime.datetime.now()

    # create file from consol output'
    TXT_SOURCE, EXCEL_SOURCE, NAS_DES_PATH = utils.get_data_copy_paths_based_on_os()
    utils.copy_file_to_nas(TXT_SOURCE, NAS_DES_PATH)
    utils.copy_file_to_nas(EXCEL_SOURCE, NAS_DES_PATH)

    sys.stdout = txt_write_move.Logger()
    today = date.today()
    # Akadeemia 42-63 Välja ostetud 10.11.2023 - Laenujääk 12 200 EUR
    # Akadeemia 38-20 Müüdud 28.10.2021 Laenujääk 18 800 EUR'
    PerMonthVilde90 = kinnisvara.apr_month(kinnisvara.Korter3_Laen, 2.39, 11)

    print(f"{kinnisvara.Korter3_Nimi} laenumakse: {PerMonthVilde90} € + kindlustus.\n")
    dateVilde90 = relativedelta(today, valme.VILDE90_193_LAEN_KUUPAEV)
    print(f"Laenu {kinnisvara.Korter3_Nimi} makstud: {dateVilde90.years} Years, {dateVilde90.months} Months\n")

    KuudMakstudVilde90 = diff_months(today, valme.VILDE90_193_LAEN_KUUPAEV)
    BalanceVilde90 = kinnisvara.apr_balance(kinnisvara.Korter3_Laen, 6.342, 11, KuudMakstudVilde90)

    print(f"{kinnisvara.Korter3_Nimi} laenu jääk: {BalanceVilde90} €. Laenu summa: {kinnisvara.Korter3_Laen}")
    print(f"Laenu kohutus kokku(Kõik): {BalanceVilde90}")

    print(f"Val Capital: {morr.VAL_CAPITAL_RAHA / 2} €.")

    # kinnisvara kokku. Liidetakse kõikkorterite ostu hinnad - balancid ehk palju laenu veel maksta'
    kinnisvara_port = kinnisvara.calculate_real_estate_total_value() + morr.LAHTSE_ARVUTUSLIK_VAARTUS / 2

    print(f"\nHetkel korteri/krundi puhas väärtus kokku: {kinnisvara_port} €.")
    print(f"\nLähtse Väärtus: {fg('red')}{morr.LAHTSE_ARVUTUSLIK_VAARTUS / 2}{attr('reset')} €.")

    # Portfell kokku'
    ignar_total = valme.FysIsik + valme.JurIsik + kinnisvara_port

    # Ehk 1 000 000 Eesti krooni'
    EESMARK_1 = round(1000000 / 15.6466)
    EESMARK_2 = 500000
    print(f"Vilde peale makse Isale: {fg('red')}{valme.Uus_vilde_summa}{attr('reset')} €.")
    print("\n")
    print(f"Juriidilise isiku väärtus: {valme.JurIsik} €.")
    print(f"Krüpto: {fg('red')}{valme.Jur_Krypto}{attr('reset')} €.")
    print(f"Juriidilise isiku aktsiad: {valme.Juraktsiad} €.")
    print(f"Funderbeam Kokku: {fg('red')}{valme.JUR_FUNDERBEAM}{attr('reset')} €.")
    print(f"Võlakirjade väärtus: {fg('red')}{valme.VOLAKIRJAD_KOKKU}{attr('reset')} €.")
    print("\n")
    print(f"Füüsilise isiku aktsia portfell: {valme.FysIsik} €.")
    print(f"Aktsiadaktsiad/Raha Jur ja Füs isikud kokku: {valme.FysIsik + valme.JurIsik} €.")
    print(f"Vaba raha Jur/Füs Kokku: {fg('red')}{valme.RahaKokku}{attr('reset')} €.")

    print("\n")
    print(f"Terve portfell kokku: {fg('red')}{round(ignar_total)}{attr('reset')} €.")
    print(f"Eesmärk krooni miljonär: {EESMARK_1} €.")
    print(f"Krooni miljonär veel minna: {EESMARK_1 - ignar_total} €.")
    age = date.today() - date(1990, 2, 19)
    years = age.days // 365
    months = (age.days % 365) // 30
    print(f"Eesmärk 35 aastaselt portfelli väärtus {EESMARK_2} €. Vanus hetkel: {years} years, {months} months")
    print(f"35 aastase eesmärk veel minna: {fg('red')}{round(EESMARK_2 - ignar_total)}{attr('reset')} €.")

    morr_total = morr.kokku
    print(f"Mörr-i aktsiad: {morr.m_aktsiad} €.")
    print(f"Mörr-i Val Capital: {morr.VAL_CAPITAL_RAHA / 2} €.")
    print(f"Mörr-i vaba raha: {morr.MORR_RAHA} €.")
    print(f"Mörr-i Lähse väärtus: {morr.LAHTSE_ARVUTUSLIK_VAARTUS / 2} €.")
    print(f"Mörr-i portfell kokku: {fg('red')}{morr_total}{attr('reset')} €.")

    # kelly Portfell'
    kelly_total = kelly.Kelly_Portfell_Kokku
    print(f"Kelly portfell: {fg('red')}{kelly_total}{attr('reset')} €.")

    # Pere kõik kokku'
    Pere = ignar_total + morr_total + kelly_total
    print(f"Pere portfell kokku: {fg('red')}{round(Pere)}{attr('reset')} €.")

    aktsiad_kokku = valme.FysIsik + valme.JurIsik
    # check if new Excel file is needed and if so, create it
    need_new_excel_file(excel_name="Portfell", sheet_name="Porfelli Info", excel_headers=excel_functions.HEADERS)

    calculate_family_portfolios_year_to_years(ignar_total, morr_total, kelly_total)

    # make a list with all the data for Excel file input
    values_list = []
    values_list.extend(
        (
            str(today),
            kinnisvara_port,
            valme.FysIsik,
            valme.JurIsik,
            aktsiad_kokku,
            ignar_total,
            morr_total,
            Pere,
            valme.Uus_vilde_summa,
            valme.RahaKokku,
            valme.JUR_FUNDERBEAM,
            kelly_total,
        )
    )

    # how_to_add: 1 = append, 2 = overwrite, 3 = compare if change is needed
    # compare_column for overwrite: 1 is first column in excel (A) and 2 is B and so on
    write_to_excel(excel_name="Portfell", list_of_data=values_list, how_to_add=2, compare_column=1)
    column_width(excel_name="Portfell", excel_headers=HEADERS)
    mail_body = utils.generate_mail_body(
        portfolio_goal_no_1=EESMARK_1,
        portfolio_goal_no_2=EESMARK_2,
        kelly_total_portfolio=kelly_total,
        family_total_portfolio=Pere,
        ignar_total_portfolio=ignar_total,
        morr_stocks=morr.m_aktsiad,
        morr_free_cash=morr.MORR_RAHA,
        morr_total_portfolio=morr_total,
        vilde_apartment=dateVilde90,
        real_estate=kinnisvara,
        vilde_balance=BalanceVilde90,
    )
    utils.check_if_and_send_email(mail_body=mail_body, day_to_send_email="Sunday", send_every_day=True)

    print(f"Program took: {round(time.time() - start_time)} seconds to run")
    print("=================================================================================")
    print(
        f"Program Start_Time: {start_date.strftime('%Y-%m-%d %H:%M:%S')} and End_time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
