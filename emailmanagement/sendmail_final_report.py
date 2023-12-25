from django.conf import settings
from django.core.mail import send_mail

def sendFinalreport(instance):
    message = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Email Template</title>
            <style>
                @import url("https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");
            </style>
        </head>
        <body>
            <table align="center" cellpadding="0" cellspacing="0" border="0" width="100%" style="max-width: 600px; font-family: Poppins; background: whitesmoke; padding: 20px; border-radius: 6px;">
                <tr>
                    <td align="center" bgcolor="#FFFFFF" style="padding: 20px;">
                        <img src="http://lims.dftqc.gov.np/assets/nepal-government.png" alt="" width="132" style="display: block; margin: 0 auto;">
                        <p style="color: #0B53A7; font-weight: 600; font-size: 18px; margin-top: 20px;">Labrotary Information Management System (LIMS)</p>
                        <p style="text-align: center; font-weight: 400;">Your test for <span style="font-weight: 600;">{instance.name} (Reference Number: {instance.refrence_number})</span> is completed successfully. Please visit DFTQC to collect your report.</p>
                       
                        <p style="text-align: center; margin-top: 20px;">Please visit <a href="http://lims.dftqc.gov.np" style="text-decoration: none; color: #0B53A7; font-weight: 600;">www.lims.dftqc.gov.np</a> for any enquiries.</p>
                        <p style="margin: 0; text-align: center;"><span style="font-weight: 600;">Tel:</span> 977-1-4262369, 4262430, 4240016, 4262739</p>
                        <p style="margin: 0; text-align: center; text-decoration: none;"><span style="font-weight: 600;">Fax:</span> 977-1-4262337 <span style="font-weight: 600; margin-left: 10px;">E-mail:</span> info@dftqc.gov.np</p>
                    </td>
                </tr>
            </table>
        </body>
        </html>"""
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [instance.owner_user]
    plain_message = ""
    subject = f"Test report for {instance.name} (Refrence Number:{instance.refrence_number})"
    send_mail(subject, plain_message, email_from, recipient_list,html_message=message)
    #  <a href="https://pdfmachine.kantipurinfotech.com.np/public/api/show-pdf-report/{instance.id}/1" style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">View Report</a>