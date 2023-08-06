# memory-monitor-cli

To install:
```shell
$ pip install memory-monitor-cli
```

Monitor the memory with a time window of `1` minute (`m`) and refresh each second (`60` times per minute):
```shell
$ mm-cli run --time-window 1 --time-unit m --frequency 60
```

Streaming to a file...
```shell
$ mm-cli run --time-window 1 --time-unit m --frequency 60 --stream-to-file memory-usage.gz
```
and (maybe later) show the stream:
```shell
$ mm-cli show --stream-from-file memory-usage.gz
```