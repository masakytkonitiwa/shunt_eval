from django.urls import path
from . import views

urlpatterns = [
    # --- トップ・ログイン後の入口 ---
    path('', views.patient_id_input, name='patient_id_input'),  # トップページ
    path('wizard/', views.wizard_view, name='wizard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # --- 新規登録・手術登録 ---
    path('operation/new/', views.add_new_operation_view, name='add_new_operation'),
    path('operation/add/<int:patient_id>/', views.add_operation, name='add_operation'),
    path('operation/<int:operation_id>/anesthesia/', views.add_anesthesia_info, name='add_anesthesia_info'),

    # --- 評価フォーム ---
    path('evaluate/<int:operation_id>/<int:step>/', views.evaluation_step_view, name='evaluation_step'),
    path('operation/<int:operation_id>/start/', views.start_evaluation_view, name='start_evaluation'),
    path('operation/<int:operation_id>/summary/', views.evaluation_summary_view, name='evaluation_summary'),


    # --- 手術履歴確認 ---
    path('surgery/<int:patient_id>/', views.latest_surgery_view, name='latest_surgery'),
  
    # --- 編集 ---  
    path('operation/<int:operation_id>/anesthesia/edit/', views.edit_anesthesia_info, name='edit_anesthesia_info'),
    path('operation/<int:operation_id>/edit/', views.edit_operation, name='edit_operation'),
    path('evaluation/<int:evaluation_id>/edit/', views.edit_evaluation, name='edit_evaluation'),




    path('test500/', views.test_server_error, name='test_server_error'),


]
