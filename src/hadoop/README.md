# EE542 Lab 4 — Hadoop Source and Configurations

This is a GitHub-ready **source bundle reconstructed from the commands used in the EE542 Lab 4 conversation**. The five Python programs reproduce the code provided and executed in the chat; the XML files and configuration snippets reproduce the configuration values used in the setup. They have **not** been independently downloaded from the running EC2 machines or verified byte-for-byte against files currently on those machines. For an exact submission snapshot, compare them with `~/ee542-lab4/mapreduce/` and `/usr/local/hadoop/etc/hadoop/` on the Master before uploading.

## Layout

```text
mapreduce/
  wordcount_mapper.py
  wordcount_reducer.py
  minmax_reducer.py
  char_mapper.py
  char_reducer.py
config/
  core-site.xml
  hdfs-site.xml
  mapred-site.xml
  yarn-site.xml
  workers.single-node
  workers.two-nodes
  java-and-hadoop-env.sh
  hosts.cluster-entries
results/
  hadoop_initial_runs.csv
```

## Environment used

- AWS: Master `10.0.1.64`, Worker `10.0.1.71`; Ubuntu 22.04.5 LTS (`t2.medium` each).
- OpenJDK 11, Hadoop 3.3.6; Hadoop installed at `/usr/local/hadoop`.
- HDFS input: `/gutenberg/pg1342.txt` and `/gutenberg/pg84.txt` (total 1,221,271 bytes; 22,656 lines).
- `config/workers.single-node` was used for the original baseline; `config/workers.two-nodes` for the expanded cluster.
- HDFS replica count remained `1`. Both nodes were later registered with HDFS and YARN.
- `config/hosts.cluster-entries` contains **additional mappings only**, not a replacement for `/etc/hosts`.

## Processing rules

- Word Count splits on whitespace. Case and punctuation are preserved; `the` and `The` are different keys.
- Min/Max is a **second Hadoop Streaming job** reading Word Count's `part-*` output. Its elapsed time excludes the first Word Count stage. Equal-frequency minima/maxima use the first encountered key.
- Character Count removes line endings, counts spaces and punctuation, and preserves case; output keys are Unicode code points such as `U+0020` for space.

## Run on the Master

Before running, check `hadoop version`, `yarn node -list`, and `hdfs dfs -ls /gutenberg`. Run from `mapreduce/`. The HDFS output directory must not exist before submission. Set `LABEL=1node` for single-node or `LABEL=2nodes` for two-node trials, and use the matching `workers` configuration **before** starting services; these commands do not reconfigure the cluster. Use `/usr/bin/time -p` and record `real` elapsed seconds.

```bash
cd ~/ee542-lab4/mapreduce
LABEL=2nodes
JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar
mkdir -p ~/ee542-lab4/results
set -o pipefail

/usr/bin/time -p hadoop jar "$JAR" \
  -files wordcount_mapper.py,wordcount_reducer.py \
  -input /gutenberg \
  -output "/output_wordcount_${LABEL}" \
  -mapper 'python3 wordcount_mapper.py' \
  -reducer 'python3 wordcount_reducer.py' \
  -numReduceTasks 1 \
  2>&1 | tee "${HOME}/ee542-lab4/results/wordcount_${LABEL}.log"

/usr/bin/time -p hadoop jar "$JAR" \
  -files minmax_reducer.py \
  -input "/output_wordcount_${LABEL}/part-*" \
  -output "/output_minmax_${LABEL}" \
  -mapper cat \
  -reducer 'python3 minmax_reducer.py' \
  -numReduceTasks 1 \
  2>&1 | tee "${HOME}/ee542-lab4/results/minmax_${LABEL}.log"

/usr/bin/time -p hadoop jar "$JAR" \
  -files char_mapper.py,char_reducer.py \
  -input /gutenberg \
  -output "/output_charcount_${LABEL}" \
  -mapper 'python3 char_mapper.py' \
  -reducer 'python3 char_reducer.py' \
  -numReduceTasks 1 \
  2>&1 | tee "${HOME}/ee542-lab4/results/charcount_${LABEL}.log"
```

For the recorded two-node Character Count, the first run failed due to `UnknownHostException` and the successful output was saved separately to `/output_charcount_2nodes_retry1`; its successful measured time was **28.71 s**. If that directory already exists, choose another unused output path. Never treat the failed attempt's `17.91 s` as a successful measurement.

## Verify outputs

```bash
hdfs dfs -ls /output_wordcount_2nodes
hdfs dfs -cat '/output_minmax_2nodes/part-*'
hdfs dfs -ls /output_charcount_2nodes_retry1

hdfs dfs -cat '/output_wordcount_1node/part-*' | sort > /tmp/wc_1node.txt
hdfs dfs -cat '/output_wordcount_2nodes/part-*' | sort > /tmp/wc_2nodes.txt
diff -q /tmp/wc_1node.txt /tmp/wc_2nodes.txt

hdfs dfs -cat '/output_charcount_1node/part-*' | sort > /tmp/char_1node.txt
hdfs dfs -cat '/output_charcount_2nodes_retry1/part-*' | sort > /tmp/char_2nodes.txt
diff -q /tmp/char_1node.txt /tmp/char_2nodes.txt
```

For the recorded experiments both `diff -q` comparisons produced no output. The Min/Max results were `MIN #1342] 1` and `MAX the 8577` under both configurations.

## Recorded initial results

| Job | One node (s) | Two nodes (s) |
| --- | ---: | ---: |
| Word Count | 30.22 | 33.45 |
| Min/Max (second stage) | 24.49 | 24.97 |
| Character Count | 29.27 | 28.71 |

Each time is one successful measurement, not a multi-run average. The 2-node Hadoop cluster registered two DataNodes and two NodeManagers; per-task worker placement was not independently verified. More repeat runs may improve comparison quality.
