*** settings ***
Library    OneSecMail
Library    Collections

*** test cases ***
Get Messages With Valid Mailbox
    ${mailboxes}=    OneSecMail.Get Emails    	4uu0c1@dpptd.com
    Log    ${mailboxes}
    ${message}=    Get From List    ${mailboxes}    0
    Log    ${message}

read 
    ${message}=    OneSecMail.Read Email    4uu0c1@dpptd.com    1103535846
    Log    message
