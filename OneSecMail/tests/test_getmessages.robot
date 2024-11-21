*** settings ***
Library    OneSecMail

*** test cases ***
Get Messages With Valid Mailbox
    ${mailboxes}=    OneSecMail.Get Messages    	4uu0c1@dpptd.com
    Log    ${mailboxes}

read 
    ${message}=    Read Last Message    4uu0c1@dpptd.com