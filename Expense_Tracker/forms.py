from flask_wtf import FlaskForm #importing FlaskForm class from flask_wtf module
from wtforms import StringField,  SubmitField, TextAreaField, SelectField #importing form field types from wtforms
from wtforms.validators import DataRequired 

class EntryForm(FlaskForm): #defines a class called EntryForm which inherits aatributes from FlaskForm
    category=SelectField('Category', choices=[('Miscellaneous', 'Click to Select'), 
    ('Water', 'Water'), ('Electricity', 'Electricity'),('Vacation', 'Vacation'),('Transport', 'Transport'),
    ('Groceries', 'Groceries'),('Clothing and Accessories', 'Clothing and Accessories'),
    ('Health and Fitness','Health and Fitness'),('Medical', 'Medical'),('Gadgets', 'Gadgets'),
    ('Home', 'Home'),('Rent', 'Rent'),('Miscellaneous', 'Miscellaneous'),('Services', 'Services'),
    ('Education','Education'),('Food','Food')]) #drop down field with the above options
    content=TextAreaField('Content',validators=[DataRequired()]) #creates text box that required data to be filled in
    amount=TextAreaField('Amount',validators=[DataRequired()])
    submit=SubmitField('Enter') #creates a button called submit with the name "Enter"