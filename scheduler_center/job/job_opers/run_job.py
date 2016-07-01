

from http_request_job import HttpRequestJob
from shell_job import ShellJob

def run_script(params={}):
    
    RUN_SCRIPT_MAP = {
        'url': HttpRequestJob,
        'shell_path': ShellJob,
    }
    
    params_key = [item for item in TRIGGER_MAP if item in params]
    run_class = RUN_SCRIPT_MAP[params_key]
    obj = run_class(params)
    return obj.run()