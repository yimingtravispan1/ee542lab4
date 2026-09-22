# EE 542 - Lab4

## 4. Setting up Spark on AWS EC2

Apache Spark 3.5.1 was installed on the EC2 instance. The Spark environment variables were configured in `.bashrc`:

```bash
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin
```

The installation was verified using:

```bash
spark-submit --version
```

Spark started successfully with Java 11.

Master:

![](images/Master_spark_installed.png)

Worker:

![](images/Master_spark_installed.png)

---

## 5. Spark with Python (PySpark)

Three PySpark programs were implemented using the Gutenberg text files.

### 5.1 Word Count

`spark_wordcount.py` counts the frequency of each word using `flatMap`, `map`, and `reduceByKey`.

```bash
spark-submit spark_wordcount.py
```

The program successfully processed the input files and generated the word-count output.

**Execution time:** 2.33 s

![](images/Word_Count_Time.png)

### 5.2 Character Frequency

`spark_charcount.py` counts the frequency of each character in the Gutenberg dataset.

```bash
spark-submit spark_charcount.py
```

The output contains each character and its total frequency.

**Execution time:** 2.64 s

![](images/Character_Count_Time.png)

### 5.3 Minimum and Maximum Word Count

`spark_minmax.py` calculates the least and most frequently occurring words.

```bash
spark-submit spark_minmax.py
```

Result:

```text
MIN: ('www.gutenberg.org/ebooks/1342', 1)
MAX: ('the', 8577)
```

![](images/Min_and_Max_Results.png)

**Execution time:** 2.075938 + 0.291528 ≈ 2.37 s

![](images/Min_Time.png)

![](images/Max_Time.png)

## 6. Performance Comparison

Hadoop and Spark were tested on both one-node and two-node configurations using the same Gutenberg dataset.

### 6.1 Execution Time

| Task               | Hadoop 1 Node | Hadoop 2 Nodes | Spark 1 Node | Spark 2 Nodes |
| ------------------ | ------------: | -------------: | -----------: | ------------: |
| Word Count         |         ___ s |          ___ s |        2.33 s |         4.85 s |
| Character Count    |         ___ s |          ___ s |        2.64 s |         4.65 s |
| Min/Max Word Count |         ___ s |          ___ s |        2.37 s |         4.94 s |

### 6.2 Discussion

**1. Which framework executed faster on one node? On two nodes?**

[Insert answer based on measured execution times.]

**2. Which framework is easier to implement in Python?**

Spark was easier to implement in Python because PySpark provides high-level operations such as `flatMap`, `map`, and `reduceByKey`, while Hadoop requires separate mapper and reducer programs.

**3. How does Spark's in-memory processing affect performance compared to Hadoop?**

Spark can keep intermediate data in memory and reduce repeated disk I/O. This can improve performance compared with Hadoop MapReduce, especially for larger or repeated computations. For small datasets, cluster setup and communication overhead may reduce this advantage.
