*** Settings ***
Library    OneSecMail

*** Variables ***
${DEFAULT_LANGUAGE}    unknown

*** Test Cases ***
Test Detect Language Valid
    [Documentation]    Test language detection for valid input.
    ${detected_language}=    Detect Language    Bonjour, comment ça va?
    Should Be Equal    ${detected_language}    fr

Test Detect Language Invalid
    [Documentation]    Test language detection for invalid input.
    ${detected_language}=    Detect Language    ${EMPTY}
    Should Be Equal    ${detected_language}    ${DEFAULT_LANGUAGE}

Test Assert Language Is Valid
    [Documentation]    Test assertion for expected language.
    Assert Language Is    Hello, how are you?    english

Test Assert Language Is Invalid
    [Documentation]    Test assertion for unsupported expected language.
    Run Keyword And Expect Error    SystemError    Assert Language Is    Hola, ¿cómo estás?    unsupported_language

Test Assert Language Is Mismatch
    [Documentation]    Test assertion for language mismatch.
    Run Keyword And Expect Error    AssertionError    Assert Language Is    Bonjour, comment ça va?    english