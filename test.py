import smtplib
import os

EMAIL = os.getenv("uzhavarunavupodi@gmail.com")
PASSWORD = os.getenv("scypyqaawsxlpbro")

print(EMAIL)
print(PASSWORD)

with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
    smtp.login(EMAIL,PASSWORD)
    print("Login Successful")