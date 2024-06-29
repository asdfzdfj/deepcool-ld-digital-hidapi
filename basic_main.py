import sys
import hid

import ld_series

from time import sleep, time_ns

from system_stat import get_stats

class HidDevice:
    def __init__(self, vid, pid, serial=None):
        self.vid, self.pid = vid, pid
        self.serial = serial
        self.device = None

    def __enter__(self):
        self.device = hid.device()
        self.device.open(self.vid, self.pid, self.serial)
        self.device.set_nonblocking(1)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.device is not None:
            self.device.close()
            self.device = None

    def write(self, report):
        self.write_multiple([report])

    def write_multiple(self, reports):
        """write multiple report packets in quick succession"""
        if self.device is None:
            raise RuntimeError('device has not been opened')

        for report in reports:
            self.device.write(report)

if __name__ == '__main__':
    ONE_SEC_NS = 10**9
    try:
        with HidDevice(ld_series.VID, ld_series.PID) as device:
            device.write_multiple(ld_series.INIT_SEQUENCE)
            next_send_time = 0

            while True:
                if (time_ns() >= next_send_time):
                    stats = get_stats(get_power=False)
                    report = ld_series.make_report(**stats)
                    device.write(report)

                    print(f"sent {stats}", file=sys.stderr)
                    next_send_time = time_ns() + ONE_SEC_NS

                sleep(0.01)

    except KeyboardInterrupt:
        print('ctrl-c received, exiting', file=sys.stderr)
