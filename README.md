# Deepcool LD Series Digital support for non-Windows OS

using [HIDAPI](https://github.com/libusb/hidapi)

should works on Linux, FreeBSD and other places where hidapi is supported

> [!NOTE]
> the current state of this repo is intended to be more of a reference
> implementation for using the cooler display outside Windows, and not suitable
> for use as-is
> (unless you somehow have a FreeBSD machine with amdtemp(4) compatible CPU and
> the LD series cooler attached to it, that is)  
> also, there's no plan to package this into a ready to use service currently

## requirements

python3, [`hidapi`](https://pypi.org/project/hidapi/) python bindings, and
system's hidapi library

additionally, [`psutil`](https://pypi.org/project/psutil/) for conveniences in
gathering sensors data, but that's not the main point

## device usage

the main piece is in [`ld_series.py`](./ld_series.py)

### initialization

write the two packets in `ld_series.INIT_SEQUENCE` to the device, note that the
packets are already complete and ready to be used in hidapi `device.write()`
command

### make and send the report data

use `ld_series.make_report(power, temp, usage, use_fahrenheit=False)`
to generate a report packet from supplied values, then write them to the
device using hidapi `device.write()` command

supported values:
- power (uint16, should be watts)
- temperature (float32, in degC, or degF with `use_fahrenheit=True`)
    - despite it taking float32 shaped value, it doesn't seems handle/display
      negative temps properly, probably needs more investigation
- usage (uint8, cpu percent, should be between 0-100)

## example

quick example:

```python
import hidapi
import ld_series

dev = hidapi.device()
dev.open(ld_series.VID, ld_series.PID)

# init sequence
for packet in ld_series.INIT_SEQUENCE:
    dev.write(packet)

# send some data
report = ld_series.make_report(power=0, temp=30, usage=7)
dev.write(report)

# close device when exit
dev.close()
```

also check out [`basic_main.py`](./basic_main.py) for (my own) real world uses
