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
    anesthesia = AnesthesiaInfo.objects.filter(operation=operation).first()  # ✅ 麻酔情報取得
    timepoint = str(step)
    timepoint_label = dict(Evaluation.TIMEPOINT_CHOICES).get(timepoint, timepoint)  # ✅ 追加

    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.operation = operation
            evaluation.timepoint = timepoint
            evaluation.save()
            if step + 1 < len(Evaluation.TIMEPOINT_CHOICES):
                if step == 0:
                    return redirect('add_anesthesia_info', operation_id=operation.id)
                else:
                    return redirect('evaluation_step', operation_id=operation.id, step=step + 1)
            else:
                return redirect('evaluation_summary', operation_id=operation.id)

    else:
        form = EvaluationForm()

    evaluations = Evaluation.objects.filter(operation=operation).order_by('timepoint')

    return render(request, 'patient/evaluation_form.html', {
        'form': form,
        'step': step,
        'timepoint': timepoint,
        'timepoint_label': timepoint_label,  # ← ここを追加！
        'evaluations': evaluations,
        'operation': operation,        # ✅ 手術情報
        'anesthesia': anesthesia,      # ✅ 麻酔情報
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
        # フォーム初期値の設定（数字や文字など）
        form = AnesthesiaInfoForm(initial={
            'drug_type': 'E入',
            'block_amount_1': 0,
            'block_amount_2': 0,
            'block_amount_3': 0,
            'block_amount_4': 0,
            'additional_0_5': 0,
            'additional_1_0': 0,
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
    
    try:
        anesthesia = AnesthesiaInfo.objects.get(operation=operation)
    except AnesthesiaInfo.DoesNotExist:
        anesthesia = None
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
        form = AnesthesiaInfoForm(instance=anesthesia)

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
