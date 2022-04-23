from flask import Flask,request, jsonify
from flask_restful import Resource, Api,abort,marshal_with

from .models import *
from .serializers import *
from flask_marshmallow import Marshmallow
app = FlaskAPI(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://VISHWAJIT\SQLEXPRESS/daskha?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma=Marshmallow(app)

# app.secret_key = 'super secret string'




class Raw(Resource):
    def get(self):
        one_user=raw_tags_definition.query.all()
        rtdschema=rtdSerializer(many=True)
        output=rtdschema.dump(one_user)
        return jsonify({'raw_tags':output})



class Agg_Fun(Resource):
    def get(self):
        fun=aggregation_function.query.all()
        aggfun=aggregation_functionSerializer(many=True)
        res=aggfun.dump(fun)
        return jsonify({'agg_fun':res})

class Tag(Resource):
    def get(self):
        tag=Tag_Master.query.first()
        tagm=tag_masterSerializer()
        res=tagm.dump(tag)
        return jsonify({'agg_fun':res})

class TagRaw(Resource):
    def get(self):
        raw=raw_tags_definition.query.first()
        rtd=rtdSerializer()
        tag1=Tag_Master.query.join(raw_tags_definition,
        Tag_Master.Raw_id==raw_tags_definition.id).add_columns(
        Tag_Master.Raw_id).filter(Tag_Master.Raw_id==raw_tags_definition.id).first()
        tagm=tag_master_rawSerializer()
        res=tagm.dump(tag1)
        res1=rtd.dump(raw)

        return jsonify({'TagRaw':res,'raw':res1})

class Agg_Win(Resource):
    def get(self):
        w=aggregation_window.query.all()
        aw=aggregated_windowSerializer(many=True)
        # j=json.dumps(aw)
        res=aw.dump(w)
        return jsonify({'agg_win':res})

class Agg(Resource):
    def get(self):
        tags=aggregated_tags.query.all()
        aggtag=aggregated_tagsSerializer(many=True)
        res=aggtag.dump(tags)
        return jsonify({'agg_tags':res})

class Agg_channel(Resource):
    def get(self):
        ag=Aggregated_Channel.query.first()
        ac=aggregated_channelSerializer()
        res=ac.dump(ag)
        return jsonify({'agg_channel':res})

class Cond_c(Resource):
    def get(self):
        cc=calculation_condition.query.first()
        ccl=calculated_conditionSerializer()
        res=ccl.dump(cc)
        return jsonify({'cond_cl':res})

class Dash(Resource):
    def get(self):
       d=dashboard.query.first()
       dd=dashboardSerializer() 
       res=dd.dump(d)
       return jsonify({'dash':res})

class Formula(Resource):
    def get(self):
        ft=formula_type.query.all()
        ff=formula_typeSerializer(many=True)
        res=ff.dump(ft)
        return jsonify({'formula':res})

class Form_list(Resource):
    def get(self):
        fl=formula_list.query.all()
        fls=formula_listSerializer(many=True)
        res=fls.dump(fl)
        return jsonify({'formula_list':res})

class Cond(Resource):
    def get(self):
        c=Condition.query.all()
        cs=ConditionSerializer(many=True)
        res=cs.dump(c)
        return jsonify({'Condition':res})

class Add(Resource):
    def get(self):
        s=Sum.query.all()
        cs=SumSerializer(many=True)
        res=cs.dump(s)
        return jsonify({'sum':res})

class Avg(Resource):
    def get(self):
        a=Average.query.all()
        ca=AverageSerializer(many=True)
        res=ca.dump(a)
        return jsonify({'Average':res})

class Tot(Resource):
    def get(self):
        t=Total.query.all()
        ts=TotalSerializer(many=True)
        res=ts.dump(t)
        return jsonify({'Total':res})

class Mea(Resource):
    def get(self):
        m=Mean.query.all()
        ms=MeanSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'Mean':res})

class IFF(Resource):
    def get(self):
        m=IF.query.all()
        ms=IFSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'IF':res})

class Dashome(Resource):
    def get(self):
        m=DashboardHome.query.all()
        ms=DashboardHomeSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'DashboardHome':res})

class Report(Resource):
    def get(self):
        m=ReportHome.query.all()
        ms=ReportHomeSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'ReportHome':res})

class Calfor(Resource):
    def get(self):
        m=calculation_formula.query.all()
        ms=calculated_formulaSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'calculation_formula':res})

api.add_resource(Calfor, '/calfor')         
api.add_resource(Report, '/report')    
api.add_resource(Dashome, '/dashome')
api.add_resource(IFF, '/if')
api.add_resource(Tot, '/total')
api.add_resource(Mea, '/mean')
api.add_resource(Avg, '/avg')
api.add_resource(Add, '/add')
api.add_resource(Cond, '/cond')
api.add_resource(Form_list, '/forml')
api.add_resource(Formula, '/formula')
api.add_resource(Dash, '/dash')
api.add_resource(Cond_c, '/conc')
api.add_resource(Agg_channel, '/channel')
api.add_resource(Agg_Win, '/win')
api.add_resource(TagRaw, '/tagr')
api.add_resource(Tag, '/tag')
api.add_resource(Agg_Fun, '/fun')
api.add_resource(Raw, '/raw')
api.add_resource(Agg, '/')
if __name__ == '__main__':
    app.run(debug=True)

   
