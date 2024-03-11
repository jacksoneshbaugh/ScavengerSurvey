"""
User model.
"""
___author___ = "Jackson Eshbaugh"
___version___ = "03/11/2024"

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app import login_manager, db


class User(db.Model):
    """
    User model.

    :param id: The user's id.
    :param name: The user's name.
    :param email: The user's email.
    :param password: The user's password. Will be hashed.
    :param authenticated: Whether the user is authenticated.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    authenticated: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def isAuthenticated(self):
        """
        Checks if the user is authenticated.
        :return: True if the user is authenticated, False otherwise.
        """
        return self.authenticated

    def get_id(self):
        """
        Gets the user's id.
        :return: The user's id.
        """
        return self.id

    def is_active(self):
        """
        All users are active.
        :return: True
        """
        return True

    def is_anonymous(self):
        """
        Anonymous users are not supported.
        :return: False
        """
        return False


pass


@login_manager.user_loader
def user_loader(user_id):
    """
    Given a *user_id*, return the associated User object.
    :return: The User object.
    """
    return User.query.get(user_id)


@login_manager.request_loader
def request_loader(request):
    """
    Given a *request*, return a User object or None.
    :return: The User object or None.
    """
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    return user if user else None
