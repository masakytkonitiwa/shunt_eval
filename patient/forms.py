from django import forms
from .models import Operation, Patient
from .models import Evaluation
from .models import AnesthesiaInfo
from django.utils.timezone import localtime



class PatientIDForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_code']
        labels = {
            'patient_code': '患者ID',
        }
    
from django.utils.timezone import localtime
from django import forms
from .models import Operation


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'age', 'gender', 'height', 'weight',
            'date', 'procedure', 'surgery_type',
            'surgeon'
        ]
        widgets = {
            'age': forms.NumberInput(attrs={'min': 0, 'max': 120, 'step': 1}),
            'height': forms.NumberInput(attrs={'min': 0, 'max': 250, 'step': 0.1}),
            'weight': forms.NumberInput(attrs={'min': 0, 'max': 200, 'step': 0.1}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            localized_date = localtime(self.instance.date)
            self.initial['date'] = localized_date.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()

        fields_to_check = ['age', 'height', 'weight']

        for field in fields_to_check:
            value = cleaned_data.get(field)
            if value is not None:
                try:
                    float(value)
                except (ValueError, TypeError):
                    self.add_error(field, "半角の数字で入力してください。")



SENSORY_CHOICES = [
    (0, '0'), (1, '1'), (2, '2'),
]

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'sensory_A', 'sensory_B', 'sensory_C', 'sensory_D',
            'motor_elbow', 'motor_hand',
            'observation_1', 'observation_2', 'observation_3', 'observation_4',
            'signer'
        ]
        widgets = {
            'signer': forms.TextInput(attrs={'placeholder': '記録者名'}),
        }

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step', None)  # 🆕 step を受け取る
        super().__init__(*args, **kwargs)

        # オペ前（step == 0）のときだけ初期値をセット
        if step == 0 or step == '0':
            self.fields['sensory_A'].initial = 0
            self.fields['sensory_B'].initial = 0
            self.fields['sensory_C'].initial = 0
            self.fields['sensory_D'].initial = 0
            self.fields['motor_elbow'].initial = 0
            self.fields['motor_hand'].initial = 0
            self.fields['observation_1'].initial = 0
            self.fields['observation_2'].initial = 0
            self.fields['observation_3'].initial = 0
            self.fields['observation_4'].initial = 0




class AnesthesiaInfoForm(forms.ModelForm):
    class Meta:
        model = AnesthesiaInfo
        fields = [
            'drug_type',
            'block_amount_1',
            'block_amount_2',
            'block_amount_3',
            'block_amount_4',
            'additional_0_5',
            'additional_1_0',
        ]
        labels = {
            'drug_type': 'ブロック使用薬剤',
            'block_amount_1': '① (ml)',
            'block_amount_2': '② (ml)',
            'block_amount_3': '③ (ml)',
            'block_amount_4': '④ (ml)',
            'additional_0_5': '0.5% 使用量 (ml)',
            'additional_1_0': '1% 使用量 (ml)',
        }
        widgets = {
            'block_amount_1': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
            'block_amount_2': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
            'block_amount_3': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
            'block_amount_4': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
            'additional_0_5': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '50'}),
            'additional_1_0': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '50'}),
        }
        
    def clean(self):
            cleaned_data = super().clean()

            # 数値をチェックするフィールドリスト
            fields_to_check = [
                'block_amount_1', 'block_amount_2', 'block_amount_3', 'block_amount_4',
                'additional_0_5', 'additional_1_0',
            ]

            for field in fields_to_check:
                value = cleaned_data.get(field)
                if value is not None:
                    try:
                        float(value)
                    except (ValueError, TypeError):
                        self.add_error(field, "半角の数字で入力してください。")
