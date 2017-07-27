import sys
from operator import add
from pyspark import SparkContext

if __name__ == "__main__":
    sc = SparkContext(appName="PythonWordCount")
    lines = sc.textFile("words.txt")
    print(lines.count())
    print(lines.first())
    counts = lines.flatMap(lambda x: x.split(' ')) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(add)
    output = counts.collect()
    for (word, count) in output:
        print("%s: %i" % (word, count))
    lines.filter(lambda line: "hadoop" in line)
    print(lines.first())

    sc.stop()
