from django import forms
from django.contrib.auth.models import User
from django.db import transaction

from api.models.atualizacao import Atualizacao
from api.models.bairro import Bairro
from api.models.banco import Banco
from api.models.cidade import Cidade
from api.models.conta_bancaria import ContaBancaria
from api.models.endereco import Endereco
from api.models.farmacia import Farmacia
from api.models.parceiro import UsuarioParceiro
from api.models.representante_legal import RepresentanteLegal
import re


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
    cep = forms.CharField(label='CEP', max_length=8, required=False)
    logradouro = forms.CharField(label='Logradouro*', max_length=80)
    numero = forms.IntegerField(label='Número', required=False)
    complemento = forms.CharField(max_length=100, required=False)
    cidade = forms.ModelChoiceField(label='Cidade*',queryset=Cidade.objects.all())
    bairro = forms.IntegerField(label='Bairro*', required=True)

    banco = forms.ModelChoiceField(label='Banco*', queryset=Banco.objects.all())
    numero_agencia = forms.IntegerField(label='Número Agência*')
    digito_agencia = forms.CharField(label='Dígito Agência*', max_length=1)
    numero_conta = forms.IntegerField(label='Número Conta*')
    digito_conta = forms.CharField(label='Dígito Conta*', max_length=1)
    operacao = forms.CharField(label='Operação', max_length=3, required=False)
    raio_acao = forms.DecimalField(max_digits=10,decimal_places=2,label="Raio de Ação(KM)")

    class Meta:
        model = Farmacia
        exclude = ('endereco', 'conta_bancaria', 'data_criacao', 'data_atualizacao')

    def __init__(self, *args, **kwargs):
        super(FarmaciaForm, self).__init__(*args, **kwargs)
        self.fields['cidade'].widget.attrs.update({'style': 'width: 100%;'})

    def clean_bairro(self):
        bairro_id = int(self.data['bairro'])
        if bairro_id:
            try:
                return Bairro.objects.get(id=bairro_id)
            except Bairro.DoesNotExist:
                raise forms.ValidationError('Bairro não existe.')
        else:
            return None

    def save(self, commit=True):
        with transaction.atomic():
            self.instance = super(FarmaciaForm, self).save(commit=False)
            self.instance.endereco = self.get_endereco(commit=commit)
            self.instance.conta_bancaria = self.get_conta_bancaria(commit=commit)
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

    def get_conta_bancaria(self, commit=True):
        try:
            obj = ContaBancaria(
                banco=self.cleaned_data['banco'],
                numero_agencia=self.cleaned_data['numero_agencia'],
                digito_agencia=self.cleaned_data['digito_agencia'],
                numero_conta=self.cleaned_data['numero_conta'],
                digito_conta=self.cleaned_data['digito_conta'],
                operacao=self.cleaned_data['operacao']
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
        exclude = ('usuario', 'endereco')

    def clean_confirmacao_senha(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("senha")
        password2 = self.cleaned_data.get("confirmacao_senha")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas incorretas")
        return password2

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        return re.sub(r'\D','',telefone)

    def clean_rg(self):
        rg = self.cleaned_data['rg']
        return re.sub(r'\D','',rg)

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        return re.sub(r'\D','',cpf)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('Ja existe usuário com este email cadastrado.')

        return email

    def clean_bairro(self):
        bairro_id = int(self.data['bairro'])
        if bairro_id:
            try:
                return Bairro.objects.get(id=bairro_id)
            except Bairro.DoesNotExist:
                raise forms.ValidationError('Bairro não existe.')
        else:
            return None

    def get_usuario(self, commit=True):
        try:
            farmacia = self.initial['farmacia']
            username = '{}{}{}'.format(
                farmacia.id,
                farmacia.cnpj[:3].rjust(3, '0'),
                self.cleaned_data['nome']
            )[:30].ljust(30, '0')

            obj = User(
                first_name=self.cleaned_data['nome'],
                last_name=self.cleaned_data['sobrenome'],
                email=self.cleaned_data['email'],
                username=username
            )
            obj.set_password(self.cleaned_data['senha'])

            if commit:
                obj.save()

            return obj
        except Exception as err:
            print(err)
            return None

    def get_endereco(self, commit=True):
        unmask_cep = self.cleaned_data['cep']
        unmask_cep = re.sub(r'\D','',unmask_cep)
        try:
            obj = Endereco(
                cep=unmask_cep,
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

    def save(self, commit=True):
        #cria o representante
        with transaction.atomic():
            self.instance = super(RepresentanteFarmaciaForm, self).save(commit=False)
            self.instance.endereco = self.get_endereco(commit=commit)
            self.instance.usuario = self.get_usuario(commit=commit)
            self.instance.farmacia = self.initial['farmacia']
        #salva
        if commit:
            self.instance.save()
        return self.instance

class UsuarioParceiroForm(forms.ModelForm):
    nome = forms.CharField(max_length=30)
    sobrenome = forms.CharField(max_length=30, required=False)
    email = forms.EmailField()
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    confirmacao_senha = forms.CharField(label='Confirmação de senha', widget=forms.PasswordInput)

    class Meta:
        model = UsuarioParceiro
        exclude = ('usuario',)

    def clean_confirmacao_senha(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("senha")
        password2 = self.cleaned_data.get("confirmacao_senha")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Senhas incorretas")
        return password2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('Ja existe usuário com este email cadastrado.')

        return email

    def get_usuario(self, commit=True):
        try:
            parceiro = self.initial['parceiro']
            cpf_cnpj = parceiro.cpf_cnpj if parceiro.cpf_cnpj else ''
            username = '{}{}{}'.format(
                parceiro.id,
                cpf_cnpj[:3].rjust(3, '0'),
                self.cleaned_data['nome']
            )[:30].ljust(30, '0')

            obj = User(
                first_name=self.cleaned_data['nome'],
                last_name=self.cleaned_data['sobrenome'],
                email=self.cleaned_data['email'],
                username=username
            )
            obj.set_password(self.cleaned_data['senha'])

            if commit:
                obj.save()

            return obj
        except Exception as err:
            print(err)
            return None

    def save(self, commit=True):
        with transaction.atomic():
            self.instance = super(UsuarioParceiroForm, self).save(commit=False)
            self.instance.usuario = self.get_usuario(commit=commit)
            self.instance.parceiro = self.initial['parceiro']
            if commit:
                self.instance.save()
            return self.instance
