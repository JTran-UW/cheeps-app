from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators as valid

class RegisterForm(FlaskForm):
    """
    Registration form for new users
    """
    username = StringField(
        "Username",
        [
            valid.DataRequired(message="Username is a required field."),
            valid.Length(min=4, max=50, message="Username must be between 4 and 50 characters."),
            valid.Regexp(r'[A-Za-z0-9]+', message="Special characters not allowed.")
        ]
    )
    email = StringField(
        "Email",
        [
            valid.DataRequired(message="Email is a required field."),
            valid.Length(min=4, max=100, message="Email must be between 4 and 100 characters."),
            valid.Email(message=("Not a valid email address."))
        ]
    )
    password1 = PasswordField(
        "Password",
        [
            valid.DataRequired(message="Password is a required field."),
            valid.Length(min=4, max=255, message="Length of password must be between 4 and 255 characters."),
            valid.EqualTo("password2", message=("Passwords must match"))
        ]
    )
    password2 = PasswordField("Confirm Password")

class LoginForm(FlaskForm):
    """
    Login form for users
    """
    username = StringField(
        "Username",
        [valid.DataRequired(message="Username is a required field.")]
    )
    password = PasswordField(
        "Password",
        [valid.DataRequired(message="Password is a required field.")]
    )

class PostForm(FlaskForm):
    """
    Form to create new post
    """
    word = StringField(
        "Your word",
        [
            valid.DataRequired(message="You must put input a word."),
            valid.Length(max=50, message="Word must be fewer than 50 characters in length."),
            valid.Regexp(r"^[a-zA-Z]+$", message="You may only use one word, no special characters.") # https://stackoverflow.com/questions/3617797/regex-to-match-only-letters
        ]
    )
