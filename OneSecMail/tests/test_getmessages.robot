*** settings ***
Library    OneSecMail

*** test cases ***
Get Messages With Valid Mailbox
    ${mailboxes}=    OneSecMail.Get Messages    2a3i01httw7w    dpptd.com
    Log    ${mailboxes}