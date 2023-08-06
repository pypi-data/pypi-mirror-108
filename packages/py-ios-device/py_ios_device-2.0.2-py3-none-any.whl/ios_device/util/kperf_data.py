from collections import namedtuple

from construct import Struct, Int32ul, Int64ul, FixedSized, GreedyRange, Padding, CString, Array, Byte, Const, Bytes, \
    Adapter, struct

KdBuf = namedtuple('KdBuf', ['timestamp', 'data', 'values', 'tid', 'debugid', 'eventid', 'func_qualifier'])
RAW_VERSION2_BYTES = b'\x00\x02\xaa\x55'
kd_buf_format = '<Q32sQIIQ'
kd_buf_size = struct.calcsize(kd_buf_format)
ProcessData = namedtuple('namedtuple', ['pid', 'name'])

KDBG_EVENTID_MASK = 0xfffffffc
KDBG_FUNC_MASK = 0x00000003


class KDBufAdapter(Adapter):
    def _decode(self, obj, context, path):
        return make_event(obj)


def make_event(buf):
    timestamp, args_buf, tid, debugid, cpuid, unused = struct.unpack(kd_buf_format, buf)
    return KdBuf(
        timestamp, args_buf, struct.unpack('<QQQQ', args_buf), tid, debugid, debugid & KDBG_EVENTID_MASK,
                                                                             debugid & KDBG_FUNC_MASK
    )


kd_threadmap = Struct(
    'tid' / Int64ul,
    'pid' / Int32ul,
    'process' / FixedSized(20, CString('utf8')),
)

kperf_data = Struct(
    'magic' / Const(RAW_VERSION2_BYTES, Bytes(4)),
    'number_of_treads' / Int32ul,
    Padding(8),
    Padding(4),
    'is_64bit' / Int32ul,
    'tick_frequency' / Int64ul,
    Padding(0x100),
    'threadmap' / Array(lambda ctx: ctx.number_of_treads, kd_threadmap),
    '_pad' / GreedyRange(Const(0, Byte)),
    'traces' / GreedyRange(KDBufAdapter(Bytes(kd_buf_size)))
)


class CoreProfileSessionTap:

    def __init__(self):
        self._thread_map = {}

    @property
    def thread_map(self):
        return self._thread_map

    @thread_map.setter
    def thread_map(self, parsed_threadmap):
        self._thread_map.clear()
        for thread in parsed_threadmap:
            self._thread_map[thread.tid] = ProcessData(thread.pid, thread.process)

    def watch_events(self, data):
        if data.startswith(RAW_VERSION2_BYTES):
            parsed = kperf_data.parse(data)
            self.thread_map = parsed.threadmap
            traces = parsed.traces
            for event in traces:
                yield event
        else:
            for i in range(int(len(data) / kd_buf_size)):
                buf = data[i * kd_buf_size: (i + 1) * kd_buf_size]
                yield make_event(buf)
