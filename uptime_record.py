import utils_logger
import psutil, time, os

class UptimeRecord:
    def __init__(self):
        self.logger = utils_logger.get_logger(self.__class__.__name__)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self._file_record = os.path.join(current_dir, 'record.txt')
    
    def record(self):
        time_format = '%Y-%m-%d %H:%M:%S'
        time_boot = psutil.boot_time()
        time_now = time.time()
        uptime = time_now - time_boot
        uptime = int(uptime)

        seconds_day = 60 * 60 * 24
        seconds_hour = 60 * 60
        seconds_minute = 60
        uptime_days = int(uptime / seconds_day)
        uptime_hours = int((uptime - uptime_days * seconds_day) / seconds_hour)
        uptime_minutes = int((uptime - uptime_days * seconds_day - uptime_hours * seconds_hour) / seconds_minute)
        uptime_seconds = uptime - uptime_days * seconds_day - uptime_hours * seconds_hour - uptime_minutes * seconds_minute

        uptime_str = '{} {}:{}:{}'.format(uptime_days, uptime_hours, uptime_minutes, uptime_seconds)
        time_boot_str = time.strftime(time_format, time.localtime(time_boot))
        time_now_str = time.strftime(time_format, time.localtime(time_now))

        record = '{},{},{},{},{},{}'.format(
            time_boot, time_now, uptime, time_boot_str, time_now_str, uptime_str
        )

        data_records = []
        if os.path.exists(self._file_record):
            with open(self._file_record, 'r') as file:
                data_records = file.read().split('\n')

        with open(self._file_record, 'w') as file:
            flag_update = False
            if len(data_records) > 0:
                last_record = data_records[-1]
                if last_record.split(',')[0] == str(time_boot):
                    data_records[-1] = record
                    flag_update = True
                    self.logger.info('update uptime time_boot: {}'.format(time_boot_str))
            if not flag_update:
                data_records.append(record)
                self.logger.info('record new uptime time_boot: {}'.format(time_boot_str))

            max_lines = 1000
            if len(data_records) > max_lines:
                data_records = data_records[-max_lines:]
            file.write('\n'.join(data_records))

if __name__ == '__main__':
    UptimeRecord().record()