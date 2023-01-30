import datetime
import os
import sys
import time
from datetime import date
import shutil

from dateutil.relativedelta import relativedelta
from termcolor import colored

from My_Send_Email.Send import send_email

import Excel_functions
import Kelly
import Kinnisvara
import Morr
import Valme
import txt_write_move
from Functions import what_path_for_file, diff_months, get_funderbeam_syndicate_listings
from Excel_functions import need_new_excel_file, write_to_excel, column_width, headers, year_to_year_percent
import warnings


if __name__ == '__main__':
    start_time = time.time()
    '# to IGNORE: UserWarning: Cannot parse header or footer so it will be ignored'
    '# warn("""Cannot parse header or footer so it will be ignored""")'
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
    path = what_path_for_file()

    'copy to nas webserver'
    txt_source = path + r'Portfolio_calculator\Print_result.txt'
    excel_source = path + r'Portfolio_calculator\Portfell.xlsx'
    pc_des_path = path + r'Calculators\portfolio_result'
    nas_des_path = r'\\RMI_NAS\Python\Calculators\portfolio_result'

    '# Copy txt result and excel file to NAS server, if all the files or path exists'
    if os.path.isfile(txt_source) and os.path.isfile(excel_source) and os.path.isdir(nas_des_path):
        '# Copy previously created file to Calculators directory'
        shutil.copy(txt_source, nas_des_path)
        shutil.copy(excel_source, nas_des_path)
        print(f"Kopeeritud edukalt {datetime.datetime.now()}")
    else:
        print(f"Ei kopeeritud {datetime.datetime.now()}")
        pass

    '# create file from consol output'
    sys.stdout = txt_write_move.Logger()

    '# Tänane kuupäev arvutamaks, et mitu makset on tehtud juba'
    today = date.today()
    PerMonthAka42 = Kinnisvara.apr_month(Kinnisvara.Korter1_Laen, 3, 15)
    '# Akadeemia 38-20 Müüdud 28.10.2021 Laenujääk 18 800 EUR'
    PerMonthVilde90 = Kinnisvara.apr_month(Kinnisvara.Korter3_Laen, 2.39, 11)

    print(f'\n{Kinnisvara.Korter1_Nimi} laenumakse: {PerMonthAka42} € + kindlustus.')
    print(Kinnisvara.Korter3_Nimi, "laenumakse:", PerMonthVilde90, "€ + kindlustus.\n")

    '# how many years and months each loan is paid already'
    dateAka42 = relativedelta(today, Valme.Vana_Aka42_63_Laen_Kuupäev)
    dateVilde90 = relativedelta(today, Valme.Vilde90_193_Laen_Kuupäev)

    print("Laenu Akadeemia 42-63 makstud:", dateAka42.years, "Years,", dateAka42.months, "Months")
    print("Laenu Vilde 90-193 makstud:", dateVilde90.years, "Years,", dateVilde90.months, "Months\n")

    '#makstud kuude vahe arvutus'
    KuudMakstudAka42 = diff_months(today, Valme.Aka42_63_Laen_Kuupäev)
    KuudMakstudVilde90 = diff_months(today, Valme.Vilde90_193_Laen_Kuupäev)

    '#diffMonths annab natuke erineva tulemuse, kui aastad vs kuud'
    BalanceAka42 = Kinnisvara.apr_balance(Kinnisvara.Korter1_Laen, 5.198, 15, KuudMakstudAka42)
    BalanceVilde90 = Kinnisvara.apr_balance(Kinnisvara.Korter3_Laen, 2.39, 11, KuudMakstudVilde90)

    print(Kinnisvara.Korter1_Nimi, "laenu jääk", BalanceAka42, "€.", 'Laenu summa', Kinnisvara.Korter1_Laen)
    print(Kinnisvara.Korter3_Nimi, "laenu jääk", BalanceVilde90, "€.", 'Laenu summa', Kinnisvara.Korter3_Laen)

    print(f"\nLaenu kohutus kokku(ainult Akadeemia): {BalanceAka42}")
    print(f"Laenu kohutus kokku(Kõik): {BalanceAka42 + BalanceVilde90}")

    '#Kinnisvara kokku. Liidetakse kõik Dics korterite ostu hinnad - balancid ehk palju laenu veel maksta'
    KinnisVaraPort = Kinnisvara.kinnisvara_vaartus() - BalanceAka42 + Morr.Lähtse_Raha / 2

    print("\nHetkel korteri/krundi puhas väärtus kokku:", KinnisVaraPort, "€.")
    print("\nLähtse investeering:", colored(Morr.Lähtse_Raha / 2, 'red'), "€.")

    '# Portfell kokku'
    Ignar_Kokku = Valme.FysIsik + Valme.JurIsik + KinnisVaraPort

    '#Ehk 1 000 000 Eesti krooni'
    Eesmark = round(1000000 / 15.6466)
    Eesmark2 = 500000
    print("Vilde peale makse Isale:", colored(Valme.Uus_vilde_summa, 'red'), "€.")
    print("\n")
    print("Juriidilise isiku väärtus:", Valme.JurIsik, "€.")
    print("Krüpto:", colored(Valme.Jur_Krypto, 'red'), "€.")
    print("Juriidilise isiku aktsiad:", Valme.JurAktsiad, "€.")
    print("Funderbeam Kokku:", colored(Valme.JurFunderBeam, 'red'), "€.")
    print("\n")
    print("Füüsilise isiku aktsia portfell:", Valme.FysIsik, "€.")
    print("Aktsiad/Raha Jur ja Füs isikud kokku:", Valme.FysIsik + Valme.JurIsik, "€.")
    print("Vaba raha Jur/Füs Kokku:", colored(Valme.RahaKokku, 'red'), "€.")
    print("\n")
    print("Terve portfell kokku:", colored(Ignar_Kokku, 'red'), "€.")
    print("Eesmärk krooni miljonär", Eesmark, "€.")
    print("Krooni miljonär veel minna:", Eesmark - Ignar_Kokku, "€.")

    print("Eesmärk 35 aastaselt portfelli väärtus", Eesmark2, "€.")
    print("Veel minna:", colored(Eesmark2 - Ignar_Kokku, 'red'), "€.")

    Morr_kokku = Morr.kokku
    print("Mörr-i aktsiad:", Morr.m_aktsiad, "€.")
    print("Mörr-i vaba raha:", Morr.m_raha, "€.")
    print("Mörr-i portfell kokku:", colored(Morr_kokku, 'red'), "€.")

    '# Kelly Portfell'
    Kelly_kokku = Kelly.Kelly_Portfell_Kokku
    print("Kelly portfell:", colored(Kelly_kokku, 'red'), "€.")

    '# Pere kõik kokku'
    Pere = Ignar_Kokku + Morr_kokku + Kelly_kokku
    print("Pere portfell kokku:", colored(Pere, 'red'), "€.")

    Aktsiad_kokku = Valme.FysIsik + Valme.JurIsik
    # check if new Excel file is needed and if so, create it
    need_new_excel_file(excel_name="Portfell", sheet_name="Porfelli Info", excel_headers=Excel_functions.headers)

    # compare the current portfolio with the previous years
    print("=================Ignar's==========================")
    print(year_to_year_percent(excel_name="Portfell",
                               mm_dd="01-01",
                               todays_total_portfolio=Ignar_Kokku,
                               excel_column_input='F'))
    print("=================Mörr's===========================")
    print(year_to_year_percent(excel_name="Portfell",
                               mm_dd="01-01",
                               todays_total_portfolio=Morr_kokku,
                               excel_column_input='G',
                               filter_nr_input=2000))
    print("=================Kelly's==========================")
    print(year_to_year_percent(excel_name="Portfell",
                               mm_dd="01-01",
                               todays_total_portfolio=Kelly_kokku,
                               excel_column_input='L',
                               filter_nr_input=2))
    print("==================================================")

    # make a list with all the data for Excel file input
    values_list = []
    values_list.extend((str(today), KinnisVaraPort, Valme.FysIsik, Valme.JurIsik, Aktsiad_kokku,
                        Ignar_Kokku, Morr_kokku, Pere, Valme.Uus_vilde_summa,
                        Valme.RahaKokku, Valme.JurFunderBeam, Kelly_kokku))

    '# how_to_add: 1 = append, 2 = overwrite, 3 = compare if change is needed'
    '# compare_column for overwrite: 1 is first column in excel (A) and 2 is B and so on'
    write_to_excel(excel_name="Portfell", list_of_data=values_list, how_to_add=2, compare_column=1)
    column_width(excel_name="Portfell", excel_headers=headers)

    #funderbeam_list = []
    # adds today's date to the beginning of the list
    #funderbeam_list.extend(str(today))
    #funderbeam_list = funderbeam_list + get_funderbeam_syndicate_listings()
    # TODO: check why it doesn't work with the following line. ERROR
    # write_to_excel(excel_name="funderbeam_syndicate_listings",
    #               list_of_data=funderbeam_list, how_to_add=2, compare_column=1)

    # for combining results to send in e-mail
    mail_body = f"\nTerve portfell kokku: {Ignar_Kokku} €." + \
              f"\nEesmärk krooni miljonär: {Eesmark} €." + \
              f"\nKrooni miljonär veel minna: {Eesmark - Ignar_Kokku} €." + \
              f"\nEesmärk 35 aastaselt portfelli väärtus: {Eesmark2} €." + \
              f"\nVeel minna: {Eesmark2 - Ignar_Kokku} €." + \
              f"\nMörr-i aktsiad: {Morr.m_aktsiad} €." + \
              f"\nMörr-i vaba raha:{Morr.m_raha} €." + \
              f"\nMörr-i portfell kokku: {Morr_kokku} €. " \
              f"\nKelly portfell: {Kelly_kokku} €. " + \
              f"\nPere portfell kokku: {Pere} €." + "\n\n" +\
              f"\nLaenu Akadeemia 42-63 makstud: {dateAka42.years} Years, {dateAka42.months} Months" +\
              f"\nLaenu Vilde 90-193 makstud: {dateVilde90.years} Years, {dateVilde90.months} Months" +\
              f"\n\n{Kinnisvara.Korter1_Nimi} laenu jääk {BalanceAka42} €. Laenu summa {Kinnisvara.Korter1_Laen}" +\
              f"\nK{Kinnisvara.Korter3_Nimi} laenu jääk {BalanceVilde90} €. Laenu summa {Kinnisvara.Korter3_Laen}"

    '#if it is friday and password file is in directory, then send e-mail'
    if os.path.isfile(what_path_for_file() + r'Projects\My_Send_Email\synology_pass'):
        no_file = 'E-maili saatmine: Parooli faili ei ole kataloogis: ' + what_path_for_file()
        no_file = colored(no_file, 'red')
    elif date.today().weekday() == 4:
        '# Variables are: STMP, username, password file, send from, send to, email title and email body'
        send_email(stmp_variable='valme.noip.me',  # '192.168.50.235',
                   user='email',
                   password_file=what_path_for_file() + r'Projects\My_Send_Email\synology_pass',
                   sent_from='email@valme.noip.me',
                   sent_to='val-capital@googlegroups.com',
                   sent_subject=f'Portfelli seis: ' + time.strftime('%d-%m-%Y'),
                   sent_body=mail_body)
    else:
        print(colored('E-maili saatmine: Pole reede', 'green'))

    print(f"Program took: {round(time.time() - start_time)} seconds to run")
