from pipeline_broadcaster import broadcast,grep,printer
from cothread import threaded

p = printer()
target = broadcast([threaded(grep('foo', p)),
                    threaded(grep('bar', p))])

for _ in range(68):
    target.send("payload1\n")
    target.send("payload2\n")

del target
del p
