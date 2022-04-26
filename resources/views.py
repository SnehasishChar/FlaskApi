from select import select
from tokenize import Name
from webbrowser import get
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
from sqlalchemy.sql import exists
from flask import *
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
#     queryset = calculated_channels.query.all()

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
#         query = calculated_channels.query.filter_by(id=pk)
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
        db.session.add(ag)
        db.session.commit()
        result=ac.dump(ag)
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
    def post(self):
        data=request.get_json()
        id=data['id']
        formula_name =data['formula_name']
        formula_title =data['formula_title']
        cf=calculation_formula(id=id,formula_name=formula_name,formula_title=formula_title)
        af=calculated_formulaSerializer()
        db.session.add(cf)
        db.session.commit()
        dump_data = af.dump(cf)
        return jsonify({'condition formula':dump_data})

class CalculatedFormulaViewSet1(Resource):
    def get(self,id):
        m=calculation_formula.query.get(id)
        ms=calculated_formulaSerializer()
        if m:
            res=ms.dump(m)
            return jsonify({'calculation_formula':res})
        else:
            return jsonify({'message':'calculation_formula not found'})
    def put(self,id):
        data=request.get_json()
        cf=calculation_formula.query.get(id)
        cs=calculated_formulaSerializer()
        if cf:
            cf.id=data['id']
            cf.formula_name =data['formula_name']
            cf.formula_title =data['formula_title']
        else:
            cf=calculation_formula.query.get(id=id,**data)
        db.session.add(cf)
        db.session.commit()
        result=cs.dump(cf)
        return jsonify({'update record':result})

    def delete(self,id):
        a=calculation_formula.query.get(id)
        if a:
            db.session.delete(a)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 

        else:
            return {'message': 'calculation_formula not found'}
class CalculatedConditionViewSet(Resource):
    def get(self):
        cc=calculation_condition.query.all()
        ccl=calculated_conditionSerializer(many=True)
        res=ccl.dump(cc)
        return jsonify({'cond_cl':res})
    def post(self):
        data=request.get_json()
        id=data['id']
        condition_name =data['condition_name']
        condition_title =data['condition_title']
        cc=calculation_condition(id=id,condition_name=condition_name,condition_title=condition_title)
        cs=calculated_conditionSerializer()
        db.session.add(cc)
        db.session.commit()
        dump_data = cs.dump(cc)
        return jsonify({'calculate condition':dump_data}) 
class CalculatedConditionViewSet1(Resource):
    def get(self,id):
        m=calculation_condition.query.get(id)
        ms=calculated_conditionSerializer()
        if m:
            res=ms.dump(m)
            return jsonify({'calculation_condition':res})
        else:
            return jsonify({'message':'calculation_formula not found'})
    def put(self,id):
        data=request.get_json()
        cc=calculation_condition.query.get(id)
        cs=calculated_conditionSerializer()
        if cc:
            cc.id=data['id']
            cc.condition_name =data['condition_name']
            cc.condition_title =data['condition_title']
        else:
            cc=calculation_condition.query.get(id=id,**data)
        db.session.add(cc)
        db.session.commit()
        result=cs.dump(cc)
        return jsonify({'update record':result})

    def delete(self,id):
        a=calculation_condition.query.get(id)
        if a:
            db.session.delete(a)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 
        else:
            return {'message': 'calculation_condition not found'}
class formula_typeViewSet(Resource):
    def get(self):
        ft=formula_type.query.all()
        ff=formula_typeSerializer(many=True)
        res=ff.dump(ft)
        return jsonify({'formula':res})
    def post(self):
        data=request.get_json()
        id=data['id']
        Name=data['Name']
        fl=formula_type(id=id,Name=Name)
        fls=formula_typeSerializer()
        db.session.add(fl)
        db.session.commit()
        dump_data = fls.dump(fl)
        return jsonify({'formula_type':dump_data}) 

class formula_typeViewSet1(Resource):
    def get(self,id):
        ft=formula_type.query.get(id)
        ff=formula_typeSerializer()
        if ff:
            res=ff.dump(ft)
            return jsonify({'formula':res})
        else:
            return jsonify({'message':'formula type not found'})
    def put(self,id):
        data=request.get_json()
        ft=formula_type.query.get(id)
        ff=formula_typeSerializer()
        if ft:
            ft.id=data['id']
            ft.Name=data['Name']
        else:
            ft=formula_type.query.get(id=id,**data)
        db.session.add(ft)
        db.session.commit()
        result=ff.dump(ft)
        return jsonify({'update record':result})

    def delete(self,id):
        f=formula_type.query.get(id)
        if f:
            db.session.delete(f)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 
        else:
            return {'message': 'formula type not found'}
    

class formula_listViewSet(Resource):
    def get(self):
        fl=formula_list.query.all()
        fls=formula_listSerializer(many=True)
        res=fls.dump(fl)
        return jsonify({'formula_list':res})

    def post(self):
        data=request.get_json()
        id=data['id']
        formula_type_id=data['formula_type_id']
        Formula_id=data['Formula_id']
        Name=data['Name']
        aggregation_win_type=data['aggregation_win_type']
        fl=formula_list(id=id,formula_type_id=formula_type_id,Formula_id=Formula_id,Name=Name,aggregation_win_type=aggregation_win_type)
        fls=formula_listSerializer()
        db.session.add(fl)
        db.session.commit()
        dump_data = fls.dump(fl)
        return jsonify({'formula_list':dump_data}) 
class formula_listViewSet1(Resource):
    def get(self,id):
        fl=formula_list.query.get(id)
        fls=formula_listSerializer()
        if fl:
            res=fls.dump(fl)
            return jsonify({'formula_list':res})
        else:
            return jsonify({'message':'formula list not found'})
    def put(self,id):
        data=request.get_json()
        ft=formula_list.query.get(id)
        ff=formula_listSerializer()
        if ft:
            ft.id=data['id']
            ft.formula_type_id=data['formula_type_id']
            ft.Formula_id=data['Formula_id']
            ft.Name=data['Name']
            ft.aggregation_win_type=data['aggregation_win_type']
        else:
            ft=formula_list.query.get(id=id,**data)
        db.session.add(ft)
        db.session.commit()
        result=ff.dump(ft)
        return jsonify({'update record':result})

    def delete(self,id):
        f=formula_list.query.get(id)
        if f:
            db.session.delete(f)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 
        else:
            return {'message': 'formula list not found'}


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
    def post(self):
        data=request.get_json()
        id=data['id']
        Tag_id=data['Tag_id']
        operator_id=data['operator_id']
        value =data['value']
        c=Condition(id=id,Tag_id=Tag_id,operator_id=operator_id,value=value)
        cs=ConditionSerializer()
        db.session.add(c)
        db.session.commit()
        dump_data = cs.dump(c)
        return jsonify({'Condition':dump_data})

class ConditionViewSet1(Resource):
    def get(self,id):
        c=Condition.query.get(id)
        cs=ConditionSerializer()
        if c:
            res=cs.dump(c)
            return jsonify({'Condition':res})
        else:
            return jsonify({'message':'formula list not found'})

    def put(self,id):
        data=request.get_json()
        c=Condition.query.get(id)
        cs=ConditionSerializer()
        if c:
            c.id=data['id']
            c.Tag_id=data['Tag_id']
            c.operator_id=data['operator_id']
            c.value =data['value']
        else:
            c=Condition.query.get(id=id,**data)
        db.session.add(c)
        db.session.commit()
        result=cs.dump(c)
        return jsonify({'update record':result})

    def delete(self,id):
        f=Condition.query.get(id)
        if f:
            db.session.delete(f)
            db.session.commit() 
            return jsonify({'delete':'sucess'}) 
        else:
            return {'message': 'formula list not found'}

class TagMasterView(Resource):
    def get(self):
        tag=Tag_Master.query.first()
        tagm=tag_masterSerializer()
        res=tagm.dump(tag)
        return jsonify({'agg_fun':res})

class SumViewSet(Resource):
    def get(self):
        s=Sum.query.all()
        cs=SumSerializer(many=True)
        res=cs.dump(s)
        return jsonify({'sum':res})
        
    

        

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

class DashboardHomeView(Resource):
    def get(self):
        m=DashboardHome.query.all()
        ms=DashboardHomeSerializer(many=True)
        res=ms.dump(m)
        return jsonify({'DashboardHome':res})


def get_dashboard_home_details(an_item):
    tags_value = an_item.Tag_list.split(",")
    all_tag_name = []
    y_label = []    
    for tag in tags_value:
        # print(Tag_Master.query.filter_by(id=int(tag), Agg_id=None, Calc_id=None).first())
        if Tag_Master.query.filter_by(id=int(tag), Agg_id=None, Calc_id=None).first():
            tag_data = Tag_Master.query.filter_by(id=int(tag), Agg_id=None, Calc_id=None).first()
            raw_data = raw_tags_definition.query.filter_by(id=tag_data.Raw_id).first()
            all_tag_name.append(raw_data.equipment_id + " / " + raw_data.parameter + " / " +
                                raw_data.measurement_device + " (" + raw_data.channel_type + ") - " +
                                raw_data.parameter_name)
            y_label.append(tag_data.unit_of_measurement)
        elif Tag_Master.query.filter_by(id=int(tag), Raw_id=None, Calc_id=None).first():
            tag_data = Tag_Master.query.filter_by(id=int(tag)).first()
            all_tag_name.append(tag_data.Agg_id.aggregated_tags_name)
            y_label.append(tag_data.unit_of_measurement)
        elif Tag_Master.query.filter_by(id=int(tag), Raw_id=None, Agg_id=None).first():
            tag_data = Tag_Master.query.filter_by(id=int(tag)).first()
            all_tag_name.append(tag_data.Calc_id.Name)
            y_label.append(tag_data.unit_of_measurement)
    
    return({
        "id": an_item.id, "Name": an_item.Name, "Tag_list": all_tag_name, "Chart_type": an_item.Chart_type,
        "color": an_item.color, "dashboard": an_item.dashboard, "graph_id": an_item.graph_id, "y_label": y_label
    })
        
class DashboardHomeView1(Resource):
    def get(self):
        try:
            dashboard_id = dashboard_home_id = None
            if request.args.get('search'):
                dashboard_id = request.args.get('search')
            if request.args.get('id'):
                dashboard_home_id = request.args.get('id')
            data = []
            if request.args.get('id'):
                if dashboard_home_id == '0':
                    all_dashboard_home_data = DashboardHome.query.all()
                    for an_item in all_dashboard_home_data:
                            data.append(get_dashboard_home_details(an_item))
                else:
                    an_item = DashboardHome.query.filter_by(id=int(dashboard_home_id)).first()
                    data.append(get_dashboard_home_details(an_item))
            elif request.args.get('search'):
                all_dashboard_home_data = DashboardHome.query.filter_by(dashboard=dashboard_id).all()
                if all_dashboard_home_data:
                    for an_item in all_dashboard_home_data:
                        data.append(get_dashboard_home_details(an_item))
                else:
                    data.append({'message': 'No data found.'})
            return jsonify({'data': data})
        except Exception as e:
            return jsonify({'message': 'No data found.', 'error': str(e)})

        
        results="'DashboardHome.query.filter_by(DashboardHome.Name.like('%'+search_fields+'%')).all()'"
        ms=DashboardHomeSerializer(many=True)
        if results: 
            res=ms.dump(results)
            return jsonify({'DashboardHome':res})
        else:
            return jsonify({'msg':'search fields not found'})
    


