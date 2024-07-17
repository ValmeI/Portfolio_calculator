import os
import shutil
import sys
import time
import warnings
from datetime import date
import datetime
from colored import attr, fg
from dateutil.relativedelta import relativedelta
import Excel_functions
import Kelly
import Kinnisvara
import Morr
import txt_write_move
import Valme
from Excel_functions import column_width, HEADERS, need_new_excel_file, write_to_excel, year_to_year_percent
from Functions import diff_months, what_path_for_file

# TODO: Add logguru for logging and different log levels so debug/warning can be turned off from output

# import from upper directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Projects.My_Send_Email.Send import send_email  # type: ignore

# to IGNORE: UserWarning: Cannot parse header or footer so it will be ignored'
# warn("""Cannot parse header or footer so it will be ignored""")'
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


if __name__ == "__main__":
    print(f'Programm: "{__file__}" käivitus: {datetime.datetime.now()}')
    start_time = time.time()
    start_date = datetime.datetime.now()
    PATH = what_path_for_file()
    TXT_SOURCE = PATH + r"Portfolio_calculator/Print_result.txt"
    EXCEL_SOURCE = PATH + r"Portfolio_calculator\Portfell.xlsx"
    PC_DES_PATH = PATH + r"Calculators\portfolio_result"
    NAS_DES_PATH = r"\\RMI_NAS\Python\Calculators\portfolio_result"

    # Copy txt result and excel file to NAS server, if all the files or path exists'
    if os.path.isfile(TXT_SOURCE) and os.path.isfile(EXCEL_SOURCE) and os.path.isdir(NAS_DES_PATH):
        # Copy previously created file to Calculators directory'
        shutil.copy(TXT_SOURCE, NAS_DES_PATH)
        shutil.copy(EXCEL_SOURCE, NAS_DES_PATH)
        print(f"Kopeeritud edukalt {datetime.datetime.now()}")
    else:
        print(f"Ei kopeeritud {datetime.datetime.now()}")

    # create file from consol output'
    sys.stdout = txt_write_move.Logger()

    today = date.today()
    # Akadeemia 42-63 Välja ostetud 10.11.2023 - Laenujääk 12 200 EUR
    # Akadeemia 38-20 Müüdud 28.10.2021 Laenujääk 18 800 EUR'
    PerMonthVilde90 = Kinnisvara.apr_month(Kinnisvara.Korter3_Laen, 2.39, 11)

    print(f"{Kinnisvara.Korter3_Nimi} laenumakse: {PerMonthVilde90} € + kindlustus.\n")
    dateVilde90 = relativedelta(today, Valme.VILDE90_193_LAEN_KUUPAEV)
    print(f"Laenu {Kinnisvara.Korter3_Nimi} makstud: {dateVilde90.years} Years, {dateVilde90.months} Months\n")

    KuudMakstudVilde90 = diff_months(today, Valme.VILDE90_193_LAEN_KUUPAEV)
    BalanceVilde90 = Kinnisvara.apr_balance(Kinnisvara.Korter3_Laen, 6.342, 11, KuudMakstudVilde90)

    print(f"{Kinnisvara.Korter3_Nimi} laenu jääk: {BalanceVilde90} €. Laenu summa: {Kinnisvara.Korter3_Laen}")
    print(f"Laenu kohutus kokku(Kõik): {BalanceVilde90}")

    # Kinnisvara kokku. Liidetakse kõik Dics korterite ostu hinnad - balancid ehk palju laenu veel maksta'
    kinnisvara_port = Kinnisvara.kinnisvara_vaartus() + Morr.LAHTSE_RAHA / 2

    print(f"\nHetkel korteri/krundi puhas väärtus kokku: {kinnisvara_port} €.")
    print(f"\nLähtse investeering: {fg('red')}{Morr.LAHTSE_RAHA / 2}{attr('reset')} €.")

    # Portfell kokku'
    Ignar_Kokku = Valme.FysIsik + Valme.JurIsik + kinnisvara_port

    # Ehk 1 000 000 Eesti krooni'
    EESMARK_1 = round(1000000 / 15.6466)
    EESMARK_2 = 500000
    print(f"Vilde peale makse Isale: {fg('red')}{Valme.Uus_vilde_summa}{attr('reset')} €.")
    print("\n")
    print(f"Juriidilise isiku väärtus: {Valme.JurIsik} €.")
    print(f"Krüpto: {fg('red')}{Valme.Jur_Krypto}{attr('reset')} €.")
    print(f"Juriidilise isiku aktsiad: {Valme.JurAktsiad} €.")
    print(f"Funderbeam Kokku: {fg('red')}{Valme.JUR_FUNDERBEAM}{attr('reset')} €.")
    print("\n")
    print(f"Füüsilise isiku aktsia portfell: {Valme.FysIsik} €.")
    print(f"Aktsiad/Raha Jur ja Füs isikud kokku: {Valme.FysIsik + Valme.JurIsik} €.")
    print(f"Vaba raha Jur/Füs Kokku: {fg('red')}{Valme.RahaKokku}{attr('reset')} €.")

    print("\n")
    print(f"Terve portfell kokku: {fg('red')}{round(Ignar_Kokku)}{attr('reset')} €.")
    print(f"Eesmärk krooni miljonär: {EESMARK_1} €.")
    print(f"Krooni miljonär veel minna: {EESMARK_1 - Ignar_Kokku} €.")
    age = date.today() - date(1990, 2, 19)
    years = age.days // 365
    months = (age.days % 365) // 30
    print(f"Eesmärk 35 aastaselt portfelli väärtus {EESMARK_2} €. Vanus hetkel: {years} years, {months} months")
    print(f"Veel minna: {fg('red')}{round(EESMARK_2 - Ignar_Kokku)}{attr('reset')} €.")

    Morr_kokku = Morr.kokku
    print(f"Mörr-i aktsiad: {Morr.m_aktsiad} €.")
    print(f"Mörr-i vaba raha: {Morr.MORR_RAHA} €.")
    print(f"Mörr-i portfell kokku: {fg('red')}{Morr_kokku}{attr('reset')} €.")

    # Kelly Portfell'
    Kelly_kokku = Kelly.Kelly_Portfell_Kokku
    print(f"Kelly portfell: {fg('red')}{Kelly_kokku}{attr('reset')} €.")

    # Pere kõik kokku'
    Pere = Ignar_Kokku + Morr_kokku + Kelly_kokku
    print(f"Pere portfell kokku: {fg('red')}{round(Pere)}{attr('reset')} €.")

    Aktsiad_kokku = Valme.FysIsik + Valme.JurIsik
    # check if new Excel file is needed and if so, create it
    need_new_excel_file(excel_name="Portfell", sheet_name="Porfelli Info", excel_headers=Excel_functions.HEADERS)

    # compare the current portfolio with the previous years
    print("=================Ignar's==========================")
    print(
        year_to_year_percent(
            excel_name="Portfell", mm_dd="01-01", todays_total_portfolio=Ignar_Kokku, excel_column_input="F"
        )
    )
    print("=================Mörr's===========================")
    print(
        year_to_year_percent(
            excel_name="Portfell",
            mm_dd="01-01",
            todays_total_portfolio=Morr_kokku,
            excel_column_input="G",
            filter_nr_input=2000,
        )
    )
    print("=================Kelly's==========================")
    print(
        year_to_year_percent(
            excel_name="Portfell",
            mm_dd="01-01",
            todays_total_portfolio=Kelly_kokku,
            excel_column_input="L",
            filter_nr_input=2,
        )
    )
    print("==================================================")

    # make a list with all the data for Excel file input
    values_list = []
    values_list.extend(
        (
            str(today),
            kinnisvara_port,
            Valme.FysIsik,
            Valme.JurIsik,
            Aktsiad_kokku,
            Ignar_Kokku,
            Morr_kokku,
            Pere,
            Valme.Uus_vilde_summa,
            Valme.RahaKokku,
            Valme.JUR_FUNDERBEAM,
            Kelly_kokku,
        )
    )

    # how_to_add: 1 = append, 2 = overwrite, 3 = compare if change is needed
    # compare_column for overwrite: 1 is first column in excel (A) and 2 is B and so on
    write_to_excel(excel_name="Portfell", list_of_data=values_list, how_to_add=2, compare_column=1)
    column_width(excel_name="Portfell", excel_headers=HEADERS)

    # for combining results to send in e-mail
    mail_body = (
        f"\nTerve portfell kokku: {Ignar_Kokku} €."
        + f"\nEesmärk krooni miljonär: {EESMARK_1} €."
        + f"\nKrooni miljonär veel minna: {EESMARK_1 - Ignar_Kokku} €."
        + f"\nEesmärk 35 aastaselt portfelli väärtus: {EESMARK_2} €."
        + f"\nVeel minna: {EESMARK_2 - Ignar_Kokku} €."
        + f"\nMörr-i aktsiad: {Morr.m_aktsiad} €."
        + f"\nMörr-i vaba raha: {Morr.MORR_RAHA} €."
        + f"\nMörr-i portfell kokku: {Morr_kokku} €. "
        f"\nKelly portfell: {Kelly_kokku} €. "
        + f"\nPere portfell kokku: {Pere} €."
        + "\n\n"
        + f"\nLaenu Vilde 90-193 makstud: {dateVilde90.years} Years, {dateVilde90.months} Months"
        + f"\n\nK{Kinnisvara.Korter3_Nimi} laenu jääk {BalanceVilde90} €. Laenu summa {Kinnisvara.Korter3_Laen}"
    )

    SYNOLOGY_PATH = r"Projects\My_Send_Email\synology_pass"
    # if it is friday and password file is in directory, then send e-mail'
    if os.path.isfile(what_path_for_file() + SYNOLOGY_PATH):
        no_file = f"E-maili saatmine: Parooli faili ei ole kataloogis: {what_path_for_file()}"
        no_file = fg("red") + no_file + attr("reset")
    elif date.today().weekday() == 4:
        # Variables are: STMP, username, password file, send from, send to, email title and email body'
        send_email(
            stmp_variable="valme.noip.me",  # '192.168.50.235',
            user="email",
            password_file=what_path_for_file() + SYNOLOGY_PATH,
            sent_from="email@valme.noip.me",
            sent_to="val-capital@googlegroups.com",
            sent_subject="Portfelli seis: " + time.strftime("%d-%m-%Y"),
            sent_body=mail_body,
        )
    else:
        print(f"{fg('green')}E-maili saatmine: Pole reede {attr('reset')}")
    print(f"Program Star_Time: {start_date} and End_time: {datetime.datetime.now()}")
    print(f"Program took: {round(time.time() - start_time)} seconds to run")
