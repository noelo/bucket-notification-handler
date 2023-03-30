from flask import Flask, request, make_response
import json
import uuid
from cloudevents.http import CloudEvent, from_http
from cloudevents.conversion import to_binary
from kfp import kfp

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_event():
    app.logger.info(request.data)
    payload = request.get_json(force=True)
    event = from_http(request.headers, request.get_data())
  
    trigger = event['type']
    obj = event['subject']
    src = event['source']
    print(trigger,obj,src)

    response = make_response({
        "fileTrigger": obj 
    })
    response.headers["Ce-Id"] = str(uuid.uuid4())
    response.headers["Ce-specversion"] = "0.3"
    response.headers["Ce-Source"] = "minio/trigger/kubeflowtrigger"
    response.headers["Ce-Type"] = "com.redhat.odf.trigger"
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

