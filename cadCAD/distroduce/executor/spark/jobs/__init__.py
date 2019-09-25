from cadCAD.distroduce.configuration.kakfa import configure_producer
from pyspark.context import SparkContext

ascii_art = r'''
   ___   _      __        _  __         __           __
  / _ \ (_)___ / /_ ____ (_)/ /  __ __ / /_ ___  ___/ /
 / // // /(_-</ __// __// // _ \/ // // __// -_)/ _  / 
/____//_//___/\__//_/ _/_//_.__/\_,_/ \__/ \__/ \_,_/  
  / _ \ ____ ___  ___/ /__ __ ____ ___                 
 / ___// __// _ \/ _  // // // __// -_)                
/_/   /_/   \___/\_,_/ \_,_/ \__/ \__/                 
by Joshua E. Jodesty   
'''

def distributed_produce(
        sc: SparkContext,
        spark_run,
        sim_time,
        sim_runs,
        rdd_parts,
        parameterized_message,
        prod_config
):
    print(ascii_art)
    message_counts = [sim_time] * sim_runs
    msg_rdd = sc.parallelize(message_counts).repartition(rdd_parts)
    parts = msg_rdd.getNumPartitions()
    print()
    print(f"RDD_{spark_run} - Partitions: {parts}")
    print()

    produce = configure_producer(parameterized_message, prod_config)
    return msg_rdd.map(produce).collect()
