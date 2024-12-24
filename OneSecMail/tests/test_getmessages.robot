*** settings ***
Library    OneSecMail
Library    Collections

*** test cases ***
Get Messages With Valid Mailbox
    ${mailboxes}=    OneSecMail.Get Emails Summary    	4uu0c1@dpptd.com
    Log    ${mailboxes}
    ${email_id}=    OneSecMail.Get Email Id Matching Field    4uu0c1@dpptd.com    subject    test 5
    Log    ${email_id}
    ${message}=    OneSecMail.Read Email    4uu0c1@dpptd.com    ${email_id}
    Log    ${message}
    # ${attachment}=    Download Attachment    4uu0c1@dpptd.com    ${email_id}    sd.py
    # Log    ${attachment}
    # ${message}=    Get From List    ${mailboxes}    0
    # Log    ${message}