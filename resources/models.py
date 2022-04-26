from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
import enum 
from datetime import datetime
from sqlalchemy_utils import  ChoiceType
from flask_api import FlaskAPI

app = FlaskAPI(__name__)
# app = Flask(__name__)
from sqlalchemy.engine import URL

connection_url = URL.create(
    "mssql+pyodbc",
    # username="scott",
    # password="tiger",
    host="VISHWAJIT\SQLEXPRESS",
    database="daskha",
    query={
        "driver": "ODBC Driver 17 for SQL Server",
    },
)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_url

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Bill(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    meter=db.Column(db.String(150),nullable=False)
    field=db.Column(db.String(150),nullable=False)

class raw_tags_definition(db.Model):
    __tablename__ = "raw_tags_definition"

    id=db.Column(db.Integer,primary_key=True)
    parameter = db.Column(db.String(250))
    equipment_id = db.Column(db.String(250))
    LIVE_MEASUREMENT =db.Column(db.String(250))
    measurement_device = db.Column(db.String(250))
    channel_type = db.Column(db.String(250))
    parameter_name = db.Column(db.String(250),nullable=True)
    aggregateds=db.relationship('aggregated_tags',backref='raw_tags_definition')
    tag=db.relationship('Tag_Master',backref='raw_tags_definition')
    # calculateds=db.relationship('calculated_channels',backref='raw_tags_definitions')
    
    


class aggregation_window(db.Model):
    CHOICES_WINDOW=[
        (u's',u'Second'),
        (u'm',u'Minute'),
        (u'h',u'Hour'),
        (u'd', u'Day'),
        (u'w', u'Week'),
        (u'r',u'Raw')
    ]
    __tablename__ = "aggregation_window"
    
    
    id=db.Column(db.Integer,primary_key=True)
    window_type =db.Column(ChoiceType(CHOICES_WINDOW),nullable=False)
    window_title = db.Column(db.String(150))
    window = db.Column(db.Integer())
    aggregateds=db.relationship('aggregated_tags',backref='aggregation_window')
    dash=db.relationship('dashboard',backref='aggregation_window')
    formula=db.relationship('formula_list',backref='aggregation_window')


    
class aggregation_function(db.Model):
    CHOICES_FUNCTION=[
    (u'mean',u'Mean'),
    (u'sum',u'Sum'),
    (u'max', u'Maximum'),
    (u'min',u'Min'),
    (u'first',u'First'),
    (u'last',u'Last')
    ]
    __tablename__ = "aggregation_function"
    id=db.Column(db.Integer,primary_key=True)
    function_name = db.Column(ChoiceType(CHOICES_FUNCTION),nullable=False)
    function_title = db.Column(db.String(150))
    aggregateds=db.relationship('aggregated_tags',backref='aggregation_function')
    dash=db.relationship('dashboard',backref='aggregation_function')
    
    
class aggregated_tags(db.Model):
    __tablename__ = "aggregated_tags"
    id=db.Column(db.Integer,primary_key=True)
    raw_tags = db.Column(db.Integer, db.ForeignKey('raw_tags_definition.id'))
    aggregated_function =db.Column(db.Integer, db.ForeignKey('aggregation_function.id'))
    aggregated_tags_name = db.Column(db.String(100))
    aggregation_win_value =db.Column(db.Integer())
    aggregation_win_type = db.Column(db.Integer, db.ForeignKey('aggregation_window.id'))
    channel_aggregate = db.relationship('Aggregated_Channel', backref='aggregated_tags')
    tag=db.relationship('Tag_Master',backref='aggregated_tags')

    # def __repr__(self):
    #     return self.aggregated_tags_name
   
''''class calculated_channels(db.Model):
    
    Choice_Formula = [
        (u'1', u'Engine Manual Idle (X)'),
        (u'2', u'Engine Manual-running (Y)'),
        (u'3',u'Puma Monitor (Z)'),
        (u'4',u'Forth'),
        (u'5',u'Fifth')

    ]
    choice_condition=[
        (u'1',u'IF')
    ]
    
    __tablename__ = "calculated_channels"
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    formula_id = db.Column(ChoiceType(choice_condition),nullable=False)
    calculated_field = db.Column(db.String(100))
    tag1_id = db.Column(db.Integer, db.ForeignKey('raw_tags_definition.id'))
    tag1_id_title = db.Column(db.String(150))
    condition_id_1 = db.Integer()
    value_1 = db.Column(db.Integer())
    tag2_id = db.Column(db.Integer, db.ForeignKey('raw_tags_definition.id'))
    tag2_id_title = db.Column(db.String(150), nullable=True)
    condition_id_2 = db.Column(db.Integer())
    value_2 = db.Column(db.Integer())
    tag3_id = db.Column(db.Integer, db.ForeignKey('raw_tags_definition.id'))
    tag3_id_title = db.Column(db.String(150), nullable=True)
    condition_id_3 = db.Column(db.Integer())
    value_3 = db.Column(db.Integer())
    true_value = db.Column(db.Integer())
    false_value = db.Column(db.Integer())
    tag1=db.relationship('raw_tags_definition',foreign_keys='calculated_channels.tag1_id')
    tag2=db.relationship('raw_tags_definition',foreign_keys='calculated_channels.tag2_id')
    tag3=db.relationship('raw_tags_definition',foreign_keys='calculated_channels.tag3_id')'''

class dashboard(db.Model):
    CHOICES_Graph = [
        (u'1', u'First'),
        (u'2', u'Second'),
        (u'3', u'Third'),
        (u'4', u'Forth'),
        (u'5', u'Fifth'),
        (u'6', u'sixth'), 
        (u'7', u'seventh'),
        (u'8', u'eighth')
    ]
    CHOICES_DURATION = (
        (u's', u'Second'),
        (u'm', u'Minute'),
        (u'h', u'Hour'),
        (u'd', u'Day'),
        (u'w', u'Week'),
    )
    __tablename__ = "dashboard"
    id=db.Column(db.Integer,primary_key=True)
    graph_type = db.Column(ChoiceType(CHOICES_Graph),nullable=False)
    tag_id_aggregation_function =db.Column(db.Integer, db.ForeignKey('aggregation_function.id'))
    tag_id_aggregation_window =db.Column(db.Integer, db.ForeignKey('aggregation_window.id'))
    # tag_id_calculated_channels =db.Column(db.Integer, db.ForeignKey('calculated_Channels.id'))
    duration = db.Column(db.Integer())
    duration_choices = db.Column(ChoiceType(CHOICES_DURATION),nullable=False)

class Aggregated_Channel(db.Model):
    __tablename__ = "Aggregated_Channel"
    id=db.Column(db.Integer,primary_key=True)
    aggregated_tags_id = db.Column(db.Integer, db.ForeignKey('aggregated_tags.id'))
    value = db.Column(db.String(150))
    tm = db.Column(db.String(150))
    ts = db.Column(db.DateTime, default=datetime.now)

class Calculated_Channel_ms(db.Model):
    __tablename__ = 'Calculated_Channel_ms'
    id=db.Column(db.Integer,primary_key=True)
    # name = db.relationship('calculated_channel', backref='calculated_channel_mss')
    value = db.Column(db.Float())
    ts = db.Column(db.DateTime, default=datetime.utcnow)
   
class calculation_formula(db.Model):
    CHOICES_FORMULA =[
        (u'if', u'IF'),
        (u'total',u'Total'),
        (u'sum',u'Sum'),
        (u'mean',u'Mean'),
        (u'average',u'Average')
    ]
    __tablename__ = 'calculation_formula'
    id=db.Column(db.Integer,primary_key=True)
    formula_name = db.Column(ChoiceType(CHOICES_FORMULA),nullable=False)
    formula_title = db.Column(db.String(150))
class calculation_condition(db.Model):
    CHOICES_condition = [
        (u'1', u'<'),
        (u'2', u'>'),
        (u'3', u'<='),
        (u'4', u'>='),
        (u'5', u'==')
    ]

    __tablename__ = "calculation_condition"  
    id=db.Column(db.Integer,primary_key=True)
    condition_name = db.Column(ChoiceType(CHOICES_condition),nullable=False)
    condition_title = db.Column(db.String(150))

class saad(db.Model):
    __tablename__ = "saad"
    id=db.Column(db.Integer,primary_key=True)
    a = db.Column(db.String(1200))
    b = db.Column(db.String(1200))
    c = db.Column(db.String(1200))

class formula_type(db.Model):
    __tablename__ = "formula_type"
    id=db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(150))
    formula=db.relationship('formula_list',backref='formula_type')

class formula_list(db.Model):
    __tablename__ = "formula_list"
    id=db.Column(db.Integer,primary_key=True)
    formula_type_id = db.Column(db.Integer, db.ForeignKey('formula_type.id'))
    Formula_id = db.Column(db.String(150))
    Name = db.Column(db.String(150))
    aggregation_win_type = db.Column(db.Integer, db.ForeignKey('aggregation_window.id'))
    tag=db.relationship('Tag_Master',backref='formula_list')

class IF(db.Model):
    __tablename__ = "IF"
    id=db.Column(db.Integer,primary_key=True)
    condition_list = db.Column(db.String(150))
    condition_comparison_list = db.Column(db.String(1200))
    true_value = db.Column(db.Float())
    false_value =db.Column(db.Float())

class Sum(db.Model):
    __tablename__ = "Sum"
    id=db.Column(db.Integer,primary_key=True)
    tag_list = db.Column(db.String(150))

class Average(db.Model):
    __tablename__ = "Average"
    id=db.Column(db.Integer,primary_key=True)
    tag_list = db.Column(db.String(150))

class Total(db.Model):
    __tablename__ = "Total"
    id=db.Column(db.Integer,primary_key=True)
    tag_list = db.Column(db.String(150))

class Mean(db.Model):
    __tablename__ = "Mean"
    id=db.Column(db.Integer,primary_key=True)
    tag_list = db.Column(db.String(150))
class DashboardHome(db.Model):
    __tablename__ = "DashboardHome"
    id=db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(150))
    Tag_list = db.Column(db.String(150))
    Chart_type = db.Column(db.String(150))
    # Duration = models.CharField(max_length=150)
    # Duration_type = models.CharField(max_length=150)
    color = db.Column(db.String(1500))
    dashboard = db.Column(db.String(150),nullable=True)  # Not null
    graph_id = db.Column(db.String(150),nullable=True)
    
class Tag_Master(db.Model):
    __tablename__ = "Tag_Master"
    id=db.Column(db.Integer,primary_key=True)
    Raw_id =db.Column(db.Integer, db.ForeignKey('raw_tags_definition.id'))
    Agg_id =db.Column(db.Integer, db.ForeignKey('aggregated_tags.id'))
    Calc_id = db.Column(db.Integer, db.ForeignKey('formula_list.id'))
    unit_of_measurement = db.Column(db.String(250))
    conditions=db.relationship('Condition',backref='Tag_Master')
class Condition(db.Model):
    CHOICES_condition = [
        (u'1', u'<'),
        (u'2', u'>'),
        (u'3', u'<='),
        (u'4', u'>='),
        (u'5', u'=='),
    ]

    __tablename__ = "Condition"  
    id=db.Column(db.Integer,primary_key=True)
    Tag_id = db.Column(db.Integer, db.ForeignKey('Tag_Master.id'))
    operator_id = db.Column(ChoiceType(CHOICES_condition),nullable=False)
    value = db.Column(db.Float())

class ReportHome(db.Model):
    __tablename__ = "ReportHome"
    id=db.Column(db.Integer,primary_key=True)
    Name = db.Column(db.String(150))
    Tag_list = db.Column(db.String(150))
    Chart_type = db.Column(db.String(150))
    color = db.Column(db.String(1500))
    report = db.Column(db.String(250))
    graph_id = db.Column(db.String(250))