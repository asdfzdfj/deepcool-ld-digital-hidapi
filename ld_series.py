from utils import f32_to_bytes, u32_to_bytes

VID, PID = 13875, 10
REPORT_ID = 16

# LD series hid init sequence, do not change
# note that this is a complete packets, ready to be written with hidapi device.write()
INIT_SEQUENCE = [
    [REPORT_ID, 104, 1, 1, 2, 3, 1, 112, 22],
    [REPORT_ID, 104, 1, 1, 2, 2, 1, 111, 22]
]

# it has checksum, which is just adding all report bytes together
# and then take the last byte (should effectively be the same as sum % 256)
def cksum(reports):
    """calculate checksum for the given list of report bytes"""
    report_sum = sum(reports)

    return report_sum % 256

def make_packet(report):
    """make a full packet for writing out with hidapi device.write()"""
    return [REPORT_ID, *report, cksum(report), 22]

def make_report(power, temp, usage, use_fahrenheit=False):
    """create full report packet from given sensor data"""
    power_bytes = u32_to_bytes(int(power), 2)
    temp_bytes = f32_to_bytes(float(temp))
    usage_bytes = u32_to_bytes(int(usage), 1)
    use_f_byte = 1 if use_fahrenheit else 0

    return make_packet([
        # packet preamble?
        104, 1, 1, 11, 1, 2, 5,
        *power_bytes,
        use_f_byte,
        *temp_bytes,
        *usage_bytes
    ])
