import viz
import vizact
import vizshape
import vizproximity
import random
import vizfx
import vizconnect
import viztask

WATER_RISE_EVENT = viz.getEventID('WATER_RISE_EVENT') 

HEIGHT = 0

obj_vis = []

waterSound = viz.addAudio('fountain.wav')
waterSound.volume(0.2)
choirLocation = viz.addGroup(pos=[0.2,1.8,-53])
choir_sound = choirLocation.playsound('art/scene1 choir.wav')

#scene1 = viz.addChild('art/scene1.osgb')
scene1 = vizfx.addChild('art/scene1.osgb')
viz.MainView.getHeadLight().disable()
# Disable ambient light 
vizfx.setAmbientColor(viz.BLACK)

#scene1.disable(viz.LIGHTING)
scene1.hint(viz.ALLOW_NPOT_TEXTURE_HINT)
scene1.disable(0x3000) #Disable clip plane on model
waterPlane = vizshape.addPlane(size=[400,400],pos=[0,0.2,0])
obj_vis.append(scene1)
obj_vis.append(waterPlane)

sky = viz.addChild('sky_day.osgb')
obj_vis.append(sky)

#bellSensorLocation = viz.addGroup(pos=[0.74121, 0.61385, -74.72057])
#bellSensor = vizproximity.Sensor(vizproximity.Box(size=[6,10,6]),source=bellSensorLocation)
#bellLocation = viz.addGroup(pos=[0.90712, 4.80442, -91.77573])
#bell_sound = bellLocation.playsound('bells.wav',flag=viz.PAUSE)

stoneSensorLocation = viz.addGroup(pos=[0,3.5,-90])
stoneSensor = vizproximity.Sensor(vizproximity.Box(size=[2,3,2]),source=stoneSensorLocation)

from vizfx.postprocess.blur import GaussianBlurEffect
from vizfx.postprocess.composite import BlendEffect
# Create post process effect for blending to blur effect
blur_effect = BlendEffect(None,GaussianBlurEffect(blurRadius=20),blend=0.0)
blur_effect.setEnabled(False)
vizfx.postprocess.addEffect(blur_effect)

def BlurTask():
	blur_effect.setBlend(0.0)
	blur_effect.setEnabled(True)
	yield viztask.waitCall(blur_effect.setBlend,vizact.mix(0.0,1.0,time=3.0))
	blur_effect.setEnabled(False)

from vizfx.postprocess.effect import BaseShaderEffect 
import vizfx.postprocess 

class UnderwaterEffect(BaseShaderEffect): 

	def __init__(self, speed=4.0, scale=4.0, density=20.0, **kw): 
		self._speed = speed 
		self._scale = scale 
		self._density = density 
		BaseShaderEffect.__init__(self,**kw) 

	def _getFragmentCode(self): 
		return """ 
				uniform sampler2D vizpp_InputTex; 
				uniform float osg_FrameTime; 
				uniform float speed; 
				uniform float scale; 
				uniform float density; 
				void main() 
				{ 
					vec2 uv = gl_TexCoord[0].xy; 

					//bumpUV.y = fract(bumpUV.y - osg_FrameTime*0.1); 
					vec2 dt; 
					dt.x = sin(speed*osg_FrameTime+uv.y*density)*0.001*scale; 
					dt.y = cos(0.7+0.7*speed*osg_FrameTime+uv.x*density)*0.001*scale; 

					gl_FragColor = texture2D(vizpp_InputTex,uv+dt); 
				} 
				""" 

	def _createUniforms(self): 
		self.uniforms.addFloat('speed',self._speed) 
		self.uniforms.addFloat('scale',self._scale) 
		self.uniforms.addFloat('density',self._density) 

	def setSpeed(self,speed): 
		self._speed = speed 
		self.uniforms.setValue('speed',speed) 

	def getSpeed(self): 
		return self._speed 

	def setScale(self,scale): 
		self._scale = scale 
		self.uniforms.setValue('scale',scale) 

	def getScale(self): 
		return self._scale 

	def setDensity(self,density): 
		self._density = density 
		self.uniforms.setValue('density',density) 

	def getDensity(self): 
		return self._density 

	def createConfigUI(self): 
		"""Implement configurable interface""" 
		ui = BaseShaderEffect.createConfigUI(self) 
		ui.addFloatRangeItem('Speed',[0.0,10.0],fset=self.setSpeed,fget=self.getSpeed) 
		ui.addFloatRangeItem('Scale',[0.0,10.0],fset=self.setScale,fget=self.getScale) 
		ui.addFloatRangeItem('Density',[0.0,100.0],fset=self.setDensity,fget=self.getDensity) 
		return ui 

def addWaterReflection(plane,height):
	
	SIZE = [512,512]
	
	REFLECT_MASK = viz.LAST_MASK << 1

	#Use same septh texture for both render nodes
	depth = viz.addRenderTexture(format=viz.TEX_DEPTH)
	
	#Setup reflection texture
	reflectTex = viz.addRenderTexture()
	reflect = viz.addRenderNode(size=SIZE)
	reflect.attachTexture(reflectTex)
	reflect.attachTexture(depth,viz.RENDER_DEPTH)
	reflect.setMatrix(viz.Matrix.translate(0,-height,0)*viz.Matrix.scale(1,-1,1)*viz.Matrix.translate(0,height,0))
	reflect.setInheritView(True,viz.POST_MULT)
	reflect.disable(viz.CULL_FACE,op=viz.OP_OVERRIDE)
	reflect.clipPlane([0,-1,0,-height]) #OP_OVERRIDE
	reflect.setCullMask(REFLECT_MASK)
	
	#Setup refraction texture
	refractTex = viz.addRenderTexture()
	refract = viz.addRenderNode(size=SIZE)
	refract.attachTexture(refractTex)
	refract.attachTexture(depth,viz.RENDER_DEPTH)
	refract.clipPlane([0,-1,0,-height]) #OP_OVERRIDE
	refract.setCullMask(REFLECT_MASK)
	
	vert = """
	attribute vec3 Tangent;
	uniform float osg_FrameTime;
	
	#define WAVE_SCALE 0.01
	#define WAVE_SPEED 0.01
	
	void main(void)
	{
		gl_Position = ftransform();

		vec2 fTranslation= vec2(mod(osg_FrameTime, 100.0)*WAVE_SPEED, 0.0);
		vec2 vTexCoords = gl_Vertex.xz*WAVE_SCALE;

		// Scale texture coordinates to get mix of low/high frequency details
		gl_TexCoord[1].xy = vTexCoords.xy+fTranslation*2.0;
		gl_TexCoord[2].xy = vTexCoords.xy*2.0+fTranslation*4.0;
		gl_TexCoord[3].xy = vTexCoords.xy*4.0+fTranslation*2.0;
		gl_TexCoord[4].xy = vTexCoords.xy*8.0+fTranslation;  
	
		// perspective corrected projection
		gl_TexCoord[1].zw = gl_Position.w;
		gl_TexCoord[5].xy = (gl_Position.xy + gl_Position.w)*0.5;
		gl_TexCoord[5].zw =  vec2(1, gl_Position.w);
	
		// get tangent space basis    
		vec3 n = normalize(gl_NormalMatrix * gl_Normal);
		vec3 t = normalize(gl_NormalMatrix * Tangent);
		vec3 b = cross(n, t);

		// compute tangent space eye vector
		vec3 tmpVec = -vec3(gl_ModelViewMatrix * gl_Vertex);
		gl_TexCoord[0].x = dot(tmpVec, t);
		gl_TexCoord[0].y = dot(tmpVec, b);
		gl_TexCoord[0].z = dot(tmpVec, n);
	}
	"""
	
	frag = """
	uniform sampler2D water_normal;
	uniform sampler2D water_reflection;
	uniform sampler2D water_refraction;
	
	#define FADE_DIST 10.0
	
	void main(void)
	{
		vec3 vEye = normalize(gl_TexCoord[0].xyz);

		// Get bump layers
		vec3 vBumpTexA = texture2D(water_normal, gl_TexCoord[1].xy).xyz;
		vec3 vBumpTexB = texture2D(water_normal, gl_TexCoord[2].xy).xyz;
		vec3 vBumpTexC = texture2D(water_normal, gl_TexCoord[3].xy).xyz;
		vec3 vBumpTexD = texture2D(water_normal, gl_TexCoord[4].xy).xyz;

		// Average bump layers
		vec3 vBumpTex = normalize(2.0 * (vBumpTexA + vBumpTexB + vBumpTexC + vBumpTexD)-4.0);

		// Apply individual bump scale for refraction and reflection
		vec3 vRefrBump = vBumpTex * vec3(0.02, 0.02, 1.0);
		vec3 vReflBump = vBumpTex * vec3(0.1, 0.1, 1.0);

		// Compute projected coordinates
		vec2 vProj = (gl_TexCoord[5].xy/gl_TexCoord[5].w);
		vec4 vReflection = texture2D(water_reflection, vProj.xy + vReflBump.xy);
		vec4 vRefraction = texture2D(water_refraction, vProj.xy + vRefrBump.xy);

		// Compute Fresnel term
		float NdotL = max(dot(vEye, vReflBump), 0.0);
		float facing = (1.0 - NdotL);
		float fresnelBias = 0.2;
		float fresnelPow = 5.0;
		float fresnel = max(fresnelBias + (1.0-fresnelBias)*pow(facing, fresnelPow), 0.0);

		// Use distance to lerp between refraction and deep water color
		float fDistScale = clamp(FADE_DIST/gl_TexCoord[1].w,0.0,1.0);
		vec3 WaterDeepColor = (vRefraction.xyz * fDistScale + (1.0 - fDistScale) * vec3(0.0, 0.1, 0.125));  

		// Lerp between water color and deep water color
		vec3 WaterColor = vec3(0, 0.1, 0.15);
		vec3 waterColor = (WaterColor * facing + WaterDeepColor * (1.0 - facing));
		vec3 cReflect = fresnel * vReflection;

		// final water = reflection_color * fresnel + water_color
		gl_FragColor = vec4(cReflect + waterColor, 1);  
	}
	"""
	shader = viz.addShader(vert=vert,frag=frag)
	shader.attach( viz.addUniformInt('water_normal',0) )
	shader.attach( viz.addUniformInt('water_reflection',1) )
	shader.attach( viz.addUniformInt('water_refraction',2) )
	plane.apply(shader)
	
	#Apply reflection/refraction/normal texture to plane
	plane.texture(viz.add('art/waves.dds',wrap=viz.REPEAT),unit=0)
	plane.texture(reflectTex,unit=1)
	plane.texture(refractTex,unit=2)
	
	#Remove reflect mask from plane so it isn't drawn during reflect/refract stage
	plane.setMask(REFLECT_MASK,mode=viz.MASK_REMOVE)
	
addWaterReflection(waterPlane,HEIGHT)

effect = UnderwaterEffect() 
effect.setEnabled(viz.OFF)
vizfx.postprocess.addEffect(effect) 

bubble_num=580
groups_bubble=[]
bubble_radius=0.03
bubble_transpare=0.4

def create_bubble():
	for bbbbnum in range(bubble_num):
		pos_b_x=random.randint(-3000,3000)
		pos_b_y=random.randint(-1000,100)   
		pos_b_z=random.randint(-3000,3000)
		bubble = vizshape.addSphere(radius=bubble_radius,pos=(pos_b_x/100,pos_b_y/100-2,pos_b_z/100-75),color=(255,255,255),slices = 6,stacks = 6)		
		bubble.alpha(bubble_transpare)
		bubble.visible(viz.OFF)
		groups_bubble.append(bubble)
		obj_vis.append(bubble)

create_bubble()

def resetBubbles():
	for bubble in groups_bubble:
		bubble.setPosition([0,-30,0],viz.REL_LOCAL)
		bubble.setScale([0.1]*3)

def move_and_scale(): 	
	for m_b in range(bubble_num):
		groups_bubble[m_b].visible(viz.ON)
		bubble_pos=groups_bubble[m_b].getPosition(viz.ABS_GLOBAL)
		bubble_pos[1]=bubble_pos[1]+30.0
		action_bubble=vizact.moveTo(bubble_pos,speed=1)
		action_scale_bubble=vizact.sizeTo([10,10,10],time=30)
		groups_bubble[m_b].addAction(action_bubble,pool=11)
		groups_bubble[m_b].addAction(action_scale_bubble,pool=12)

def enableUnderWater():
	waterPlane.visible(viz.OFF)
	viz.fog(0.1) 
	viz.fogcolor( 0.7686 , 0.8745 , 0.8824 )
	effect.setEnabled(viz.ON)
	timer.setEnabled(viz.OFF)
	waterSound.stop()
	move_and_scale()

def waterRise():
	waterPlane.setPosition([0,0.005,0],viz.REL_LOCAL)
	viewHeight = viz.MainView.getPosition()[1]
	waterHeight = waterPlane.getPosition()[1]
	if waterHeight > (viewHeight-0.6):
		viz.sendEvent(WATER_RISE_EVENT) 

timer = vizact.ontimer(0,waterRise)
timer.setEnabled(viz.OFF)


#'''
#-------------------------------------------------add bubble behaviour------------------------



	
##---------------------------------------------add sphere around----------------------------------------------
#[-1.79732, 8.96285, -92.03959]


#----------------------------------------add the sphere behaviour----------------------------------------
##----------------------------------------------------------sphere one---------------------------------

#center_pos=([21.57,3.49,-15.08],[31.48,5.88,-11.97],[22.08,4.50,-1.641],[1.2,2,1],[-1.2,2,1])
center_pos=([-1.53117, 8.69384, -92.32681],[21.57,-30.49,-85.08])

center_num=len(center_pos)

groups_groups = []
groups_groups_sphere=[]
groups_groups_groups_sphere2=[]
group_num=3
group_trail_num=80
size_sphere_around=2.8
radius_sphere=0.52
tranparent=0.4

music=viz.addAudio('art/Lana Del Rey - Dark Paradise.wav')

grabObjects = []
for iii in range(center_num):
	
	mainSphere = vizshape.addSphere(radius=1.05,pos=center_pos[iii],color=viz.RED)
	mainSphere.alpha(0.01)
	
	grabObjects.append(mainSphere)
	obj_vis.append(mainSphere)

	groups=[]
	groups_groups.append(groups)
	
	groups_sphere=[]
	groups_groups_sphere.append(groups_sphere)
	
	groups_groups_sphere2=[]
	groups_groups_groups_sphere2.append(groups_groups_sphere2)

	for c in range(group_num):
		groups_sphere2=[]
		groups_groups_groups_sphere2[iii].append(groups_sphere2)
	
	for izx in range(group_num):
		
		rand_x = random.randint(-1,1)
		rand_y = random.randint(-1,1)
		rand_z = random.randint(-1,1)
		x = vizact.randfloat(-10,10)
		y = vizact.randfloat(-10,10)
		z = vizact.randfloat(-10,10)
		tmp_b_cen=(rand_x/size_sphere_around+0.0001,rand_y/size_sphere_around+0.0001,rand_z/size_sphere_around+0.0001)
	
		speed_r = random.randint(80,200)
		alpha_r = random.randint(30,80)
	
#    for itrail in range(12):
		sphere = vizshape.addSphere(radius=radius_sphere,pos=tmp_b_cen,color=(255,255,255),slices = 12,stacks =12)
		sphere.alpha(tranparent)
		sphere.emissive([1,1,1])
		obj_vis.append(sphere)
		
		
		for zzz in range(group_trail_num):
			sphere2 = vizshape.addSphere(radius=radius_sphere,pos=tmp_b_cen,color=(255,255,255),slices = 6,stacks = 6)
			sphere2.alpha(1)
			groups_groups_groups_sphere2[iii][izx].append(sphere2)
			sphere2.emissive([1,1,1])
			obj_vis.append(sphere2)
	
		group = viz.addGroup(parent=mainSphere)
		sphere.setParent(group)
		spinAction = vizact.spin(x,y,z,speed_r,viz.FOREVER)
		groups_groups[iii].append(group)
		groups_groups_sphere[iii].append(sphere)
	
		for z in range(len(groups)):
			groups[z].runAction(spinAction)
	
frame_count=0

def my_frame_cunction():
	global frame_count
	
	if frame_count>(group_trail_num-1):
		frame_count=0
	
	for ttt_g in range(center_num):
		for tmp_z in range(group_num):
			tmp_pos_pp=groups_groups_sphere[ttt_g][tmp_z].getPosition(viz.ABS_GLOBAL)
			groups_groups_groups_sphere2[ttt_g][tmp_z][group_trail_num-1-frame_count].setPosition(tmp_pos_pp)
			
			
			
			for tmp_x in range(group_trail_num):
				tmp_zzz=(tmp_x+frame_count)%group_trail_num
				groups_groups_groups_sphere2[ttt_g][tmp_z][tmp_zzz].alpha((tranparent*0.5)/group_trail_num*(group_trail_num-tmp_zzz))
				
	frame_count=frame_count+1            

updateHandle = vizact.onupdate(0,my_frame_cunction)

def getGrabObjects():
	return grabObjects

active = True
def setActive(value):
	global active
	if value == True:
		waterSound.play()
		waterSound.loop()
		choir_sound.play()
		waterPlane.setPosition([0,-2.0,0])
		for obj in obj_vis:
			obj.visible(viz.ON)
		active = True
	else:
		for obj in obj_vis:
			obj.visible(viz.OFF)
		effect.setEnabled(viz.OFF)
		updateHandle.setEnabled(viz.OFF)
		timer.setEnabled(viz.OFF)
		viz.fog(0)
		waterSound.stop()
		choir_sound.stop()
		vizact.ontimer2(35,0,resetBubbles)
		active = False
		
def getActive():
	return active