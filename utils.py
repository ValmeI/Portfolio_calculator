import shutil
from Functions import what_path_for_file
from colored import attr, fg
import os
import time
from datetime import date, datetime
import mail


def get_data_copy_paths_based_on_os() -> tuple:
    BASE_PATH = "Portfolio_calculator"
    BASE_PATH = what_path_for_file()

    # Define paths using os.path.join for cross-platform compatibility
    TXT_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator", "Print_result.txt")
    EXCEL_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator", "Portfell.xlsx")
    PC_DES_PATH = os.path.join(BASE_PATH, "Calculators", "portfolio_result")

    if os.name == "nt":  # Windows
        NAS_PATH = r"\\RMI_NAS\Python\Calculators\portfolio_result"
    elif os.name == "posix":  # macOS or Linux
        NAS_PATH = "/Volumes/Python/Calculators/portfolio_result"

    return TXT_SOURCE, EXCEL_SOURCE, PC_DES_PATH, NAS_PATH


def copy_files_to_nas(TXT_SOURCE: str, EXCEL_SOURCE: str, NAS_DES_PATH: str) -> None:
    # Copy txt result and excel file to NAS server, if all the files or path exists'
    if os.path.isfile(TXT_SOURCE) and os.path.isfile(EXCEL_SOURCE) and os.path.isdir(NAS_DES_PATH):
        # Copy previously created file to Calculators directory'
        shutil.copy(TXT_SOURCE, NAS_DES_PATH)
        shutil.copy(EXCEL_SOURCE, NAS_DES_PATH)
        print(f"Successfully copied at {datetime.now()} to {NAS_DES_PATH}")
    else:
        print(f"Could not copy at {datetime.now()} to {NAS_DES_PATH}")


def generate_mail_body(
    portfolio_goal_no_1: float,
    portfolio_goal_no_2: float,
    kelly_total_portfolio: float,
    family_total_portfolio: float,
    ignar_total_portfolio: float,
    morr_stocks: float,
    morr_free_cash: float,
    morr_total_portfolio: float,
    vilde_apartment: date,
    real_estate: float,
    vilde_balance: float,
) -> str:

    # for combining results to send in e-mail
    mail_body = (
        f"\nTerve portfell kokku: {ignar_total_portfolio} €."
        + f"\nEesmärk krooni miljonär: {portfolio_goal_no_1} €."
        + f"\nKrooni miljonär veel minna: {portfolio_goal_no_1 - ignar_total_portfolio} €."
        + f"\nEesmärk 35 aastaselt portfelli väärtus: {portfolio_goal_no_1} €."
        + f"\nVeel minna: {portfolio_goal_no_2 - ignar_total_portfolio} €."
        + f"\nMörr-i aktsiad: {morr_stocks} €."
        + f"\nMörr-i vaba raha: {morr_free_cash} €."
        + f"\nMörr-i portfell kokku: {morr_total_portfolio} €. "
        f"\nKelly portfell: {kelly_total_portfolio} €. "
        + f"\nPere portfell kokku: {family_total_portfolio} €."
        + "\n\n"
        + f"\nLaenu Vilde 90-193 makstud: {vilde_apartment.years} Years, {vilde_apartment.months} Months"
        + f"\n\nK{real_estate.Korter3_Nimi} laenu jääk {vilde_balance} €. Laenu summa {real_estate.Korter3_Laen}"
    )
    return mail_body


def check_if_and_send_email(mail_body: str, day_to_send_email: str, send_every_day: bool = False) -> None:

    SYNOLOGY_PATH = r"Projects/My_Send_Email/synology_pass"
    password_file_path = what_path_for_file() + SYNOLOGY_PATH

    if os.path.isfile(what_path_for_file() + SYNOLOGY_PATH):
        no_file = f"E-maili saatmine: Parooli faili ei ole kataloogis: {what_path_for_file()}"
        no_file = fg("red") + no_file + attr("reset")
        return
    if date.today().strftime("%A") == day_to_send_email or send_every_day is True:
        # Variables are: STMP, username, password file, send from, send to, email title and email body'
        try:
            mail.send_email(
                stmp_variable="valme.noip.me",  # '192.168.50.235',
                user="email",
                password_file=password_file_path,
                sent_from="email@valme.noip.me",
                sent_to="val-capital@googlegroups.com",
                sent_subject=f"Portfelli seis: {time.strftime('%d-%m-%Y')}",
                sent_body=mail_body,
            )
            print(f"{fg('green')}E-maili saatmine: E-mail saadetud!{attr('reset')}")
        except Exception as e:
            print(f"{fg('red')}E-maili saatmine ebaõnnestus: {e}{attr('reset')}")
    else:
        print(f"{fg('green')}E-maili saatmine: Pole {day_to_send_email}{attr('reset')}")
