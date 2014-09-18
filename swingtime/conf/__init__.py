from django.conf import settings
from swingtime.conf import swingtime_settings


#===============================================================================
class AppSettings(object):
    
    SETTINGS_MODULE = None
    
    #---------------------------------------------------------------------------
    def __init__(self, base_settings_module, global_override):
        
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(base_settings_module):
            if setting == setting.upper():
                setattr(self, setting, getattr(base_settings_module, setting))

        if hasattr(settings, global_override):
            self.SETTINGS_MODULE = getattr(settings, global_override)
            try:
                mod = __import__(self.SETTINGS_MODULE, {}, {}, [''])
            except ImportError as e:
                raise ImportError(
                    "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (self.SETTINGS_MODULE, e)
                )
            
            for setting in dir(mod):
                if setting == setting.upper():
                    setattr(self, setting, getattr(mod, setting))

    #---------------------------------------------------------------------------
    def get_all_members(self):
        return dir(self)
    
settings = AppSettings(swingtime_settings, 'SWINGTIME_SETTINGS_MODULE')