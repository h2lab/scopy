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

    def __init__(self, con=None, 
            gain=78, 
            samples=24400, 
            offset=0, 
            mode="rising_edge",
            freq = 7370000,
            adc_src = "clkgen_x4",
            triggers = "tio4",
            hs2 = "clkgen",
            scope_type = None,
            sn = None
            ):


        if scope_type is None:
            scope_type = get_cw_type() 
            self._scope = scope_type()
        self._scope.con(sn)

        for k in dir(self._scope):
            if not k.startswith('_'):
                setattr(self.__class__, k, getattr(self._scope,k))
        
        # setup scope parameters
        self.gain.gain = gain
        self.adc.samples = samples 
        self.adc.offset = offset
        self.adc.basic_mode = mode
        self.clock.clkgen_freq = freq
        self.clock.adc_src = adc_src
        self.trigger.triggers = triggers
        self.io.hs2 = hs2

       

