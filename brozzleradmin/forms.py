from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class NewCrawlRequestForm(FlaskForm):
    crawl_request_name = StringField('crawl_request_name', validators=[DataRequired()])


class NewJobForm(FlaskForm):
    job_template_choices = [('1', 'Single Page Crawl'), ('2', 'Domain Crawl'), ('3', 'Twitter Crawl'),
                            ('4', '1 HOP Day Crawl'), ('5','1 HOP OFF Crawl')]
    job_template_config = SelectMultipleField('job_template', choices=job_template_choices, validators=[DataRequired()])
    job_name = StringField('job_name', validators=[DataRequired()])
    job_warc_prefix = StringField('job_warc_prefix', validators=[DataRequired()])
    job_seeds = StringField('job_seeds', widget=TextArea(), validators=[DataRequired()])


class NewCustomJobForm(FlaskForm):
    job_name = StringField('job_name', validators=[DataRequired()])
    job_config = StringField('job_config', widget=TextArea(), validators=[DataRequired()])
    job_warc_prefix = StringField('job_warc_prefix', validators=[DataRequired()])


class NewScheduleJobForm(FlaskForm):
    job_name = StringField('job_name', validators=[DataRequired()])
    job_config = StringField('job_config', widget=TextArea(), validators=[DataRequired()])
    job_schedule = StringField('job_schedule', validators=[DataRequired()])
    job_hour = StringField('job_hour', validators=[DataRequired()])
    job_minutes = StringField('job_minute', validators=[DataRequired()])
    job_recurring = BooleanField('job_recurring')
