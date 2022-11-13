from django import forms
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, ButtonHolder, HTML, Row, Fieldset

#from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from app.proyecto.domain.models import CasoPrueba, Proyecto


class CasosForm(forms.ModelForm):
    class Meta:
        model = CasoPrueba
        fields=('codigo', 'nombre', 'descripcion','precondicion','pasos','resultado_esperado','tipo','variedad','prioridad','evaluacion','postcondicion','observacion')
        widgets = {
            'codigo': forms.TextInput(attrs={'type': 'text', 'placeholder': ''}),
            'nombre': forms.TextInput(attrs={'type': 'text', 'placeholder': ''}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': ''}),
            'precondicion': forms.Textarea(attrs={'rows':3}),
            'pasos': forms.Textarea(attrs={'rows':3}),
            'resultado_esperado': forms.Textarea(attrs={'rows':3}),
            'tipo':forms.Select(),
            'evaluacion':forms.Select(),
            'variedad':forms.Select(),
            'prioridad':forms.Select(),
            #'estado':forms.Select(),
            'postcondicion': forms.TextInput(attrs={'type': 'text', 'placeholder': ''}),
            'observacion': forms.Textarea(attrs={'rows':3}),
        }
        help_texts = {
            'descripcion': 'Descripción del espacio de trabajo'
        }

    def __init__(self, *args, **kwargs):
        super(CasosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'custom-validate'
        self.helper.form_id = 'formEditar'
        self.helper.layout = Layout(
            Div(
                Div('codigo', css_class='col-md-2'),
                Div('nombre', css_class='col-md-10'),
                css_class='row'
            ),
            'descripcion',
            'precondicion',
            'pasos',
            'resultado_esperado',
            Div(
                Div('tipo', HTML('<div class="form-group"><label>Estado</label> <div>%s</div></div>' % self.instance.get_estado_display()), css_class="col-md-4"),
                Div('prioridad', 'evaluacion', css_class="col-md-4"),
                Div('variedad', css_class="col-md-4"),
                css_class='row'
            ),
            'postcondicion',
            'observacion',
            ButtonHolder(
                HTML(
                    '<button type="submit" class="btn btn-primary disabled" disabled="disabled"><i class="fa fa-save"></i> Guardar</button>'
                    if self.instance.id and self.instance.proyecto.activo is False else
                    '<button type="submit" class="btn btn-primary %s"><i class="fa fa-save"></i> Guardar</button>'
                )
            )

        )

    class Media:
        js = ('js/proyecto/editar.js',)