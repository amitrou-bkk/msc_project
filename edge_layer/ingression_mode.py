from enum import Enum

class EdgeDataIngressMode(Enum):
    FileSystem = 1
    SRTP = 2
    HTTP = 3
    HTTPS = 4
    MessageQueue = 5