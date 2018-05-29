'''
Created on 21 may 2018

@author: daniel.cano
@summary: Books padel at 18h, one week later when executed 
          and sends a confirmation mail
'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import schedule
import time
import datetime as dt

user = "user"
pwd = "pass"

mail = "mail"
mail_pas = "pass"


def get_book_date():
    nx = dt.datetime.today()+dt.timedelta(days=7) # next week day
    return 'date={d:02d}%2F{m:02d}%2F{y}'.format(d=nx.day, m=nx.month, y=nx.year)


def reservar():
    driver = webdriver.Chrome(executable_path='C:\Python27\selenium\chromedriver.exe')
#     driver = webdriver.PhantomJS(executable_path='C:\Python27\selenium\phantomjs.exe')

    driver.get("http://www.lifepadelclub.com/prReserves.tp?idActivitat=1&"+get_book_date())
#     driver.get("http://www.lifepadelclub.com/prReserves.tp?idActivitat=1&date=29%2F05%2F2018")
    elem = driver.find_element_by_name('j_username')
    elem.send_keys(user)
    # sleep(3)
    elem = driver.find_element_by_name('j_password')
    elem.send_keys(pwd)
    elem.send_keys(Keys.RETURN)
    driver.save_screenshot('cuadro_horario.png')
    driver.find_element_by_xpath("//td[@data-horainici='1800']").click()
    elem = driver.find_element_by_css_selector("input[type='radio'][value='true']")
    elem.find_element_by_xpath('..').click()  # click over tag (father)

    # confirma reserva
#     driver.find_element_by_id('confirmarReserva').click()
#     elem = driver.find_element_by_class_name('btn-primary') # OK, confirmar
#     driver.save_screenshot('reserva.png')
#     driver.close()


def task():
    reservar()
    send_mail()


def send_mail():
    sender = "pypadelbooking@gmail.com"
    recipients = ["daniel.cano@doga.es", "dancan.88@gmail.com"]

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Padel sheduled"
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    nx = dt.datetime.today()+dt.timedelta(days=7)  # next week day
    text = "Hi!\ntext {d:02d}-{m:02d}-{y}".format(d=nx.day, m=nx.month, y=nx.year)
    html = """\
    <html>
      <head></head>
      <body>
        <p>Hi!<br>
           You have been selected to play at DOGA master in Abrera
        </p>
      </body>
    </html>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    filename = "reserva.png"

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(filename, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(mail, mail_pas)
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()


if __name__ == '__main__':
    reservar()
#     schedule.every().day.at("00:00").do(task)
#     while True:
#         schedule.run_pending()
#         time.sleep(60)  # wait one minute
    # nohup python2.7 MyScheduledProgram.py &
