from django import forms
from api.models.atualizacao import Atualizacao


class AtualizacaoForm(forms.ModelForm):
    class Meta:
        model = Atualizacao
        fields = (
            'arquivo',
        )

    def __init__(self, *args, **kwargs):
        super(AtualizacaoForm, self).__init__(*args, **kwargs)
        self.fields['arquivo'].required = True
