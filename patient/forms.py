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
    
    
class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'age', 'gender', 'height', 'weight',
            'date', 'procedure', 'surgery_type',
            'surgeon'  # ← 術者を追加！
        ]
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M'  # ← ここ追加！
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            # ここを変える！
            localized_date = localtime(self.instance.date)
            self.initial['date'] = localized_date.strftime('%Y-%m-%dT%H:%M')


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
            'additional_0_5': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
            'additional_1_0': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '30'}),
        }
