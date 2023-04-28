import boto3

s3_target = boto3.resource('s3',
    endpoint_url='http://rook-ceph-rgw-ceph-object-......',
    aws_access_key_id='.......',
    aws_secret_access_key='......',
    aws_session_token=None,
    config=boto3.session.Config(signature_version='s3v4'),
    verify=False
)

bucket = s3_target.Bucket('noc-test')
# bucket = s3_target.Bucket('ceph-bkt')
for obj in bucket.objects.all():
    print(obj.key)

s3_target.meta.client.upload_file("/home/noelo/Documents/RHODS/t8.shakespeare.txt", "noc-test","records2.json")
# s3_target.meta.client.upload_file("/home/noelo/Documents/RHODS/t8.shakespeare.txt", "ceph-bkt","records2.json")