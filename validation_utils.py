"""
Useful functions for validation of data in the app.
"""
___author___ = "Jackson Eshbaugh"
___version___ = "03/11/2024"


def validate_email(email):
    """
    Validates an email.
    :param email: The email to validate.
    :return: True if the email is valid, False otherwise.
    """
    return '@' in email and '.' in email


def validate_password(password1, password2):
    """
    Validates a password. Rules: at least 8 characters, at least one number, at least one special character,
    and the two passwords must match.
    :param password1: The first password submission to validate.
    :param password2: The second password submission to validate.
    :return: an array of booleans for each rule.
    """
    length = len(password1) >= 8
    number = any(char.isdigit() for char in password1)
    special = any(char in '!@#$%^&*()-+' for char in password1)
    match = password1 == password2
    return [length, number, special, match]


def escape_string(string):
    """
    Escapes a string.
    :param string: The string to escape.
    :return: The escaped string.
    """
    return string.replace("'", "\\'")
