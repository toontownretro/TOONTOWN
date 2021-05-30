"""DistributedJailbirdDale module: contains the DistributedJailbirdDale class"""

from toontown.toonbase.ToontownModules import *
import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.classicchars import DistributedDale
import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
import DistributedCCharBase

class DistributedJailbirdDale(DistributedDale.DistributedDale):
    """DistributedDale class"""

    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedJailbirdDale')

    def __init__(self, cr):
        try:
            self.DistributedDale_initialized
        except:
            self.DistributedDale_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr,
                                                               TTLocalizer.JailbirdDale,
                                                               'jda')
            self.fsm = ClassicFSM.ClassicFSM('DistributedJailbirdDale',
                            [State.State('Off',
                                         self.enterOff,
                                         self.exitOff,
                                         ['Neutral']),
                             State.State('Neutral',
                                         self.enterNeutral,
                                         self.exitNeutral,
                                         ['Walk']),
                             State.State('Walk',
                                         self.enterWalk,
                                         self.exitWalk,
                                         ['Neutral']),
                             ],
                             # Initial State
                             'Off',
                             # Final State
                             'Off',
                             )

            self.fsm.enterInitialState()

            self.nametag.setName(TTLocalizer.Dale)
            
    def walkSpeed(self):
        return ToontownGlobals.DaleSpeed
