from django import forms
from .models import Patient, Operation, Evaluation, AnesthesiaInfo
from django.utils.timezone import localtime
from decimal import Decimal

# --- ここから Patient 登録用フォーム ---
class PatientIDForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_code']
        labels = {
            'patient_code': '患者ID',
        }

# --- ここから Operation 登録・編集用フォーム ---
class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = [
            'age', 'gender', 'height', 'weight',
            'date', 'procedure', 'surgery_type', 'surgeon'
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
        for field in ['age', 'height', 'weight']:
            value = cleaned_data.get(field)
            if value is not None:
                try:
                    float(value)
                except (ValueError, TypeError):
                    self.add_error(field, "半角の数字で入力してください。")
                    
                    

# --- Evaluation フォーム（感覚・運動評価）---
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'sensory_A', 'sensory_B', 'sensory_C', 'sensory_D',
            'motor_elbow', 'motor_hand',
            'observation_1', 'observation_2', 'observation_3', 'observation_4'
        ]
        widgets = {
        }

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step', None)
        super().__init__(*args, **kwargs)

        sensory_choices = [
            (0, '0点: 正常な感覚（無麻酔）'),
            (1, '1点: 鈍い（部分的ブロック）'),
            (2, '2点: 完全ブロック'),
            (99, '99点: 評価不能（反応なし）')
        ]
        motor_choices = [
            (0, '0点: 正常な運動機能'),
            (1, '1点: 軽度の筋力低下'),
            (2, '2点: 中等度の筋力低下'),
            (3, '3点: 完全麻痺'),
            (99, '99点: 評価不能（反応なし）')
        ]
        observation_choices = [
            (0, '0: 異常なし'),
            (1, '1: 血腫など異常あり')
        ]

        # 感覚機能：手動で設定
        for field_name in ['sensory_A', 'sensory_B', 'sensory_C', 'sensory_D']:
            self.fields[field_name].widget = forms.RadioSelect(choices=sensory_choices)
            self.fields[field_name].required = False

        # 運動機能：手動で設定
        for field_name in ['motor_elbow', 'motor_hand']:
            self.fields[field_name].widget = forms.RadioSelect(choices=motor_choices)
            self.fields[field_name].required = False

        # 観察：手動で設定
        for field_name in ['observation_1', 'observation_2', 'observation_3', 'observation_4']:
            self.fields[field_name].widget = forms.RadioSelect(choices=observation_choices)
            self.fields[field_name].required = False

        # オペ前（step==0）のときだけ初期値0をセット
        if step == 0 or step == '0':
            for field_name in [
                'sensory_A', 'sensory_B', 'sensory_C', 'sensory_D',
                'motor_elbow', 'motor_hand',
                'observation_1', 'observation_2', 'observation_3', 'observation_4'
            ]:
                self.fields[field_name].initial = 0

                
                
                
# --- AnesthesiaInfo フォーム（麻酔情報入力）---

# ブロックポイント 0〜2mlを0.1刻み
BLOCK_CHOICES = []
for i in range(0, 21):
    value = Decimal(i) * Decimal('0.1')
    value = value.quantize(Decimal('0.0'))  # ★ここを追加して1桁に整える！
    value_str = str(value)
    BLOCK_CHOICES.append((value_str, f"{value} ml"))

# 追加麻酔 0〜50ml


ADDITIONAL_CHOICES = []
for i in range(0, 51):
    value = Decimal(i).quantize(Decimal('0.0'))  # 小数点1桁に整形
    ADDITIONAL_CHOICES.append((str(value), f"{value} ml"))




class AnesthesiaInfoForm(forms.ModelForm):
    block_amount_1 = forms.TypedChoiceField(choices=BLOCK_CHOICES, widget=forms.RadioSelect, coerce=Decimal)
    block_amount_2 = forms.TypedChoiceField(choices=BLOCK_CHOICES, widget=forms.RadioSelect, coerce=Decimal)
    block_amount_3 = forms.TypedChoiceField(choices=BLOCK_CHOICES, widget=forms.RadioSelect, coerce=Decimal)
    block_amount_4 = forms.TypedChoiceField(choices=BLOCK_CHOICES, widget=forms.RadioSelect, coerce=Decimal)
    additional_0_5 = forms.TypedChoiceField(choices=ADDITIONAL_CHOICES, widget=forms.RadioSelect, coerce=Decimal)
    additional_1_0 = forms.TypedChoiceField(choices=ADDITIONAL_CHOICES, widget=forms.RadioSelect, coerce=Decimal)

   # 🆕 drug_typeにもラジオボタン設定を追加！
    drug_type = forms.ChoiceField(choices=[ ('Eなし', 'Eなし'),('E入り', 'E入り')], widget=forms.RadioSelect)


    class Meta:
        model = AnesthesiaInfo
        fields = [
            'drug_type',
            'block_amount_1', 'block_amount_2', 'block_amount_3', 'block_amount_4',
            'additional_0_5', 'additional_1_0',
        ]
        labels = {
            'drug_type': 'ブロック使用薬剤',
            'block_amount_1': '① (ml)',
            'block_amount_2': '② (ml)',
            'block_amount_3': '③ (ml)',
            'block_amount_4': '④ (ml)',
            'additional_0_5': '0.5% 追加局所麻酔 (ml)',
            'additional_1_0': '1% 追加局所麻酔 (ml)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')

        if instance:
            # 小数点1桁に丸めてから文字列にする
            self.fields['block_amount_1'].initial = str(instance.block_amount_1.quantize(Decimal('0.0')))
            self.fields['block_amount_2'].initial = str(instance.block_amount_2.quantize(Decimal('0.0')))
            self.fields['block_amount_3'].initial = str(instance.block_amount_3.quantize(Decimal('0.0')))
            self.fields['block_amount_4'].initial = str(instance.block_amount_4.quantize(Decimal('0.0')))
            
            # 整数に直してから文字列にする
            self.fields['additional_0_5'].initial = str(int(instance.additional_0_5))
            self.fields['additional_1_0'].initial = str(int(instance.additional_1_0))
        else:
            self.fields['block_amount_1'].initial = "0.0"
            self.fields['block_amount_2'].initial = "0.0"
            self.fields['block_amount_3'].initial = "0.0"
            self.fields['block_amount_4'].initial = "0.0"
            self.fields['additional_0_5'].initial = "0"
            self.fields['additional_1_0'].initial = "0"
