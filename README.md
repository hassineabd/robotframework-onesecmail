# robotframework-onesecmail

## Overview

This a `robotframework` library that provides a set of keywords for interacting with the [OneSecMail API](https://onesecmail.com/api-documentation), which allows you to generate temporary email addresses and manage emails received at those addresses.

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
- Generate disposable email addresses
- Check for new messages
- Read message content
- Wait for specific emails with filters
- Context managers for temporary email handling
- Logging and error handling
- Support for multiple domains
