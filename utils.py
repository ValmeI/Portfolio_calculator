import shutil
from Functions import what_path_for_file
from colored import fg, attr
import os
import time
from datetime import date, datetime
from app_logging import logger
import subprocess
import platform
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import config


def get_data_copy_paths_based_on_os() -> tuple:
    BASE_PATH = "Portfolio_calculator"
    BASE_PATH = what_path_for_file()

    # Define paths using os.path.join for cross-platform compatibility
    TXT_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator", "Print_result.txt")
    EXCEL_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator", "Portfell.xlsx")

    if os.name == "nt":  # Windows
        NAS_PATH = r"\\RMI_NAS\Python\Calculators\portfolio_result"
    elif os.name == "posix":  # macOS or Linux
        NAS_PATH = "/Volumes/Python/Calculators/portfolio_result"
    logger.debug(f"TXT_SOURCE: {TXT_SOURCE}, EXCEL_SOURCE: {EXCEL_SOURCE}, NAS_PATH: {NAS_PATH}")
    return TXT_SOURCE, EXCEL_SOURCE, NAS_PATH


def copy_file_to_nas(source_file: str, destination_path: str) -> None:
    # Check if the source file exists and the destination directory exists
    if os.path.isfile(source_file) and os.path.isdir(destination_path):
        if platform.system() in ["Linux", "Darwin"]:  # Darwin is macOS
            try:
                # Use rsync to copy the file to the NAS destination path
                result = subprocess.run(
                    ["rsync", "-av", source_file, destination_path], capture_output=True, text=True, check=True
                )
                if result.returncode == 0:
                    print(f'Successfully copied "{source_file}" to "{destination_path}" using rsync.')
                else:
                    logger.warning(
                        f"Failed to copy {source_file} at {datetime.now()} to {destination_path} using rsync: {result.stderr}"
                    )
            except Exception as e:
                logger.error(f"An error occurred while copying {source_file} to NAS using rsync: {e}")

        elif platform.system() == "Windows":
            try:
                shutil.copy(source_file, destination_path)
                print(f'Successfully copied "{source_file}" to "{destination_path}" using shutil.')
            except Exception as e:
                logger.error(f"An error occurred while copying {source_file} to NAS using shutil: {e}")
        else:
            logger.error(f"Unsupported OS: {platform.system()}")
    else:
        logger.warning(
            f"Could not copy at {datetime.now()} to {destination_path} - source file or destination directory missing."
        )


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

    if date.today().strftime("%A") == day_to_send_email or send_every_day is True:
        try:
            twilio_send_email(
                sent_from="ignarvalme@gmail.com",
                sent_to="ignarvalme@gmail.com",
                sent_subject=f"Portfelli seis: {time.strftime('%d-%m-%Y')}",
                sent_body=mail_body,
            )
            print(f"{fg('green')}E-maili saatmine: E-mail saadetud!{attr('reset')}")
        except Exception as e:
            logger.warning(f"{fg('red')}E-maili saatmine ebaõnnestus: {e}{attr('reset')}")
    else:
        print(f"{fg('green')}E-maili saatmine: Pole {day_to_send_email}{attr('reset')}")


def twilio_send_email(sent_from: str, sent_to: str, sent_subject: str, sent_body: str) -> None:

    message = Mail(from_email=sent_from, to_emails=sent_to, subject=sent_subject, html_content=sent_body)
    try:
        sg = SendGridAPIClient(config.twilio_apy_key)
        response = sg.send(message)
        if response.status_code == 202:
            print(f"\n {fg('green')}{attr('bold')}Email sent{attr('reset')}")
        else:
            print(f"\n {fg('red')}{attr('bold')}Email NOT SENT{attr('reset')}, response: {response.body}")
    except Exception as e:
        print(str(e))
