from toontown.toonbase.ToontownModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect, Particles, ForceGroup
from .EffectController import EffectController
from .PooledEffect import PooledEffect
import random

class FireworkSparkles(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)

        model = loader.loadModel("phase_4/models/props/tt_m_efx_ext_fireworkCards")
        self.card = model.find("**/tt_t_efx_ext_particleSpark_sharp")
        self.cardScale = 16.0

        self.setDepthWrite(0)
        self.setColorScaleOff()
        self.setLightOff()

        self.startDelay = 0.0
        self.effectScale = 1.0
        self.effectColor = Vec4(1,1,1,1)

        # Load Particle Effects
        self.f = ParticleEffect.ParticleEffect("Sparkles")
        self.f.reparentTo(self)

        self.p0 = Particles.Particles('particles-2')
        self.p0.setFactory("PointParticleFactory")
        self.p0.setRenderer("SpriteParticleRenderer")
        self.p0.setEmitter("SphereVolumeEmitter")

        self.f.addParticles(self.p0)

        # Setup forces
        f0 = ForceGroup.ForceGroup('Gravity')
        force0 = LinearVectorForce(Vec3(0.0, 0.0, -15.0), 1.0, 0)
        force0.setVectorMasks(1, 1, 1)
        force0.setActive(1)
        f0.addForce(force0)
        self.f.addForceGroup(f0)

        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(10)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0)
        self.p0.setLocalVelocityFlag(1)
        self.p0.setSystemGrowsOlderFlag(0)
        # Factory parameters
        self.p0.factory.setLifespanBase(1.5)
        self.p0.factory.setLifespanSpread(1.0)
        self.p0.factory.setMassBase(1.0000)
        self.p0.factory.setMassSpread(0.0000)
        self.p0.factory.setTerminalVelocityBase(400.0)
        self.p0.factory.setTerminalVelocitySpread(0.0)
        # Renderer parameters
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd,ColorBlendAttrib.OIncomingAlpha,ColorBlendAttrib.OOne)
        # Sprite parameters
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.0, 1.0, 1.0, 1.0))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0000)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.getColorInterpolationManager().addLinear(0.0,.1,Vec4(0,0,0,0),self.effectColor,1)
        # Emitter parameters
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitudeSpread(0.0000)
        self.p0.emitter.setOffsetForce(Vec3(0.0, 0.0, 0.0))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0, 0.0, 0.0))
        self.p0.emitter.setRadiateOrigin(Point3(0.0, 0.0, 0.0))
        self.setEffectScale(self.effectScale)
        self.setEffectColor(self.effectColor)

    def createTrack(self):
        self.track = Sequence(
            Wait(self.startDelay),
            Func(self.p0.setBirthRate, .03),
            Func(self.p0.clearToInitial),
            Func(self.f.start, self, self),
            Wait(.3),
            Func(self.p0.setBirthRate, 100.0),
            Wait(2.5),
            Func(self.cleanUpEffect)
            )

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(1.2*self.cardScale*scale)
        self.p0.renderer.setFinalXScale(1.5*self.cardScale*scale)
        self.p0.renderer.setInitialYScale(1.5*self.cardScale*scale)
        self.p0.renderer.setFinalYScale(1.2*self.cardScale*scale)
        self.p0.emitter.setAmplitude(25.0*scale)
        self.p0.emitter.setRadius(400.0*scale)

    def setRadius(self, radius):
        self.p0.emitter.setRadius(radius)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.setColor(self.effectColor)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
