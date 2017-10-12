from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class NewCollectionForm(FlaskForm):
    collection_name = StringField('collection_name', validators=[DataRequired()])
    collection_prefix = StringField('collection_prefix', validators=[DataRequired()])


class NewJobForm(FlaskForm):
    job_name = StringField('job_name', validators=[DataRequired()])
    job_config = StringField('job_config', widget=TextArea(), validators=[DataRequired()])


class NewScheduleJobForm(FlaskForm):
    job_name = StringField('job_name', validators=[DataRequired()])
    job_config = StringField('job_config', widget=TextArea(), validators=[DataRequired()])
    job_schedule = StringField('job_schedule', validators=[DataRequired()])
    job_hour = StringField('job_hour', validators=[DataRequired()])
    job_minutes = StringField('job_minute', validators=[DataRequired()])
