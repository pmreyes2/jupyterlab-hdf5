import re

__all__ = ['chunkSlice', 'dsetChunk', 'dsetContentDict', 'dsetDict', 'groupDict', 'uriJoin', 'uriName']

## chunk handling
def chunkSlice(chunk, s):
    if s.start is None:
        return slice(None, s.stop*chunk, s.step)

    return slice(s.start*chunk, s.stop*chunk, s.step)

def dsetChunk(dset, row, col):
    if dset.ndim == 0:
        # for the case of no dimensions
        return [[dset.value]]
    if dset.ndim == 1:
        # For the case of arrays of one dimension
        return [dset[slice(*col)].tolist()]
    return dset[slice(*row), slice(*col)].tolist()

## create dicts to be converted to json
def dsetContentDict(dset, row=None, col=None):
    return dict([
        # metadata
        ('attrs', dict(dset.attrs.items())),
        ('dtype', dset.dtype.str),
        # modifying ndim and shape from 0D or 1D to 2D to trigger coming back
        # here to read the 0 or 1 dimansional array
        ('ndim', 2 if dset.ndim in [0,1] else dset.ndim ),
        ('shape', (1,1) if dset.ndim == 0 else (1,dset.shape[0]) if dset.ndim == 1 else dset.shape),

        # actual data
        ('data', dsetChunk(dset, row, col) if row and col else None)
    ])

def dsetDict(name, uri, content=None):
    return dict([
        ('type', 'dataset'),
        ('name', name),
        ('uri', uri),
        ('content', content)
    ])

def groupDict(name, uri):
    return dict([
        ('type', 'group'),
        ('name', name),
        ('uri', uri),
        ('content', None)
    ])


## uri handling
_emptyUriRe = re.compile('//')
def uriJoin(*parts):
    return _emptyUriRe.sub('/', '/'.join(parts))

def uriName(uri):
    return uri.split('/')[-1]
