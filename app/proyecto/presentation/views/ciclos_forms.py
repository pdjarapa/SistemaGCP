from django import forms
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, HTML, Row, Fieldset

#from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from app.proyecto.domain.models import CasoPrueba, Proyecto, CicloPrueba


class CicloForm(forms.ModelForm):
    class Meta:
        model = CicloPrueba
        fields=('nombre', 'descripcion')
        widgets = {
            'nombre': forms.TextInput(attrs={'type': 'text', 'placeholder': ''}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': ''}),
        }
        help_texts = {
            'descripcion': 'Descripción del ciclo de prueba'
        }

    def __init__(self, *args, **kwargs):
        super(CicloForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'custom-validate'
        self.helper.form_id = 'formEditar'
        self.helper.layout = Layout(
            'nombre',
            'descripcion',
            ButtonHolder(
                HTML(
                    '<button type="submit" class="btn btn-primary"><i class="fa fa-save"></i> Guardar </button>')
            )

        )

    class Media:
        js = ('js/proyecto/editar.js',)