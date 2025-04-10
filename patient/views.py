from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import PatientIDForm
from datetime import datetime
from .models import Patient, Operation
from django.shortcuts import render
from .forms import OperationForm
from django.utils import timezone
from datetime import timedelta
from .forms import EvaluationForm
from .models import Evaluation
from django.shortcuts import get_object_or_404
from .models import Operation, AnesthesiaInfo
from .forms import AnesthesiaInfoForm
from django.http import HttpResponseServerError

from decimal import Decimal


def test_server_error(request):
    return HttpResponseServerError()


@login_required
def dashboard_view(request):
    today = timezone.now().date()
    four_days_ago = today - timedelta(days=4)

    # 直近4日以内の手術を取得（降順）
    recent_operations = Operation.objects.filter(date__date__gte=four_days_ago).order_by('-date')

    return render(request, 'patient/dashboard.html', {
        'operations': recent_operations
    })

@login_required
def wizard_view(request):
    return HttpResponse("これは wizard ページです。（ログイン済み）")

@login_required
def patient_id_input(request):
    if request.method == 'POST':
        form = PatientIDForm(request.POST)
        if form.is_valid():
            patient_id = form.cleaned_data['patient_id']
            return redirect('latest_surgery', patient_id=patient_id)
    else:
        form = PatientIDForm()
    return render(request, 'patient/patient_id_input.html', {'form': form})



@login_required
def latest_surgery_view(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
        latest_op = Operation.objects.filter(patient=patient).order_by('-date').first()
        if latest_op:
            return render(request, 'patient/surgery_with_date.html', {
                'patient_id': patient.id,
                'date': latest_op.date
            })
        else:
            return render(request, 'patient/surgery_none.html', {
                'patient_id': patient.id
            })
    except Patient.DoesNotExist:
        return HttpResponse("患者が見つかりませんでした。")


@login_required
def add_operation(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return HttpResponse("患者が見つかりませんでした。")

    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.patient = patient
            operation.save()
          
            # ✅ OP前（step=0）の評価フォームへ遷移
            return redirect('evaluation_step', operation_id=operation.id, step=0)
            return redirect('evaluation_step', operation_id=operation.id, step=int(0))

    else:            

        form = OperationForm()

    return render(request, 'patient/add_operation.html', {
        'form': form,
        'patient': patient
    })


@login_required
def add_new_operation_view(request):
    if request.method == 'POST':
        form = PatientIDForm(request.POST)
        if form.is_valid():
            patient = form.save()
            return redirect('add_operation', patient_id=patient.id)
    else:
        form = PatientIDForm()

    return render(request, 'patient/add_patient.html', {  # ← 入力フォームだけの画面
        'form': form,
    })

@login_required
def evaluation_step_view(request, operation_id, step):
    operation = get_object_or_404(Operation, id=operation_id)
    anesthesia = AnesthesiaInfo.objects.filter(operation=operation).first()
    timepoint = str(step)
    timepoint_label = dict(Evaluation.TIMEPOINT_CHOICES).get(timepoint, timepoint)

    # ✅ 全stepのevaluationを取得して、過去の麻酔覚醒状況をチェック
    past_evaluations = Evaluation.objects.filter(operation=operation).order_by('timepoint')

    awakening_none = False
    awakening_recorded = False
    awakening_value = None

    for ev in past_evaluations:
        if ev.awakening_time == 'none':
            awakening_none = True
        elif ev.awakening_time:
            # 最初に時刻記録（痛みあり）を見つけたらそれを使う
            awakening_recorded = True
            awakening_value = ev.awakening_time
            awakening_none = False  # 時刻を記録したら、痛みなし状態は解除
            break  # もうそれ以降は見る必要なし


    # ✅ 麻酔直後step=1の created_atを取得
    anesthesia_end_evaluation = Evaluation.objects.filter(operation=operation, timepoint="1").first()
    anesthesia_end_time = anesthesia_end_evaluation.created_at if anesthesia_end_evaluation else None

    if request.method == 'POST':
        print("=== POSTきた！===")
        form = EvaluationForm(request.POST, step=step, anesthesia_end_time=anesthesia_end_time)

        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.operation = operation
            evaluation.timepoint = timepoint

            # 🔥 awakening_time を手動で上書き！（POSTされた値）
            evaluation.awakening_time = form.cleaned_data.get('awakening_time')

            evaluation.save()

            print("=== 保存完了！===")
            print(f"awakening_time: {evaluation.awakening_time}")

            # ✅ 保存できたらすぐリダイレクト（重要）
            if int(step) + 1 < len(Evaluation.TIMEPOINT_CHOICES):
                if int(step) == 0:
                    return redirect('add_anesthesia_info', operation_id=operation.id)
                else:
                    return redirect('evaluation_step', operation_id=operation.id, step=int(step) + 1)
            else:
                return redirect('evaluation_summary', operation_id=operation.id)

        else:
            # ❗ フォームエラーのとき、ここでエラー内容を表示
            print("=== form.errors ===")
            print(form.errors)

    else:
        # ✅ GETリクエスト（ページ初期表示）
        form = EvaluationForm(step=step, anesthesia_end_time=anesthesia_end_time)

    evaluations = Evaluation.objects.filter(operation=operation).order_by('timepoint')

    performed_points = {
        'performed_point_1': anesthesia.block_amount_1 > 0 if anesthesia else False,
        'performed_point_2': anesthesia.block_amount_2 > 0 if anesthesia else False,
        'performed_point_3': anesthesia.block_amount_3 > 0 if anesthesia else False,
        'performed_point_4': anesthesia.block_amount_4 > 0 if anesthesia else False,
    }

    return render(request, 'patient/evaluation_form.html', {
        'form': form,
        'step': step,
        'timepoint': timepoint,
        'timepoint_label': timepoint_label,
        'evaluations': evaluations,
        'operation': operation,
        'anesthesia': anesthesia,
        **performed_points,
        'awakening_recorded': awakening_recorded,
        'awakening_value': awakening_value,
        'awakening_none': awakening_none,
    })





@login_required
def add_anesthesia_info(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)

    if request.method == 'POST':
        form = AnesthesiaInfoForm(request.POST)
        if form.is_valid():
            anesthesia = form.save(commit=False)
            anesthesia.operation = operation
            anesthesia.save()
            return redirect('evaluation_step', operation_id=operation.id, step=1)
        else:
            # 🛑 ここを追加 🛑
            print("=== フォームエラー内容 ===")
           
    else:
        form = AnesthesiaInfoForm(initial={
            'drug_type': 'Eなし',
            'block_amount_1': "0.0",
            'block_amount_2': "0.0",
            'block_amount_3': "0.0",
            'block_amount_4': "0.0",
            'additional_0_5': "0.0",
            'additional_1_0': "0.0",
        })

    return render(request, 'patient/anesthesia_form.html', {
        'form': form,
        'operation': operation,
    })


@login_required
def start_evaluation_view(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    existing_steps = Evaluation.objects.filter(operation=operation).values_list('timepoint', flat=True)

    for step in range(len(Evaluation.TIMEPOINT_CHOICES)):
        if str(step) not in existing_steps:
            return redirect('evaluation_step', operation_id=operation.id, step=step)

    # 全てのstepが記録済みなら summary に行く！
    return redirect('evaluation_summary', operation_id=operation.id)

    
@login_required
def evaluation_summary_view(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    evaluations = Evaluation.objects.filter(operation=operation).order_by('timepoint')
    anesthesia = AnesthesiaInfo.objects.filter(operation=operation).first()

    return render(request, 'patient/evaluation_summary.html', {
        'operation': operation,
        'evaluations': evaluations,
        'anesthesia': anesthesia,
    })



@login_required
def edit_operation(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    
    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            form.save()
            return redirect('evaluation_summary', operation_id=operation.id)
    else:
        form = OperationForm(instance=operation)

    return render(request, 'patient/edit_operation.html', {
        'form': form,
        'operation': operation
    })




@login_required
def edit_anesthesia_info(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    anesthesia = get_object_or_404(AnesthesiaInfo, operation=operation)

    if request.method == 'POST':
        form = AnesthesiaInfoForm(request.POST, instance=anesthesia)
        if form.is_valid():
            form.save()
            return redirect('evaluation_summary', operation_id=operation.id)
        else:
            print("=== フォームエラー ===")
            print(form.errors)
    else:
        form = AnesthesiaInfoForm(instance=anesthesia)
        # 🛠ここ追加！！（初期値チェック）
        print("=== 初期フォームの中身チェック ===")
        print("block_amount_1:", form.initial.get('block_amount_1'))
        print("additional_0_5:", form.initial.get('additional_0_5'))

    return render(request, 'patient/edit_anesthesia.html', {
        'form': form,
        'operation': operation
    })

    
    
@login_required
def edit_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    operation = evaluation.operation  # 戻る用に使います

    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('evaluation_summary', operation_id=operation.id)
    else:
        form = EvaluationForm(instance=evaluation)

    return render(request, 'patient/edit_evaluation.html', {
        'form': form,
        'evaluation': evaluation,
        'timepoint_label': evaluation.get_timepoint_display(),
    })
