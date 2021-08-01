import tracemalloc
tracemalloc.start()

new_snap=tracemalloc.take_snapshot().load('data.txt')
s=tracemalloc.take_snapshot()
top_stats = new_snap.compare_to(s,"lineno")
lines= []
print("*********************")
for stats in top_stats[:5]:
	lines.append(str(stats))
	print(str(stats))