from pyspark import SparkContext

sc = SparkContext(appName="WordCount")

text = sc.textFile("hdfs://10.0.1.64:9000/gutenberg/*.txt")

counts = text.flatMap(lambda line: line.split()) \
             .map(lambda word: (word, 1)) \
             .reduceByKey(lambda a, b: a + b)

counts.saveAsTextFile(
    "hdfs://10.0.1.64:9000/output_spark_wordcount_2node"
)

sc.stop()