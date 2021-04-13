from scopy.scopes.lecroy import lecroy
from scopy.scopes.owon_xds import owon_xds
from scopy.scopes.dummy import dummy

__all__ = ['lecroy', 'owon_xds', 'dummy']

try:
    import chipwhisperer
    from scopy.scopes.cw_scope import cw_scope
    __all__.append('cw_scope')
except:
    pass


