import subprocess
import psutil

def _run_sysctl(name):
    stdout = subprocess.run(['/sbin/sysctl', '-n', name], capture_output=True).stdout
    value = stdout.decode('utf-8').strip()

    return value

def get_cpu_usage_percent():
    percent = psutil.cpu_percent()
    percent_rounded = round(percent, 0)

    return percent_rounded

def get_cpu_temp():
    sysctl_temp = _run_sysctl('dev.amdtemp.0.core0.sensor0')
    temp = float(sysctl_temp.strip('C'))

    return temp

# without additional sensor readings the best I could do is this bad estimation
def estimate_power_usage():
    freq_levels = _run_sysctl('dev.cpu.0.freq_levels')
    cpu_freq = psutil.cpu_freq().current
    nproc = psutil.cpu_count()

    # format: <Mhz>/<mW>
    freq_power_map = { hz: int(mw) for hz, mw in (f.split('/') for f in freq_levels.split(' ')) }
    power_estimate = freq_power_map[str(cpu_freq)] * nproc / 1000

    return power_estimate

def get_stats(get_temp=True, get_usage=True, get_power=False):
    return {
        'temp': get_cpu_temp() if get_temp else 0,
        'usage': get_cpu_usage_percent() if get_usage else 0,
        'power': estimate_power_usage() if get_power else 0,
    }
