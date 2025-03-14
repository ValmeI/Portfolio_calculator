import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from termcolor import colored
from secrets import token_hex


def send_email(stmp_variable: str, user: str, password_file: str, sent_from: str, sent_to: str, sent_subject: str, sent_body: str) -> None:
    try:
        with open(password_file + ".txt", "r", encoding="utf8") as open_file:
            password = open_file.read().strip()
    except FileNotFoundError:
        print(colored("Password file not found.", "red"))
        return
    except Exception as e:
        print(colored(f"Error reading password file: {e}", "red"))
        return

    try:
        server = smtplib.SMTP_SSL(stmp_variable, 465)
        server.login(user, password)

        msg = EmailMessage()
        msg["From"] = sent_from
        msg["To"] = sent_to
        msg["Subject"] = sent_subject
        msg["Message-ID"] = make_msgid(idstring=token_hex(16))
        msg.set_type("text/html")
        msg.set_content(sent_body)

        server.send_message(msg)
        print(colored("Mail Sent Successfully", "green"))
    except smtplib.SMTPException as smtp_e:
        print(colored(f"Error sending email: {smtp_e}", "red"))
    except Exception as e:
        print(colored(f"Error sending email: {e}", "red"))
    finally:
        server.quit()
