#import chipwhisperer as cw

from scopy.scopes._base import _base as scope_base

from chipwhisperer.capture import scopes
from chipwhisperer.common.utils.util import get_cw_type


class cw_scope(scope_base):
    name = "Chipwhisperer Scope"
    ifaces = { } # Chipwhisper devices are handling the connection

    def querry_id(self):
        cw_id = "NEWAE,{},V{}.{}.{}".format(self.get_name(), self.fw_version['major'], self.fw_version['minor'],self.fw_version['debug'])
        return cw_id

    def __init__(self, args):
        scope_type = Nargs.get('scope_type') if args.get('scope_type') else None
        if scope_type is None:
            scope_type = get_cw_type() 
            self._scope = scope_type()
        self._scope.con(sn)

        for k in dir(self._scope):
            if not k.startswith('_'):
                setattr(self.__class__, k, getattr(self._scope,k))
        
        # setup scope parameters
        gain=args.get('gain') if args.get('gain') else 78
        sn = args.get('sn') if args.get('sn') else None
        samples = args.get('sample_size') if args.get('sample_size') else 24400
        offset=args.get('offset') if args.get('offset') else 0 
        mode= args.get('mode') if args.get('mode') else "rising_edge"
        freq = args.get('freq') if args.get('freq') else 7370000
        adc_src = args.get('adc_src') if args.get('adc_src') else "clkgen_x4"
        triggers = args.get('triggers') if args.get('triggers') else "tio4"
        hs2 = args.get('hs2') if args.get('hs2') else "clkgen"

       

