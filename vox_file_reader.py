import struct
class val:
    def __init__(self,size,off,voxels,palette):
        self.size = size
        self.off = off
        self.voxels = voxels
        self.palette = palette

v = val((0,0,0),0,set(),[])

def handle_chunk(data):
    chunk_header = struct.unpack('4sii',data[v.off:v.off+12])
    v.off+=12
    chunk_id,chunk_size,children_size = chunk_header
    values = {}
    if chunk_id == b"SIZE":
        chunk_data = struct.unpack_from('iii', data[v.off:v.off+chunk_size])
        v.size = chunk_data
    elif chunk_id == b"XYZI":
        num_voxels = struct.unpack_from('i', data[v.off:v.off+4])[0]
        voxels = set()
        for i in range(num_voxels):
            start =v.off+4+(i*4)
            end = v.off+8+(i*4)
            voxels.add(struct.unpack_from('BBBB', data[start:end]))
        chunk_data = voxels
        v.voxels=voxels
    elif chunk_id == b"RGBA":
        palette = [0]*256
        for i in range(256):
            start =v.off+4+(i*4)
            end = v.off+8+(i*4)
            palette[(i+1)%256]=struct.unpack_from('BBBB', data[start:end])
        chunk_data = palette
        v.palette=palette
    else:
        chunk_data = None
    v.off+=chunk_size
    return chunk_id,chunk_size,children_size,chunk_data,values

def voxels_from_file(filepath):
    with open(filepath,"rb") as f:
        header,version = struct.unpack('4si',f.read(8))
        data = f.read()

        for i in range(300):
            try:
                handle_chunk(data)
            except struct.error:
                pass
    return v.voxels,v.palette,v.size
