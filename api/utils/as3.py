import boto3
from boto3.s3.transfer import S3Transfer
import base64
import time
import os

def get_url_pre_signed(key):
    """
    Recupera a url da foto assinada
    """
    bucket = 'thefarma-bkt'
    s3 = boto3.client('s3', region_name='us-west-2',
                                   aws_access_key_id = 'AKIAIETYIAFF74EPJ6MA',
                                   aws_secret_access_key='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')
    try:
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': bucket,
                'Key': key,
            }
        )
    except Exception as e:
        print(e)
        return None

    return str(url)


def download_file(key_nome):
    #instancia
    transfer = S3Transfer(boto3.client('s3', region_name='us-west-2',
                                   aws_access_key_id = 'AKIAIETYIAFF74EPJ6MA',
                                   aws_secret_access_key='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'))
    bucket = 'thefarma-bkt' #nome do bucket
    #verifica se o caminho existe
    if not os.path.exists('/arquivos_atualizacao/'):
        os.makedirs('/arquivos_atualizacao/')
    
    #nome unico
    filename = '/arquivos_atualizacao/' + str(time.time()) + '.txt'

    transfer.download_file(bucket, key_nome, filename)

    return filename