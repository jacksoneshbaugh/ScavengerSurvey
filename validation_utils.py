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


def validate_password(password):
    """
    Validates a password. Rules: at least 8 characters, at least one number, at least one special character.
    :param password: The password to validate.
    :return: an array of booleans for each rule.
    """
    length = len(password) >= 8
    number = any(char.isdigit() for char in password)
    special = any(char in '!@#$%^&*()-+' for char in password)
    return [length, number, special]