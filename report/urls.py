from . import views,preeti_to_unicode,preeti_to_pdf,dashboard
from . import final_report,track,status,assigned_sample_for_smu_superadmin, additional_details

from django.urls import path, include


urlpatterns = [   
    path('sample-form-has-assigned-analyst/', views.SampleFormHasAnalystAPIView.as_view()),
    path('sample-form-has-assigned-analyst-final-report/', views.SampleFormHasAnalystFinalReportAPIView.as_view()),
    path('detail-sample-form-has-assigned-analyst-final-report/<int:supervisor_table_id>/', views.DetailSampleFormHasAnalystFinalReportAPIView.as_view()),

    path('sample-form-has-parameter-has-assigned-analyst/<int:sample_form_id>/', views.ParameterHasAssignedAnalyst.as_view()), #both are same

    path('detail-sample-form-has-parameter-has-assigned-analyst/<int:sample_form_id>/', views.DetailParameterHasAssignedAnalyst.as_view()), #both are same
    path('detail-sample-form-has-parameter-has-assigned-analyst/<str:sample_form_id>/', views.DetailParameterHasAssignedAnalyst.as_view()), #both are same

    path('completed-sample-form-has-assigned-verifier/', views.CompletedSampleFormHasVerifierAPIView.as_view()),
    path('sample-form-to-approved-by-admin/', views.notApprovedSampleFormHasAdminAPIView.as_view()),
    # path('completed-sample-form-has-assigned-verifier-check-exists/<int:sample_form_id>/', supervisor.getStatusOfVerifierSampleForm.as_view()),

    path('final-report-sample-form/', final_report.FinalSampleFormHasVerifiedAPIView.as_view()), #accessable to all superadmin,user

    path('sample-form-assigned-for-smu-superadmin/', assigned_sample_for_smu_superadmin.FinalSampleFormHasVerifiedAPIView.as_view()),

    path('track-report-sample-form/', track.TrackSampleFormAPIView.as_view()),

    path('status/<str:url>/', status.GetStatus.as_view()),
    # path('completed-sample-form-has-assigned-verifier-check-exists/<int:sample_form_id>/', supervisor.getStatusOfVerifierSampleForm.as_view()),

    path('get-report/<str:report_name>/<str:report_type>/<str:report_lang>/', views.ReportDownload.as_view()),
    path('get-single-report/<str:report_name>/<str:report_type>/<str:report_lang>/<str:id>/<int:role>/', views.ReportDownload.as_view()),

    path('get-report-raw-data/<str:download_print>/<str:report_lang>/<str:sample_form_has_parameter>/', views.rawDataReportDownload.as_view()),
    path('get-report-raw-data-api/<str:download_print>/<str:report_lang>/<str:sample_form_has_parameter>/', views.rawDataReportApi.as_view()),
    
    path('preeti-to-unicode', preeti_to_unicode.PreetiToUniCode.as_view()),
    path('unicode-to-preeti', preeti_to_unicode.UnicodeToPreeti.as_view()),
    path('preeti-to-pdf', preeti_to_pdf.PreetiToPdf,name="Preeti-to-pdf"),
    path('final-report', views.FinalReportPdf,name="FinalReport"),

    path('dashboard-report/', dashboard.reportStatus.as_view()),
    path('analyst-report-download/', dashboard.AnalystProgressReport.as_view()),
    path('supervisor-report-download/', dashboard.SuperVisorProgressReport.as_view()),

    path('sample-form-track-by-analyst/<str:sample_form_id>/', views.SampleFormTrackbyAnalyst.as_view()),


    path('final-report-in-nepali/<str:sample_form_id>/<int:role_id>/', views.FinalReportNepali.as_view()), #both are same

    path('get-sample-form-contacts-for-industry/', additional_details.AdditionalDetailSampleForm.as_view()), #by sagar 
 
]