from django.db import models
from django.utils import timezone

class Patient(models.Model):
    patient_code = models.IntegerField()  # ← 明示的に手動入力IDに変更！
    
    def __str__(self):
        return f"ID: {self.patient_code}"

class Operation(models.Model):
    GENDER_CHOICES = [
        ('M', '男性'),
        ('F', '女性'),
    ]

    PROCEDURE_CHOICES = [
        ('AVF', 'AVF'),
        ('AVG', 'AVG'),
        ('PTA', 'PTA'),
        ('TPA', '血栓除去PTA'),
        ('OPTPA', '開創血栓除去PTA'),
        ('ETC', 'その他'),
    ]

    SURGERY_TYPE_CHOICES = [
        ('P', 'プライマリー'),
        ('R', 'ノンプライマリー'),
    ]
    
    SURGEON_CHOICES = [
        ('HB', 'HB'),
        ('NG', 'NG'),
        ('ST', 'ST'),
        ('KB', 'KB'),
        ('ETC', 'ETC'),
    ]
    
    patient = models.ForeignKey(
        Patient,
        related_name='operations',
        on_delete=models.CASCADE,
        null=True,  # ← 一時的に追加
        default=1  ) # ← 一時的にデフォルト患者IDを指定（例：ID=1の患者がいれば）


    date = models.DateTimeField(verbose_name="手術日時", default=timezone.now)
    age = models.PositiveIntegerField(verbose_name="年齢", default=0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性別", default='M')
    height = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="身長(cm)", default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="体重(kg)", default=0)
    procedure = models.CharField(max_length=10, choices=PROCEDURE_CHOICES, verbose_name="術式", default='AVF')
    surgery_type = models.CharField(max_length=1, choices=SURGERY_TYPE_CHOICES, verbose_name="手術の種類", default='P')
    surgeon = models.CharField(max_length=100, choices=SURGEON_CHOICES, verbose_name="術者", default='HB')
    def __str__(self):
        return f"患者ID: {self.patient.id} の手術 ({self.date})"
    
class Evaluation(models.Model):
    
    TIMEPOINT_CHOICES = [
    ('0', 'オペ前'),
    ('1', '麻酔直後'),
    ('2', 'オペ直後'),
    ('3', '帰室時'),
    ('4', '時系列⑤'),
    ('5', '時系列⑥'),
    ('6', '時系列⑦'),
    ('7', '時系列⑧'),
]
    
    SENSORY_CHOICES = [
    (0, '0点: 正常な感覚（無麻酔）'), 
    (1, '1点: 冷感を感じるが、健側（または正常部）に比べて鈍い（部分的ブロック）'), 
    (2, '2点: 完全な感覚遮断（完全ブロック）'),
    (9, '9点: 評価不能（反応なし）')
]

    MOTOR_CHOICES = [
        (0, '0点: 正常な運動機能'), 
        (1, '1点: 軽度の筋力低下（可動域制限なし）'),
        (2, '2点: 顕著な筋力低下（可動域制限あり）'), 
        (3, '3点: 完全麻痺（随意運動なし）'),
        (9, '9点: 評価不能（反応なし）')
    ]
    
    OBS_CHOICES = [
        (0, '0:異常なし'), 
        (1, '1:血腫、腫脹、赤みなど、何らかの異常あり'),
    ]

    
    operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name='evaluations')
    
    timepoint = models.CharField(max_length=1, choices=TIMEPOINT_CHOICES)

    # 感覚機能評価（0〜2）

    sensory_A = models.IntegerField(choices=SENSORY_CHOICES, null=True, blank=True)
    sensory_B = models.IntegerField(choices=SENSORY_CHOICES, null=True, blank=True)
    sensory_C = models.IntegerField(choices=SENSORY_CHOICES, null=True, blank=True)
    sensory_D = models.IntegerField(choices=SENSORY_CHOICES, null=True, blank=True)

    # 運動機能評価（0〜3）
    motor_elbow = models.IntegerField(choices=MOTOR_CHOICES, null=True, blank=True)
    motor_hand = models.IntegerField(choices=MOTOR_CHOICES, null=True, blank=True)

    # ブロックポイント観察（〇 or X）
    observation_1 = models.IntegerField(choices=OBS_CHOICES, null=True, blank=True)
    observation_2 = models.IntegerField(choices=OBS_CHOICES, null=True, blank=True)
    observation_3 = models.IntegerField(choices=OBS_CHOICES, null=True, blank=True)
    observation_4 = models.IntegerField(choices=OBS_CHOICES, null=True, blank=True)

    signer = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.operation} - {self.timepoint}"

class AnesthesiaInfo(models.Model):
    operation = models.OneToOneField('Operation', on_delete=models.CASCADE)

    # ブロック使用薬剤（E入 or Eなし など）
    drug_type = models.CharField(max_length=20, choices=[('E入', 'E入'), ('Eなし', 'Eなし')])

    # 各ブロックポイントの使用量（ml）
    block_amount_1 = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, default=0)
    block_amount_2 = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, default=0)
    block_amount_3 = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, default=0)
    block_amount_4 = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, default=0)

    # 追加局所麻酔使用量（Eなし）
    additional_0_5 = models.DecimalField("0.5% 使用量 (ml)", max_digits=4, decimal_places=1, null=True, blank=True, default=0)
    additional_1_0 = models.DecimalField("1% 使用量 (ml)", max_digits=4, decimal_places=1, null=True, blank=True, default=0)

    def __str__(self):
        return f"麻酔情報 (Operation ID: {self.operation.id})"