FROM registry.access.redhat.com/ubi8/python-39:1-97
USER 0
COPY . /app
RUN chown -R 1001:0 ./
USER 1001
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
ENTRYPOINT [ "python" ]
CMD [ "kubeflow_trigger.py" ]