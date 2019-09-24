from functools import reduce
from datetime import timedelta
from pprint import pprint
import time
from pathos.multiprocessing import ThreadPool as TPool

from cadCAD.utils import flatten
from cadCAD.distroduce.executor import distributed_produce
from distributed_produce.examples.event_bench.spark.session import spark_context as sc


def main(sc, spark_runs, rdd_parts, sim_time, sim_runs, parameterized_message):
    publish_times, spark_job_times = [], []
    prod_config = {'bootstrap_servers': 'localhost:9092', 'acks': 0}
    exec_spark_job = lambda run: distributed_produce(
        sc, run, sim_time, sim_runs, rdd_parts, parameterized_message, prod_config
    )

    job = 0
    with TPool(spark_runs) as t:
        start_time = time.time()
        publish_times.append(t.map(exec_spark_job, range(spark_runs)))
        spark_job_times.append({'job_num': job, 'job_time': time.time() - start_time})
        job += 1

    publish_times = sorted(flatten(list(reduce(lambda a, b: a + b, publish_times))), key=lambda x: x[0])
    # publish_start_sec = list(set([time[0].second for time in publish_times]))
    publish_send_secs = [time[1] for time in publish_times]
    publish_send_dts = [time[0] for time in publish_times]

    send_time = publish_send_dts[-1] - publish_send_dts[0] + timedelta(microseconds=1000000 * publish_send_secs[-1])
    sent_messages = sim_time * sim_runs
    print(f"Spark Job Times: ")
    pprint(spark_job_times)
    print()
    print(f"Messages per Second: {float(sent_messages) / (float(send_time.seconds) + float(send_time.microseconds/1000000))}")
    print(f"Sent Messages: {sent_messages}")
    print(f"Send Time (Seconds): {send_time}")
    print(f"Avg. Send Loop Duration: {sum(publish_send_secs)/(spark_runs*25)}")


if __name__ == "__main__":
    sc.setLogLevel("ERROR")
    spark_runs = 1
    sim_time = 400
    sim_runs = 25
    rdd_parts = 8

    def msg(t):
        return str(f"*****************message_{t}").encode('utf-8')

    main(sc, spark_runs, rdd_parts, sim_time, sim_runs, msg)

    # prod_config = {'bootstrap_servers': 'localhost:9092', 'acks': 0, 'max_in_flight_requests_per_connection': 1, 'batch_size': 0, 'retries': 0}
    # print(f"Second Starts: {len(publish_start_sec)}")
    # print(f"Start Seconds: {publish_start_sec}")
    # pprint(publish_send_secs)
    # pprint(publish_times)
