import json
import time
from data.server import Data

def get_return_length(byte_data):
    data_length = 0
    if b'OP' in byte_data:
        data_length = 12
    if b'SP' in byte_data:
        data_length = 12
    if b'BV' in byte_data:
        data_length = 116
    return data_length