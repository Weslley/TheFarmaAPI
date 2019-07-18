from rest_framework.relations import RelatedField

class ListPrimaryKeyRelatoionField(RelatedField):

    def to_internal_value(self,value):
        #converte para lista
        if isinstance(value,(str,int)):
            value = [value,]
        #retorna filtrando todos os id da lista
        return self.queryset.filter(pk__in=value)
    
    def to_representation(self,data):
        return data.pk