from flask import Flask, request, make_response
import json
import uuid
from cloudevents.http import CloudEvent, from_http
from cloudevents.conversion import to_binary
import kfp
import os
import time

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_event():
    app.logger.info(request.data)
    # payload = request.get_json(force=True)
    event = from_http(request.headers, request.get_data())
    trigger = event['type']
    fileobj = event['subject']
    srcbucket = event['source']
    print(trigger,fileobj,srcbucket)
    kfp_api = os.environ.get('KFP_API')
    kfp_name = os.environ.get('KFP_NAME')
    if trigger == 'com.amazonaws.ObjectCreated:Put':
        kubeflow_handler(kfp_api,kfp_name,fileobj,srcbucket)

    response = make_response({
        "fileTrigger": fileobj 
    })
    response.headers["Ce-Id"] = str(uuid.uuid4())
    response.headers["Ce-specversion"] = "0.3"
    response.headers["Ce-Source"] = "minio/trigger/kubeflowtrigger"
    response.headers["Ce-Type"] = "com.redhat.odf.trigger"
    return response

def kubeflow_handler(kfp_host:str, kfp_name:str,file_obj:str, src_bucket:str)->None:
    print('Connecting to kubeflow API.....',kfp_host)
    client = kfp.Client(host=kfp_host)
    print('Connecting to kubeflow API.....connected')

    pipline_id  = client.get_pipeline_id(kfp_name)
    if pipline_id is None:
        print("No pipeline found with name ",kfp_name)
    else:
        exp_obj = client.create_experiment("BatteryMonitoringExperiment"+str(time.asctime()),"Battery monitoring experiment")
        params_dict = dict(file_obj= file_obj, src_bucket = src_bucket)
        run = client.run_pipeline(exp_obj.id,"battery monitor run", pipeline_id = pipline_id,params=params_dict)
        print("Pipleline Run submitted ",run)    
    print('Connecting to kubeflow API.....finish')
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

