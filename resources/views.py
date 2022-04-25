from flask import Flask,request, jsonify
from flask_restful import Resource, Api, abort
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy_utils import  ChoiceType
from .models import *
from .serializers import *
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
app = FlaskAPI(__name__)



class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class RTDViewSet(Resource):
    def get(self):
        one_user=raw_tags_definition.query.all()
        rtdschema=rtdSerializer(many=True)
        output=rtdschema.dump(one_user)
        return jsonify({'raw_tags':output})
    
    def post(self):
        data = request.get_json()
        id=data['id']
        parameter=data['parameter']
        equipment_id=data['equipment_id']
        LIVE_MEASUREMENT=data['LIVE_MEASUREMENT']
        measurement_device=data['measurement_device']
        channel_type=data['channel_type']
        parameter_name=data['parameter_name']
        raw=raw_tags_definition(id=id,parameter=parameter,equipment_id=equipment_id,
        LIVE_MEASUREMENT=LIVE_MEASUREMENT,measurement_device=measurement_device,channel_type=channel_type,
        parameter_name=parameter_name)
        rawtag=rtdSerializer()
        db.session.add(raw)
        db.session.commit()
        res=rawtag.dump(raw)
        return jsonify({'raw_tags':res})
class RTDViewSet1(Resource):
    def get(self,id):
        one_user=raw_tags_definition.query.get(id)
        rtdschema=rtdSerializer()
        if one_user:
            output=rtdschema.dump(one_user)
            return jsonify({'raw_tags':output})
        else:
            return jsonify({'message':'Raw_tags not found'})
        
    def put(self,id):
        data = request.get_json()
        one_user=raw_tags_definition.query.get(id)
        rtdschema=rtdSerializer()
        if one_user:
            one_user.id=data['id']
            one_user.parameter=data['parameter']
            one_user.equipment_id=data['equipment_id']
            one_user.LIVE_MEASUREMENT=data['LIVE_MEASUREMENT']
            one_user.measurement_device=data['measurement_device']
            one_user.channel_type=data['channel_type']
            one_user.parameter_name=data['parameter_name']

        else:
            one_user = raw_tags_definition(id=id,**data)
        db.session.add(one_user)
        db.session.commit()
        result=rtdschema.dump(one_user)
        return jsonify({'update':result})

    def delete(self,id):
        raw=raw_tags_definition.query.get(id)
        if raw:
            db.session.delete(raw)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_tags not found'}


class Agree_Tag_ViewSet(Resource):
    def get(self):
        tags=aggregated_tags.query.all()
        aggtag=aggregated_tagsSerializer(many=True)
        res=aggtag.dump(tags)
        return jsonify({'agg_tags':res})
        
    
    def post(self):
        args = request.get_json()
        id = args['id']
        aggregated_function = args['aggregated_function']
        aggregated_tags_name=args['aggregated_tags_name']
        aggregation_win_type=args['aggregation_win_type']
        aggregation_win_value=args['aggregation_win_value']
        raw_tags=args['raw_tags']
        aggt=aggregated_tagsSerializer()
        aggtag=aggregated_tags(aggregated_function = aggregated_function,aggregated_tags_name=aggregated_tags_name,aggregation_win_type=aggregation_win_type,
        aggregation_win_value=aggregation_win_value,id=id,raw_tags= raw_tags)
        db.session.add(aggtag)
        db.session.commit()
        dump_data = aggt.dump(aggtag)
        return jsonify({'agg':dump_data})

class Agree_Tag_ViewSet1(Resource):
    def get(self,id):
        aggtags=aggregated_tags.query.get(id)
        agg=aggregated_tagsSerializer()
        if aggtags:
            res=agg.dump(aggtags)
            return jsonify({'agg_tags':res})
        else:
            return jsonify({'message':'aggregated_tags not found'})
    def put(self,id):
        data = request.get_json()
        tag=aggregated_tags.query.get(id)
        aggtags=aggregated_tagsSerializer()
        if tag:
            tag.aggregated_function=data['aggregated_function']
            tag.aggregated_tags_name=data['aggregated_tags_name']
            tag.aggregation_win_type=data['aggregation_win_type']
            tag.aggregation_win_value=data['aggregation_win_value']
            tag.raw_tags=data['raw_tags']
            
        else:
            tag = aggregated_tags(id=id,**data)
        db.session.add(tag)
        db.session.commit()
        result=aggtags.dump(tag)
        return jsonify({'update':result})


    def delete(self,id):
        aa=aggregated_tags.query.get(id)
        if aa:
            db.session.delete(aa)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_tags not found'}

class Agree_Function_ViewSet(Resource):
    def get(self):
        fun=aggregation_function.query.all()
        aggfun=aggregation_functionSerializer(many=True)
        res=aggfun.dump(fun)
        return jsonify({'agg_fun':res})

    def post(self):
        data = request.get_json()
        id = data['id']
        function_name=data['function_name']
        function_title=data['function_title']
        aggfun=aggregation_functionSerializer()
        fun=aggregation_function(id=id,function_name=function_name,function_title=function_title)
        db.session.add(fun)
        db.session.commit()
        dump_data = aggfun.dump(fun)
        return jsonify({'agg':dump_data})

class Agree_Function_ViewSet1(Resource):
    def get(self,id):
        fun=aggregation_function.query.get(id)
        aggfun=aggregation_functionSerializer()
        if fun:
            funn=aggfun.dump(fun)
            return jsonify({'raw_tags':funn})
        else:
            return jsonify({'message':'Agree_Function not found'})
    
    def put(self,id):
        data = request.get_json()
        fun=aggregation_function.query.get(id)
        aggfun=aggregation_functionSerializer()
        if fun:
            fun.id = data['id']
            fun.function_name=data['function_name']
            fun.function_title=data['function_title']
        else:
            fun=aggregation_function(id=id,**data)
        db.session.add(fun)
        db.session.commit()
        result=aggfun.dump(fun)
        return jsonify({'update record':result})
    def delete(self,id):
        fun=aggregation_function.query.get(id)
        if fun:
            db.session.delete(fun)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_tags not found'}

class Agree_Window_ViewSet(Resource):
    def get(self):
        w=aggregation_window.query.all()
        aw=aggregated_windowSerializer(many=True)
        res=aw.dump(w)
        return jsonify({'agg_win':res})

    def post(self):
        data=request.get_json()
        id=data['id']
        window_type=data['window_type'] 
        window_title =data['window_title']
        window=data['window']
        win=aggregation_window(id=id,window_type=window_type,window_title=window_title,window=window)
        aw=aggregated_windowSerializer()
        db.session.add(win)
        db.session.commit()
        dump_data = aw.dump(win)
        return jsonify({'agg':dump_data})

class Agree_Window_ViewSet1(Resource):
    def get(self,id):
        w=aggregation_window.query.get(id)
        aw=aggregated_windowSerializer()
        if w:
            res=aw.dump(w)
            return jsonify({'agg_win':res})
        else:
            return jsonify({'message':'Agree_Window not found'})

    def put(self,id):
        data=request.get_json()
        w=aggregation_window.query.get(id)
        aw=aggregated_windowSerializer()
        if w:
            w.id=data['id'] 
            w.window_type=data['window_type'] 
            w.window_title =data['window_title']
            w.window=data['window']   
        else:
            w=aggregation_window.query.get(id=id,**data)
        db.session.add(w)
        db.session.commit()
        result=aw.dump(w)
        return jsonify({'update record':result})

    def delete(self,id):
        win=aggregation_window.query.get(id)
        if win:
            db.session.delete(win)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_tags not found'}
        


# class Calculation_ViewSet(Resource):
#     serializer_class = calculationSerializer
#     queryset = calculated_channels.objects.all()

class Dashboard_ViewSet(Resource):
    def get(self):
       d=dashboard.query.all()
       dd=dashboardSerializer(many=True) 
       res=dd.dump(d)
       return jsonify({'dash':res})
    def post(self):
        data=request.get_json()
        id=data['id']
        graph_type=data['graph_type'] 
        tag_id_aggregation_function =data['tag_id_aggregation_function']
        tag_id_aggregation_window=data['tag_id_aggregation_window']
        duration=data['duration']
        duration_choices=data['duration_choices']
        d=dashboard(id=id,graph_type=graph_type,tag_id_aggregation_function=tag_id_aggregation_function,
        tag_id_aggregation_window=tag_id_aggregation_window,duration=duration,duration_choices=duration_choices)
        dd=dashboardSerializer() 
        db.session.add(d)
        db.session.commit()
        dump_data = dd.dump(d)
        return jsonify({'agg':dump_data})
        
class Dashboard_ViewSet1(Resource):
    def get(self,id):
       d=dashboard.query.get(id)
       dd=dashboardSerializer()
       if d:
            res=dd.dump(d)
            return jsonify({'dash':res})  
       else:
            return jsonify({'message':'Dashboard not found'})
  
    def put(self,id):
        data=request.get_json()
        d=dashboard.query.get(id)
        ds=dashboardSerializer()
        if d:
            d.id=data['id'] 
            d.graph_type=data['graph_type'] 
            d.tag_id_aggregation_function =data['tag_id_aggregation_function']
            d.tag_id_aggregation_window=data['tag_id_aggregation_window']
            d.duration=data['duration']
            d.duration_choices=data['duration_choices']
        else:
            d=dashboard.query.get(id=id,**data)
        db.session.add(d)
        db.session.commit()
        result=ds.dump(d)
        return jsonify({'update record':result})

    def delete(self,id):
        d=dashboard.query.get(id)
        if d:
            db.session.delete(d)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_tags not found'}
# class data_display(viewsets.ViewSet):
#     def data(self, request):
#         pk = request.data.get('pk')
#         query = calculated_channels.objects.filter(id=pk)
#         serialize = calculationSerializer(query, many=True)
#         return Response(serialize.data)

class AggregatedChannelViewSet(Resource):
    def get(self):
        ag=Aggregated_Channel.query.all()
        ac=aggregated_channelSerializer(many=True)
        res=ac.dump(ag)
        return jsonify({'agg_channel':res})
    def post(self):
        data=request.get_json()
        id=data['id']
        aggregated_tags_id =data['aggregated_tags_id'] 
        value =data['value']
        tm=data['tm']
        ts=data['ts']
        a=Aggregated_Channel(id=id,aggregated_tags_id=aggregated_tags_id,value=value,tm=tm,ts=ts)
        ac=aggregated_channelSerializer()
        db.session.add(a)
        db.session.commit()
        dump_data = ac.dump(a)
        return jsonify({'agg':dump_data})
class AggregatedChannelViewSet1(Resource):
    def get(self,id):
        ag=Aggregated_Channel.query.get(id)
        ac=aggregated_channelSerializer()
        if ag:
            res=ac.dump(ag)
            return jsonify({'agg_channel':res})
        else:
            return jsonify({'message':'Aggregated Channel not found'})
    def put(self,id):
        data=request.get_json()
        ag=Aggregated_Channel.query.get(id)
        ac=aggregated_channelSerializer()
        if ag:
            ag.id=data['id']
            ag.aggregated_tags_id =data['aggregated_tags_id'] 
            ag.value =data['value']
            ag.tm=data['tm']
            ag.ts=data['ts']
        else:
            a=Aggregated_Channel.query.get(id=id,**data)
        db.session.add(a)
        db.session.commit()
        result=ac.dump(a)
        return jsonify({'update record':result})

    def delete(self,id):
        a=Aggregated_Channel.query.get(id)
        if a:
            db.session.delete(a)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'aggregated_channel not found'}
  

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

