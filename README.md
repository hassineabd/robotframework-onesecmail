# robotframework-onesecmail

## Overview

This `robotframework` library leverages the [OneSecMail API](https://onesecmail.com/api-documentation) to provide a comprehensive set of keywords for managing temporary email addresses and their associated emails. It enables the creation of disposable email addresses, monitoring of new messages, reading of message content, and more.

## Installation

```bash
pip install robotframework-onesecmail
```

## Usage

```robot
*** Settings ***
Library    OneSecMail

*** Test Cases ***
```


Features
--------
- **Temporary Email Generation**: Create disposable email addresses for temporary use.
- **New Message Notification**: Check for new messages received at temporary email addresses.
- **Email Content Reading**: Read the content of messages received at temporary email addresses.
- **Filtered Email Waiting**: Wait for specific emails to arrive based on filters.
- **Temporary Email Management**: Utilize context managers for efficient handling of temporary email addresses.
