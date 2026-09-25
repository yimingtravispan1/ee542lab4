# EE 542 Lab 4: Hadoop and Spark

This project compares Hadoop MapReduce and Apache Spark for text analysis on a Gutenberg dataset. It documents setting up a one- and two-node Hadoop cluster on AWS EC2, implementing the analysis jobs in Python, and comparing their execution times.

## Analysis jobs

- **Word count:** count occurrences of each word.
- **Character count:** count occurrences of each character.
- **Minimum and maximum word count:** find the least and most frequent words.

Hadoop jobs use Hadoop Streaming mapper and reducer scripts. Spark jobs use PySpark transformations.

## Project files

- [`src/hadoop/`](src/hadoop/) — Hadoop Streaming mapper and reducer scripts.
- [`src/spark/`](src/spark/) — PySpark analysis programs.
- [`images/`](images/) — screenshots and experiment results.
- [`report.md`](report.md) — setup details, results, and performance discussion.
