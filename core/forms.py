from django import forms
from api.models.atualizacao import Atualizacao
from api.models.farmacia import Farmacia
from api.models.representante_legal import RepresentanteLegal
from api.models.cidade import Cidade
from api.models.bairro import Bairro
from api.models.endereco import Endereco
from django.contrib.auth.models import User

class AtualizacaoForm(forms.ModelForm):
    class Meta:
        model = Atualizacao
        fields = (
            'arquivo',
        )

    def __init__(self, *args, **kwargs):
        super(AtualizacaoForm, self).__init__(*args, **kwargs)
        self.fields['arquivo'].required = True


class FarmaciaForm(forms.ModelForm):
    cep = forms.CharField(max_length=8, required=False)
    logradouro = forms.CharField(max_length=80)
    numero = forms.IntegerField(required=False)
    complemento = forms.CharField(max_length=100, required=False)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all())
    bairro = forms.IntegerField(required=True)

    class Meta:
        model = Farmacia
        exclude = ('endereco', 'latitude', 'longitude')

    def clean_bairro(self):
        bairro_id = int(self.data['bairro'])
        if bairro_id:
            try:
                return Bairro.objects.get(id=bairro_id)
            except Bairro.DoesNotExist:
                return None
        else:
            return None

    def save(self, commit=True):
        self.instance = super(FarmaciaForm, self).save(commit=False)
        self.instance.endereco = self.get_endereco(commit=commit)
        if commit:
            self.instance.save()
        return self.instance

    def get_endereco(self, commit=True):
        try:
            obj = Endereco(
                cep=self.cleaned_data['cep'],
                logradouro=self.cleaned_data['logradouro'],
                numero=self.cleaned_data['numero'],
                complemento=self.cleaned_data['complemento'],
                cidade=self.cleaned_data['cidade'],
                bairro=self.cleaned_data['bairro']
            )

            if commit:
                obj.save()

            return obj
        except Exception as err:
            print(err)
            return None


class RepresentanteFarmaciaForm(forms.ModelForm):
    nome = forms.CharField(max_length=30)
    sobrenome = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmacao_senha = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)
    cep = forms.CharField(max_length=8, required=False)
    logradouro = forms.CharField(max_length=80)
    numero = forms.IntegerField(required=False)
    complemento = forms.CharField(max_length=100, required=False)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all())
    bairro = forms.IntegerField(required=True)

    class Meta:
        model = RepresentanteLegal
        exclude = ('usuario', 'endereco', 'farmacia')

    def clean_confirmacao_senha(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("senha")
        password2 = self.cleaned_data.get("confirmacao_senha")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas incorretas")
        return password2

    def get_endereco(self, commit=True):
        try:
            obj = Endereco(
                cep=self.cleaned_data['cep'],
                logradouro=self.cleaned_data['logradouro'],
                numero=self.cleaned_data['numero'],
                complemento=self.cleaned_data['complemento'],
                cidade=self.cleaned_data['cidade'],
                bairro=self.cleaned_data['bairro']
            )

            if commit:
                obj.save()

            return obj
        except Exception as err:
            print(err)
            return None

    def get_usuario(self, commit=True):
        pass

    def save(self, commit=True):
        obj = super(RepresentanteFarmaciaForm, self).save(commit=False)
        print(obj)
        import pdb; pdb.set_trace()
        return self.instance
