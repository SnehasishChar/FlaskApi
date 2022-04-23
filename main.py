from flask import Flask 
from flask_restful import Resource, Api,reqparse
from flask_api import FlaskAPI
from resources.views import *


# app = Flask(__name__)

app = FlaskAPI(__name__)
api=Api(app)
parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route('/')
def example():
    return {'hello': 'Hello World !!!'}
    
  
api.add_resource(HelloWorld, '/home')
api.add_resource(RTDViewSet, '/raw')
api.add_resource(Agree_Tag_ViewSet, '/agg')
api.add_resource(Agree_Function_ViewSet, '/fun')
api.add_resource(Agree_Window_ViewSet, '/win')
api.add_resource(Dashboard_ViewSet, '/dash')
api.add_resource(AggregatedChannelViewSet, '/aggchannel')
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
    app.run(debug=True)

   
