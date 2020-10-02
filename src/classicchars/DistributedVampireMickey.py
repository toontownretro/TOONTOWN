"""DistributedVampireMickey module: contains the DistributedVampireMickey class"""

from toontown.toonbase.ToontownModules import *
from . import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from toontown.classicchars import DistributedMickey
from . import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from . import DistributedCCharBase

class DistributedVampireMickey(DistributedMickey.DistributedMickey):
    """DistributedVampireMickey class"""

    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedVampireMickey")

    def __init__(self, cr):
        try:
            self.DistributedMickey_initialized
        except:
            self.DistributedMickey_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr,
                                                               TTLocalizer.VampireMickey,
                                                               'vmk')
            self.fsm = ClassicFSM.ClassicFSM(self.getName(),
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

            # We want him to show up as Mickey
            self.nametag.setName(TTLocalizer.Mickey)

    def walkSpeed(self):
        return ToontownGlobals.VampireMickeySpeed
