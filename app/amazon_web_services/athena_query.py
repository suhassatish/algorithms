import boto3
from pyathenajdbc import connect
from time import sleep


def query_from_athena_using_jdbc():
    conn = connect(s3_staging_dir='s3://krux-attribute-metrics-staging/stream-processor/pixel_attributes_stream/',
                   region_name='us-east-1',
                   driver_path='/home/vagrant/.virtualenvs/pycharm/lib/python2.7/site-packages/pyathenajdbc/AthenaJDBC41-1.1.0.jar')

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                select
                  process_time
                  ,sum(views)
                from spectrum_db.pixel_attributes_stream
                where organization = 'c819846f-b6e4-4ef4-b357-28399862b473'
                  and process_time > '2017-10-30_18:55'
                group by process_time
                order by 1 desc
                limit 10
            """)
            print(cursor.description)
            print(cursor.fetchall())
    finally:
        conn.close()


def query_from_athena_using_boto3():
    client = boto3.client('athena')  # requires boto3 version 1.4.7 for Athena
    sql = """
        select
          process_time
          ,sum(views)
        from spectrum_db.pixel_attributes_stream
        where organization = 'c819846f-b6e4-4ef4-b357-28399862b473'
          and process_time > '2017-10-29_18:55'
        group by process_time
        order by 1 desc
        limit 10
    """

    response = client.start_query_execution(
        QueryString=sql,
        # ClientRequestToken='string',
        QueryExecutionContext={
            'Database': 'krux-reports-dreamforce.rs.krxd.net'
        },
        ResultConfiguration={
            'OutputLocation': 's3://krux-tmp/suhas'
        }
    )
    q_exe_id = response['QueryExecutionId']
    print(q_exe_id)

    sleep(15)   # wait 15s for query execution to complete to avoid error "(InvalidRequestException) when calling the
    #  GetQueryResults operation: Query has not yet finished. Current state: RUNNING"

    result_set = client.get_query_results(QueryExecutionId=q_exe_id)
    print(result_set)
    """
{'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
   'content-length': '930',
   'content-type': 'application/x-amz-json-1.1',
   'date': 'Mon, 30 Oct 2017 17:28:59 GMT',
   'x-amzn-requestid': 'd0835a5b-bd97-11e7-b8c6-2734d76534d7'},
  'HTTPStatusCode': 200,
  'RequestId': 'd0835a5b-bd97-11e7-b8c6-2734d76534d7',
  'RetryAttempts': 0},
 u'ResultSet': {u'ResultSetMetadata': {u'ColumnInfo': [{u'CaseSensitive': True,
     u'CatalogName': u'hive',
     u'Label': u'process_time',
     u'Name': u'process_time',
     u'Nullable': u'UNKNOWN',
     u'Precision': 20,
     u'Scale': 0,
     u'SchemaName': u'',
     u'TableName': u'',
     u'Type': u'varchar'},
    {u'CaseSensitive': False,
     u'CatalogName': u'hive',
     u'Label': u'_col1',
     u'Name': u'_col1',
     u'Nullable': u'UNKNOWN',
     u'Precision': 19,
     u'Scale': 0,
     u'SchemaName': u'',
     u'TableName': u'',
     u'Type': u'bigint'}]},
  u'Rows': [{u'Data': [{u'VarCharValue': u'process_time'},
     {u'VarCharValue': u'_col1'}]}]}}
    """
    print(result_set['ResultSet']['Rows'])
    """
    [{u'Data': [{u'VarCharValue': u'process_time'}, {u'VarCharValue': u'_col1'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-45'}, {u'VarCharValue': u'553681'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-44'}, {u'VarCharValue': u'473976'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-43'}, {u'VarCharValue': u'580097'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-42'}, {u'VarCharValue': u'584120'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-41'}, {u'VarCharValue': u'582184'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-40'}, {u'VarCharValue': u'575626'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-39'}, {u'VarCharValue': u'581010'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-38'}, {u'VarCharValue': u'535724'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-37'}, {u'VarCharValue': u'407761'}]},
 {u'Data': [{u'VarCharValue': u'2017-10-30_17-36'}, {u'VarCharValue': u'307596'}]}]
    """

if __name__ == '__main__':
    query_from_athena_using_boto3()
