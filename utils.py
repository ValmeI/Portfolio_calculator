from Functions import what_path_for_file
from colored import attr, fg
import os
import time
from datetime import date
import mail


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


def check_if_and_send_email(mail_body: str) -> None:
    SYNOLOGY_PATH = r"Projects/My_Send_Email/synology_pass"
    # if it is friday and password file is in directory, then send e-mail'
    if os.path.isfile(what_path_for_file() + SYNOLOGY_PATH):
        no_file = f"E-maili saatmine: Parooli faili ei ole kataloogis: {what_path_for_file()}"
        no_file = fg("red") + no_file + attr("reset")
    elif date.today().weekday() == 4:
        # Variables are: STMP, username, password file, send from, send to, email title and email body'
        mail.send_email(
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
