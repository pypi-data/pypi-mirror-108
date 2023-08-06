#
#   Test if all pygeos methods are implemented
#   This makes it easier to update PGPD to new PyGEOS versions
#
import pytest
import pygeos
import pgpd

skips = {
    'geometry': (
        '_geometry',
        'get_geometry',
        'get_point',
    ),
    'creation': (
        '_wrap_construct_ufunc',
        'box',
        'geometrycollections',
        'linearrings',
        'linestrings',
        'multilinestrings',
        'multipoints',
        'multipolygons',
        'points',
        'polygons',
    ),
    'measurement': (),
    'predicates': (
        'warnings',
    ),
    'set_operations': (
        'UnsupportedGEOSOperation',
        'box',
    ),
    'constructive': (
        'BufferCapStyles',
        'BufferJoinStyles',
        'ParamEnum',
    ),
    'linear': (
        'warn',
    ),
    'coordinates': (),
    'strtree': (
        'BinaryPredicate',
        'ParamEnum',
        'VALID_PREDICATES',
    ),
}


@pytest.mark.parametrize('module', skips.keys())
def test_for_missing_methods(module):
    skip = skips[module]
    mod = getattr(pygeos, module)

    for func in dir(mod):
        if func.startswith('__'):
            continue
        if func in ('Geometry', 'GeometryType', 'IntEnum', 'lib', 'np', 'requires_geos', 'multithreading_enabled'):
            continue
        if func in skip:
            continue

        if func not in dir(pgpd.GeosSeriesAccessor):
            raise NotImplementedError(f'{module}.{func}')
