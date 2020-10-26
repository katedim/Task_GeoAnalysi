from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired


class CoordsForm(FlaskForm):
    id = HiddenField("id")
    name = StringField('Name', validators=[DataRequired()])
    lot = StringField('Longtitude', validators=[DataRequired()])
    lan = StringField('Latitude', validators=[DataRequired()])
