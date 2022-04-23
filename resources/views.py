from flask import Flask,request, jsonify
from flask_restful import Resource, Api,reqparse
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import  ChoiceType
from .models import *
from .serializers import *
from flask_marshmallow import Marshmallow
parser = reqparse.RequestParser()

app = FlaskAPI(__name__)
# app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma=Marshmallow(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class RTDViewSet(Resource):
    def get(self):
        one_user=raw_tags_definition.query.all()
        rtdschema=rtdSerializer(many=True)
        output=rtdschema.dump(one_user)
        return jsonify({'raw_tags':output})

class Agree_Tag_ViewSet(Resource):
    def get(self):
        tags=aggregated_tags.query.all()
        aggtag=aggregated_tagsSerializer(many=True)
        res=aggtag.dump(tags)
        return jsonify({'agg_tags':res})


class Agree_Function_ViewSet(Resource):
    def get(self):
        fun=aggregation_function.query.all()
        aggfun=aggregation_functionSerializer(many=True)
        res=aggfun.dump(fun)
        return jsonify({'agg_fun':res})

class Agree_Window_ViewSet(Resource):
    def get(self):
        w=aggregation_window.query.all()
        aw=aggregated_windowSerializer(many=True)
        res=aw.dump(w)
        return jsonify({'agg_win':res})

# class Calculation_ViewSet(Resource):
#     serializer_class = calculationSerializer
#     queryset = calculated_channels.objects.all()

class Dashboard_ViewSet(Resource):
    def get(self):
       d=dashboard.query.first()
       dd=dashboardSerializer() 
       res=dd.dump(d)
       return jsonify({'dash':res})

# class data_display(viewsets.ViewSet):
#     def data(self, request):
#         pk = request.data.get('pk')
#         query = calculated_channels.objects.filter(id=pk)
#         serialize = calculationSerializer(query, many=True)
#         return Response(serialize.data)

class AggregatedChannelViewSet(Resource):
    def get(self):
        ag=Aggregated_Channel.query.first()
        ac=aggregated_channelSerializer()
        res=ac.dump(ag)
        return jsonify({'agg_channel':res})

class CalculatedFormulaViewSet(Resource):
    def get(self):
        m=calculation_formula.query.all()
        ms=calculated_formulaSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'calculation_formula':res})

class CalculatedConditionViewSet(Resource):
    def get(self):
        cc=calculation_condition.query.first()
        ccl=calculated_conditionSerializer()
        res=ccl.dump(cc)
        return jsonify({'cond_cl':res})

class formula_typeViewSet(Resource):
    def get(self):
        ft=formula_type.query.all()
        ff=formula_typeSerializer(many=True)
        res=ff.dump(ft)
        return jsonify({'formula':res})

class formula_listViewSet(Resource):
    def get(self):
        fl=formula_list.query.all()
        fls=formula_listSerializer(many=True)
        res=fls.dump(fl)
        return jsonify({'formula_list':res})

class IFViewSet(Resource):
    def get(self):
        m=IF.query.all()
        ms=IFSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'IF':res})

class ConditionViewSet(Resource):
    def get(self):
        c=Condition.query.all()
        cs=ConditionSerializer(many=True)
        res=cs.dump(c)
        return jsonify({'Condition':res})

class SumViewSet(Resource):
    def get(self):
        s=Sum.query.all()
        cs=SumSerializer(many=True)
        res=cs.dump(s)
        return jsonify({'sum':res})
        
    def post(self):
        parser.add_argument('tag_list', type=str)
        args = parser.parse_args()

        return {
            'status': True,
            'tag_list': '{} added. Good'.format(args['tag_list'])
            }

class MeanViewSet(Resource):
    def get(self):
        m=Mean.query.all()
        ms=MeanSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'Mean':res})

class TotalViewSet(Resource):
    def get(self):
        t=Total.query.all()
        ts=TotalSerializer(many=True)
        res=ts.dump(t)
        return jsonify({'Total':res})

class AverageViewSet(Resource):
    def get(self):
        a=Average.query.all()
        ca=AverageSerializer(many=True)
        res=ca.dump(a)
        return jsonify({'Average':res})

# class DashboardHomeSerializer(Resource):
#     def get(self):
#         m=DashboardHome.query.all()
#         ms=DashboardHomeSerializer(many=True)
#         res=ms.dump(m)
#         return jsonify({'DashboardHome':res})