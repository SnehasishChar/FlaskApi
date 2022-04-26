# from flask_serialize import FlaskSerialize
from resources.models import *
from flask_marshmallow import Marshmallow
# from flask import DefaultSerializer
from marshmallow import post_load,Schema,fields,EXCLUDE

ma=Marshmallow()
class rtdSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=raw_tags_definition
        # include_relationships = True
        load_instance=True

class aggregated_tagsSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=aggregated_tags
        load_instance=True
        include_fk = True
        # transient = True
       

class aggregation_functionSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =aggregation_function
        load_instance=True
        
class tag_masterSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Tag_Master
        load_instance=True
        # include_fk = True


class tag_master_rawSerializer(ma.SQLAlchemyAutoSchema):
    raw=ma.Nested(rtdSerializer)
    # tag = ma.HyperlinkRelated('Raw_id.parameter')
    # tag2 = ma.Field(source='Raw_id.equipment_id')
    # tag3 = ma.Field(source='Raw_id.LIVE_MEASUREMENT')
    # tag4 = ma.Field(source='Raw_id.measurement_device')
    # tag5 = ma.Field(source='Raw_id.channel_type')
    # tag6 = ma.Field(source='Raw_id.parameter_name')
    class Meta:
        model =Tag_Master
        load_instance=True
        include_fk = True

class tag_master_formulalistSerializer(ma.SQLAlchemyAutoSchema):
    tag =ma.Field(source='Calc_id.Name')
    # aggregation_win_type = serializers.CharField(source='Calc_id.aggregation_win_type')

    class Meta:
        model =Tag_Master
        load_instance=True
class tag_master_aggrSerializer(ma.SQLAlchemyAutoSchema):
    tag = ma.Field(source='Agg_id.aggregated_tags_name')
    class Meta:
        model =Tag_Master
        load_instance=True

# class calculationSerializer(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model =calculated_channels
#         load_instance=True

class aggregated_windowSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =aggregation_window
        load_instance=True

class aggregated_channelSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Aggregated_Channel
        load_instance=True
        include_fk = True

'''class calculated_channelListSerializer(DefaultSerializer):
    def serialize_many(self, instances, only=None):
        super_serialize = super(ma.DefaultSerializer, self).serialize_many
        document = super_serialize(instances, only=only)
        books = [Calculated_Channel_ms(**item) for item in instances]
        return Calculated_Channel_ms.query.all([books])'''

    # def create(self, validated_data):
    #     books = [Calculated_Channel_ms(**item) for item in validated_data]
    #     return Calculated_Channel_ms.objects.bulk_create(books)

class calculated_channelSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        # list_serializer_class =ma.calculated_channelListSerializer
        model =Calculated_Channel_ms
        load_instance=True

class calculated_formulaSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =calculation_formula
        load_instance=True
class calculated_conditionSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =calculation_condition
        load_instance=True

class dashboardSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = dashboard
        fields = ['id', 'graph_type', 'tag_id_aggregation_function', 'tag_id_aggregation_window',
                  'tag_id_calculated_channels', 'duration', 'duration_choices']

class formula_typeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =formula_type
        load_instance=True

class formula_listSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =formula_list
        load_instance=True
        include_fk = True
class IFSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = IF
        oad_instance=True


class ConditionSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Condition
        load_instance=True
        include_fk = True

class SumSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Sum
        load_instance=True

class AverageSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Average
        load_instance=True

class TotalSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =Total
        load_instance=True


class MeanSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mean
        load_instance=True

class DashboardHomeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DashboardHome
        load_instance=True



class ReportHomeSerializer(ma.SQLAlchemyAutoSchema):
    class Meta:
        model =ReportHome
        load_instance=True



