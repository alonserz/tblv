import pathlib
import struct
from functools import lru_cache
from tblv.crc32c import masked_crc32c
from tblv.tf_protobuf.event_pb2 import Event


@lru_cache()
def test(data, crc):
    crc = struct.unpack('I', crc)[0]
    data_crc = masked_crc32c(data)
    if crc != data_crc:
        print(f'Warning: CRC not match! Got {data_crc}, expect {crc}')

def parse_file(path):
    data = {}
    with open(path, 'rb') as file:
        while True:
            part = file.read(8)
            if not part:
                break
            test(part, file.read(4))
            raw = struct.unpack('Q', part)[0]
            raw = file.read(raw)
            test(raw, file.read(4))
            event = Event()
            event.ParseFromString(raw)

            values = event.summary.value
            step = event.step

            for value in values:
                if not value.HasField('simple_value'):
                    continue

                tag = value.tag
                simple_value = value.simple_value

                if tag not in data.keys():
                    data[tag] = {}

                data[tag][step] = simple_value

    return data

def parse_dir(path):
    data = {}
    dir = pathlib.Path(path)
    files = dir.rglob('*.0')
    for file in files:
        dir_name = str(file.parent)
        file_name = file.name
        if dir_name not in data.keys():
            data[dir_name] = []
        data[dir_name].append(file_name)
    return data

           
def get_x_y_title(data, idx):
    tags = list(data.keys())
    if idx not in range(len(tags)):
        return (), (), "Wrong index"
    tag = tags[idx]
    x = tuple(data[tag].keys())
    y = tuple(data[tag].values())
    return x, y, tag
