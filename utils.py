import shutil
from functions import what_path_for_file
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
    BASE_PATH = what_path_for_file() or "Portfolio_calculator/Data"  # Default path
    logger.debug(f"BASE_PATH: {BASE_PATH}")
    

    # Define paths using os.path.join for cross-platform compatibility
    TXT_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator/data", "Print_result.txt")
    EXCEL_SOURCE = os.path.join(BASE_PATH, "Portfolio_calculator/data", "Portfell.xlsx")
    logger.debug(f"TXT_SOURCE: {TXT_SOURCE}, EXCEL_SOURCE: {EXCEL_SOURCE}")

    if os.name == "nt":  # Windows
        NAS_PATH = r"\\RMI_NAS\Python\Calculators\portfolio_result"
    elif os.name == "posix":  # macOS or Linux
        if platform.system() == "Darwin":  # macOS
            NAS_PATH = "/Volumes/Python/Calculators/portfolio_result"
        elif platform.system() == "Linux":  # Linux
            NAS_PATH = "/mnt/RMI_NAS/Python/Calculators/portfolio_result"
        else:
            NAS_PATH = "/Volumes/Python/Calculators/portfolio_result"  # Default fallback
    else:
        NAS_PATH = "Not found"
    return TXT_SOURCE, EXCEL_SOURCE, NAS_PATH

def check_data_paths(txt_source: str = None, excel_source: str = None, nas_path: str = None) -> bool:
    can_access_txt = os.path.exists(txt_source) if txt_source is not None else False
    can_access_excel = os.path.exists(excel_source) if excel_source is not None else False
    can_access_nas = os.path.exists(nas_path) if nas_path is not None else False
    logger.debug(f"can_access_txt: {can_access_txt}, can_access_excel: {can_access_excel}, can_access_nas: {can_access_nas}")
    return can_access_txt and can_access_excel and can_access_nas


def copy_file_to_nas(source_file: str, destination_path: str) -> None:
    if not check_data_paths(txt_source=source_file, nas_path=destination_path):
        logger.error(f"Failed to copy {source_file} to {destination_path} - source file or destination path not found")
        return
        
    # Check if the source file exists and the destination directory exists
    source_file_check = os.path.join(source_file) # TODO: have to redo some of this as there is probabaly duplicate code
    destination_path_check = os.path.join(destination_path)
    
    if source_file_check and destination_path_check:
        if platform.system() in ["Linux", "Darwin"]:  # Darwin is macOS
            try:
                # Use rsync to copy the file to the NAS destination path
                result = subprocess.run(["rsync", "-av", source_file, destination_path], capture_output=True, text=True, check=True)
                if result.returncode == 0:
                    print(f'Successfully copied "{source_file}" to "{destination_path}" using rsync.')
                else:
                    logger.warning(f"Failed to copy {source_file} at {datetime.now()} to {destination_path} using rsync: {result.stderr}")
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
        logger.warning(f"Could not copy at {datetime.now()} to {destination_path} - source file path found: '{source_file_check}' and destination path found: '{destination_path_check}'")


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
        sg = SendGridAPIClient(config.TWILIO_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:
            print(f"\n {fg('green')}{attr('bold')}Email sent{attr('reset')}")
        else:
            print(f"\n {fg('red')}{attr('bold')}Email NOT SENT{attr('reset')}, response: {response.body}")
    except Exception as e:
        print(str(e))


def get_default_user_agent() -> str:
    os_type = platform.system().lower()
    machine_type = platform.machine().lower()

    if os_type == "linux":
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"

    elif os_type == "darwin":  # macOS
        if machine_type == "arm64":
            return "Mozilla/5.0 (Macintosh; Apple Silicon Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        else:
            return "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"

    elif os_type == "windows":
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"

    else:
        # Default fallback to Linux if OS is unidentified
        return "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"


if __name__ == "__main__":
    TXT_SOURCE, EXCEL_SOURCE, NAS_DES_PATH = get_data_copy_paths_based_on_os()
    copy_file_to_nas(TXT_SOURCE, NAS_DES_PATH)