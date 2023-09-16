from enum import Enum

class EdgeDataIngressMode(Enum):
    FileSystem = 1
    HTTP = 3
    HTTPS = 4
    MessageQueue = 5