*** Settings ***
Library    OneSecMail
Library    Collections
*** Variables ***
${email_subject}    Manual Test Subject
${email_body}    Manual Test Body

##
${email}    n34ty4xp@rteet.com
*** Test Cases ***
Wait For Inbox With Manually Sent Email
    [Documentation]    1) Generate an email address.  
    ...               2) Prompt or instruct the user/test environment to send a manual email to that address.  
    ...               3) Verify we can see the new email in the inbox.  

    Register Email    ${email}
    Log To Console    "Send a manual email to: ${email}"
    Sleep    10
    ${inbox}=    Get Inbox Summary
    Should Not Be Empty    ${inbox}
    ${matching_email}=    Wait For Inbox    field=subject    expected_value=${email_subject}    timeout=10    interval=5
    Should Contain    ${matching_email['subject']}    ${email_subject}
    Should Contain    ${matching_email['from']}       @   # Checking basic presence of '@' in the sender address
    Log    "Manually-sent email was successfully retrieved."

Check Inbox After Manual Email (Using Get Inbox Summary)
    [Documentation]    Example to manually verify that at least one new email arrives in the inbox.
    Register Email    ${email}
    Log To Console    "Send a manual email to: ${email}"
    Sleep    10

    ${inbox}=    Get Inbox Summary
    Should Not Be Empty    ${inbox}
    Log    "Inbox summary after manual email: ${inbox}"

    ${email_id}=    Get Email Id Matching Field    subject    ${email_subject}
    Log    "Email ID: ${email_id}"

    ${message}=    Read Email    ${email_id}
    Log    "Message: ${message}"
    Should Contain    ${message['subject']}    ${email_subject}
    Should Contain    ${message['body']}    ${email_body}
    