from toontown.toonbase.ToontownModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect, Particles, ForceGroup
from .PooledEffect import PooledEffect
from .EffectController import EffectController

class GlowTrail(PooledEffect, EffectController):

    def __init__(self):
        # Initialize the superclass
        PooledEffect.__init__(self)
        EffectController.__init__(self)

        # Grab Texture off the Texture Card
        model = loader.loadModel("phase_4/models/props/tt_m_efx_ext_particleCards")
        self.card = model.find("**/tt_t_efx_ext_particleWhiteGlow")
        self.cardScale = 64.0

        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectScale = 1.0
        self.lifespan = .5

        if not GlowTrail.particleDummy:
            GlowTrail.particleDummy = render.attachNewNode(ModelNode('GlowTrailParticleDummy'))
            GlowTrail.particleDummy.setDepthWrite(0)
            GlowTrail.particleDummy.setLightOff()
            GlowTrail.particleDummy.setFogOff()

        # Load Particle Effects
        self.f = ParticleEffect.ParticleEffect("GlowTrail")
        self.f.reparentTo(self)
        self.p0 = Particles.Particles('particles-1')
        self.p0.setFactory("PointParticleFactory")
        self.p0.setRenderer("SpriteParticleRenderer")
        self.p0.setEmitter("PointEmitter")
        self.f.addParticles(self.p0)

        self.p0.setPoolSize(64)
        self.p0.setBirthRate(0.02)
        self.p0.setLitterSize(1)
        self.p0.setLitterSpread(0)
        self.p0.setSystemLifespan(0.0000)
        self.p0.setLocalVelocityFlag(0)
        self.p0.setSystemGrowsOlderFlag(0)
        # Factory parameters
        self.p0.factory.setLifespanBase(self.lifespan)
        self.p0.factory.setLifespanSpread(0.1)
        self.p0.factory.setMassBase(1.0000)
        self.p0.factory.setMassSpread(0.0000)
        self.p0.factory.setTerminalVelocityBase(400.0000)
        self.p0.factory.setTerminalVelocitySpread(0.0000)
        # Renderer parameters
        self.p0.renderer.setAlphaMode(BaseParticleRenderer.PRALPHAOUT)
        self.p0.renderer.setUserAlpha(1.0)
        # Sprite parameters
        self.p0.renderer.setFromNode(self.card)
        self.p0.renderer.setColor(Vec4(1.00, 1.00, 1.00, 1.00))
        self.p0.renderer.setXScaleFlag(1)
        self.p0.renderer.setYScaleFlag(1)
        self.p0.renderer.setAnimAngleFlag(1)
        self.p0.renderer.setNonanimatedTheta(0.0000)
        self.p0.renderer.setAlphaBlendMethod(BaseParticleRenderer.PPBLENDLINEAR)
        self.p0.renderer.setAlphaDisable(0)
        self.p0.renderer.setColorBlendMode(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne)
        # Emitter parameters
        self.p0.emitter.setEmissionType(BaseParticleEmitter.ETRADIATE)
        self.p0.emitter.setAmplitudeSpread(0.0)
        self.p0.emitter.setOffsetForce(Vec3(0.0000, 0.000, -2.0000))
        self.p0.emitter.setExplicitLaunchVector(Vec3(1.0000, 0.0000, 0.0000))
        self.p0.emitter.setRadiateOrigin(Point3(0.0000, 0.0000, 0.0000))
        self.setEffectScale(self.effectScale)

    def createTrack(self):

        self.startEffect = Sequence(
            Func(self.p0.setBirthRate, 0.015),
            Func(self.p0.clearToInitial),
            Func(self.f.start, self, self.particleDummy),
            )
        self.endEffect = Sequence(
            Func(self.p0.setBirthRate, 100.0),
            Wait(self.lifespan+0.1),
            Func(self.cleanUpEffect),
            )
        self.track = Sequence(
            self.startEffect,
            Wait(1.0),
            self.endEffect,
            )

    def setLifespan(self, duration):
        self.lifespan = duration
        self.p0.setPoolSize(int(128 * self.lifespan))
        self.p0.factory.setLifespanBase(self.lifespan)

    def setEffectColor(self, color):
        self.effectColor = color
        self.p0.renderer.setColor(self.effectColor)

    def setEffectScale(self, scale):
        self.effectScale = scale
        self.p0.renderer.setInitialXScale(0.15*self.cardScale*scale)
        self.p0.renderer.setFinalXScale(.1*self.cardScale*scale)
        self.p0.renderer.setInitialYScale(0.15*self.cardScale*scale)
        self.p0.renderer.setFinalYScale(.4*self.cardScale*scale)
        self.p0.emitter.setAmplitude(10.0*scale)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool and self.pool.isUsed(self):
            self.pool.checkin(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)
