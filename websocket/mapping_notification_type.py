from . import frontend_setting
mapping = {
    "new_sample_form":{
        "model_name":"SampleForm",
        "from_user":['admin','user'],
        "to_users":['admin','user'],
        "admin_message":"A new sample ({sample_id}) has been requested for testing by user ({username})",
        "path":frontend_setting.smu_sample_request_details,
        "user_message":"Your sample ({refrence_number}) has been submitted successfully",
    },
    "assigned_supervisor":{
        "model_name":"SuperVisorSampleForm",
        "from_user":['admin','smu'],
        "to_users":['supervisor'],
        "path":frontend_setting.supervisor_sample_request_details,
        "admin_message":"New sample ({sample_lab_id}) has been assigned",
        "user_message":"None",
    },
    "assigned_analyst":{
        "model_name":"SampleFormHasParameter",
        "from_user":['supervisor'],
        "to_users":['analyst'],
        "path":frontend_setting.analyst_sample_request_details,
        "admin_message":"A new Sample ({sample_lab_id}) has been assigned for testing",
        "user_message":"None",
    },
    "assigned_verifier":{
        "model_name":"SampleFormVerifier",
        "from_user":['supervisor'],
        "to_users":['verifier'],
        "path":frontend_setting.verifier_sample_request_details,
        "admin_message":"A sample report of  ({sample_lab_id}) has been submitted for verification. Please Verify",
        "user_message":"None",
    },
    "assigned_admin":{
        "model_name":"SampleFormVerifier",
        "from_user":['verifier'],
        "to_users":['user','smu','admin','supervisor','analyst'],
        "path":frontend_setting.admin_sample_request_details,
        "admin_message":"A sample report of  ({sample_lab_id}) has been submitted for approve",
        "user_message":"this sample form verified",
    },
    "approved_sample_form":{
        "model_name":"SampleFormVerifier",
        "from_user":['verifier'],
        "to_users":['user','smu','admin','supervisor','analyst'],
        "path":frontend_setting.sample_request,
        "admin_message":"A sample report of ({sample_lab_id}) has been completed",
        "user_message":"this sample form verified",
    }

}
