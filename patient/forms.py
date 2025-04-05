from django import forms
from .models import Operation, Patient
from .models import Evaluation
from .models import AnesthesiaInfo

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

    # ここを追加！
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')


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
