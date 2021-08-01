async def trace_leak(delay=60, top=20, trace=1):

Use spawn_callback to invoke:

tornado.ioloop.IOLoop.current().spawn_callback(trace_leak, param delay: in seconds (int)

param top: number of top allocations to list (int)

param trace: number of top allocations to trace (int)

:return: None

logger.info('start_trace', delay=delay, top-top, trace trace)

tracemalloc.start(25)

start = tracemalloc, take_snapshot()

prev = start

while True:

await tornado gen.sleep(delay)

current = tracemalloc take_snapshot() # compare current snapshot to previous snapshot prev_stats = current.compare_to(prev, "lineno)

# compare current snapshot to starting snapshot stats = current.compare_to(start, 'filename')

logger.info('Top Diffs since Start') # Print top diffs: current snapshot - start snapshot for i, stat in enumerate(stats[:top). 1):

logger.info(top_diffs', i=i, stat=str(stat))

logger.info('Top Incremental)

# Print top incremental stats: current snapshot - previous sna for I, stat in enumerate(prev_ stats[:top], 1): logger.info(top incremental, I-i, stat-str(stat))

logger.info('Top Current)

# Print top current stats

for I, stat in enumerate(current staunlics("filename')[top],

logger.info(top current, ini, stateatr(stat)) # get tracebacka (stack trace) for the current snapshot

traces curent.statistics(traceback') for stat in traces[:trace):

Logo Informe back memory blocks=stat.count. size k