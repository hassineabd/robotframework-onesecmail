*** settings ***
Library    OneSecMail
Library    Collections

*** Variables ***
${email_regex_pattern}=    ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

*** keywords ***
Generate Random Mailbox Keyword
    [Arguments]    ${count}=${EMPTY}
    ${generated_mailbox}=    OneSecMail.Generate Temporary Mailbox    ${count}
    Set Test Message    ${generated_mailbox}
    RETURN    ${generated_mailbox}

*** test cases ***
Generate Single Random Mailbox Default Count
    Run Keyword And Expect Error   ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword
    
Generate Single Random Mailbox With Zero Count
    Run Keyword And Expect Error   ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    0

Generate Single Random Mailbox With Count One
    ${generated_mailbox}=    Generate Random Mailbox Keyword    1
    Should Match Regexp    ${generated_mailbox}[0]    ${email_regex_pattern}

Generate Multiple Random Mailboxes With Count Five
    ${generated_mailbox}=    Generate Random Mailbox Keyword    5
    # Should Be String    ${generated_mailbox}
    ${second_email}=    Get From List     ${generated_mailbox}    2
    Count Values In List    ${generated_mailbox}    5
    
Generate Random Mailbox With Invalid String Input
    Run Keyword And Expect Error   ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    hassineabd

Generate Single Random Mailbox With Negative Count
    Run Keyword And Expect Error   ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    -1

Generate Single Random Mailbox With Large Count
    ${generated_mailbox}=    Generate Random Mailbox Keyword    10
    Count Values In List    ${generated_mailbox}    10

Generate Random Mailbox With Special Characters
    Run Keyword And Expect Error    ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    !@#$%^&*

Generate Random Mailbox With Null Input
    Run Keyword And Expect Error    ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    ${None}

Generate Random Mailbox With Float Count
    Run Keyword And Expect Error    ValueError: Count must be a positive integer.    Generate Random Mailbox Keyword    2.5