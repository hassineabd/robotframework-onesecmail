*** settings ***
Library    OneSecMail
Library    Collections

*** test cases ***
Get Messages With Valid Mailbox
    OneSecMail.Register Email    4uu0c1@dpptd.com
    ${mailboxes}=    Get Emails Summary
    Log    ${mailboxes}
    ${email_id}=    Get Email Id Matching Field    subject    test 5
    Log    ${email_id}
    ${message}=    OneSecMail.Read Email    ${email_id}
    Log    ${message}
    # ${attachment}=    Download Attachment    4uu0c1@dpptd.com    ${email_id}    sd.py
    # Log    ${attachment}
    # ${message}=    Get From List    ${mailboxes}    0
    # Log    ${message}