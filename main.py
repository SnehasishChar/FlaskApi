from flask import Flask 
from flask_restful import Resource, Api
from flask_api import FlaskAPI
from resources.views import *
from resources.models import *

# app = Flask(__name__)

app = FlaskAPI(__name__)
api=Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()

api.add_resource(HelloWorld, '/home')
api.add_resource(RTDViewSet, '/raw')
api.add_resource(RTDViewSet1, '/raw/<int:id>')
api.add_resource(Agree_Tag_ViewSet, '/agg')
api.add_resource(Agree_Tag_ViewSet1, '/agg/<int:id>')
api.add_resource(Agree_Function_ViewSet, '/fun')
api.add_resource(Agree_Function_ViewSet1, '/fun/<int:id>')
api.add_resource(Agree_Window_ViewSet, '/win')
api.add_resource(Agree_Window_ViewSet1, '/win/<int:id>')

api.add_resource(Dashboard_ViewSet, '/dash')
api.add_resource(Dashboard_ViewSet1, '/dash/<int:id>')

api.add_resource(AggregatedChannelViewSet, '/aggchannel')
api.add_resource(AggregatedChannelViewSet1, '/aggchannel/<int:id>')

api.add_resource(CalculatedFormulaViewSet, '/calfor')
api.add_resource(CalculatedConditionViewSet, '/calcon')
api.add_resource(formula_typeViewSet, '/forml')
api.add_resource(formula_listViewSet, '/formula')
api.add_resource(IFViewSet, '/iff')
api.add_resource(ConditionViewSet, '/condition')
api.add_resource(SumViewSet, '/sum')
api.add_resource(MeanViewSet, '/mean')
api.add_resource(TotalViewSet, '/total')
api.add_resource( AverageViewSet, '/avg')






if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True, port='8000')

   
