import threading
import time

from BackupNS import BackupNS

try:
    backup_name_server = BackupNS()

    backup_server_udp_thread = threading.Thread(target=backup_name_server.start_listening_udp)
    backup_server_udp_thread.start()

    backup_server_tcp_thread = threading.Thread(target=backup_name_server.start_listening_tcp)
    backup_server_tcp_thread.start()
except KeyboardInterrupt:
    pass