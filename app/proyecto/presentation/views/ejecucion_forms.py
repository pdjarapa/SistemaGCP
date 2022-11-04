from django import forms
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, HTML, Row, Fieldset

#from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from app.proyecto.domain.models import CasoPrueba, Proyecto, CicloPrueba, EjecucionPrueba


class EjecucionForm(forms.ModelForm):
    class Meta:
        model = EjecucionPrueba
        fields=('estado', 'comentario', 'evidencia')
        widgets = {
            'estado': forms.Select(),
            'comentario': forms.Textarea(attrs={'rows': 3, 'placeholder': ''}),

        }
        help_texts = {
            'comentario': 'Ingrese un comentario de la ejecución'
        }

    def __init__(self, *args, **kwargs):
        super(EjecucionForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'custom-validate'
        self.helper.form_id = 'formEditar'
        self.helper.layout = Layout(
            'estado',
            'comentario',
            'evidencia',
            ButtonHolder(
                HTML(
                    '<button type="submit" class="btn btn-primary"><i class="fa fa-save"></i> Guardar </button>')
            )

        )

    class Media:
        js = ('js/proyecto/editar.js',)