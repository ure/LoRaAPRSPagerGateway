"""
This syslog client can send UDP packets to a remote syslog server.
Timestamps are not supported for simplicity. For more information, see RFC 3164.
"""

import time

# Facility constants
F_KERN = 0  # kernel messages
F_USER = 1  # user-level messages
F_MAIL = 2  # mail system
F_DAEMON = 3  # system daemons
F_AUTH = 4  # security/authorization messages
F_SYSLOG = 5  # messages generated internally by syslogd
F_LPR = 6  # line printer subsystem
F_NEWS = 7  # network news subsystem
F_UUCP = 8  # UUCP subsystem
F_CRON = 9  # clock daemon
F_AUTHPRIV = 10  # security/authorization messages (private)
F_FTP = 11  # FTP daemon
F_NTP = 12  # NTP subsystem
F_AUDIT = 13  # log audit
F_ALERT = 14  # log alert
F_CLOCK = 15  # clock daemon (not standard, but used by some systems)
# Local use facilities
F_LOCAL0 = 16
F_LOCAL1 = 17
F_LOCAL2 = 18
F_LOCAL3 = 19
F_LOCAL4 = 20
F_LOCAL5 = 21
F_LOCAL6 = 22
F_LOCAL7 = 23
# Severity constants (Names reasonably shortened)
S_EMERG = 0
S_ALERT = 1
S_CRIT = 2
S_ERR = 3
S_WARN = 4
S_NOTICE = 5
S_INFO = 6
S_DEBUG = 7


class SyslogClient:
    def __init__(self, facility=F_USER):
        self._facility = facility

    def _format_datetime(self, datetime):
        return "{:3} {:2d} {:02d}:{:02d}:{:02d}".format(
            datetime.tm_mon,
            datetime.tm_mday,
            datetime.tm_hour,
            datetime.tm_min,
            datetime.tm_sec,
        )

    def log(self, severity, message):
        """Log a message with the given severity."""
        data = "<{}>{} {} {}".format(
            (self._facility << 3) + severity,
            self._format_datetime(time.localtime()),
            self._hostname,
            message,
        )
        self._sock.send(data.encode())

    def alert(self, msg):
        self.log(S_ALERT, msg)

    def critical(self, msg):
        self.log(S_CRIT, msg)

    def error(self, msg):
        self.log(S_ERR, msg)

    def debug(self, msg):
        self.log(S_DEBUG, msg)

    def info(self, msg):
        self.log(S_INFO, msg)

    def notice(self, msg):
        self.log(S_NOTICE, msg)

    def warning(self, msg):
        self.log(S_WARN, msg)


class UDPClient(SyslogClient):
    def __init__(
        self,
        socket,
        esp,
        hostname="unknown",
        host="127.0.0.1",
        port=514,
        facility=F_USER,
    ):
        super().__init__(facility)

        #        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #        socketaddr = socket.getaddrinfo(config.aprs_host, config.aprs_port)[0][4]
        #        s.connect(socketaddr)
        #        s.send(bytes(rawauthpacket, "utf-8"))

        self._hostname = hostname
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        socketaddr = socket.getaddrinfo(host, port)[0][4]
        self._sock.settimeout(4)
        self._sock.connect(socketaddr, conntype=esp.UDP_MODE)

    def close(self):
        self._sock.close()
