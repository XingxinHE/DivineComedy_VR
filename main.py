import viz
import vizact
import viztask
import vizconnect
import vizproximity
import scene1
import scene2
import scene3

viz.setMultiSample(8)
vizconnect.go('vizconnect_config_desktop.py')
#vizconnect.go('vizconnect_config_vive.py')

grabTool = vizconnect.getRawTool('grabber')
grabTool.setItems(scene1.getGrabObjects())

vizact.onkeydown(' ',viz.setDebugSound3D,viz.TOGGLE)

CHANGE_SCENES_EVENT = viz.getEventID('CHANGE_SCENES') 

oriMode = vizconnect.VIEWPOINT_MATCH_DISPLAY
posMode = vizconnect.VIEWPOINT_MATCH_FEET

scene1_pos = [[0,0, -21.87243],[0,0,-46.27398],[0.4,0,-73],[-0.2, 2.6, -90]]
scene2_pos = [[0,0.1,0],[3, -3.2, 2.4],[10,-3,-4.73], [15,0.1,-1.73]]
scene2_ori = [[90,0,0], [110,0,0], [70,0,0], [90,0,0]]
scene3_pos = [[0,0,0], [0,0,30], [0,0,70],[0,0,180]]

vp1 = []
for pos in scene1_pos:
	vp = vizconnect.addViewpoint(pos=pos,
								euler=[180,0,0],
								oriMode = oriMode, 
								posMode = posMode)
	vp1.append(vp)
	
vp2 = []								
for i, pos in enumerate(scene2_pos):
	vp = vizconnect.addViewpoint(pos=pos,
								euler=scene2_ori[i],
								oriMode = oriMode, 
								posMode = posMode)
	vp2.append(vp)

vp3 = []								
for pos in scene3_pos:
	vp = vizconnect.addViewpoint(pos=pos,
								euler=[0,0,0],
								oriMode = oriMode, 
								posMode = posMode)
	vp3.append(vp)

display = vizconnect.getDisplay()

scene1.setActive(True)
scene2.setActive(False)
scene3.setActive(False)

# Create quad to signal jump
jump_signal = viz.addTexQuad(size=0.3, pos=[-1.5,-0.8,3])
jump_signal.visible(0)
jump_signal.setReferenceFrame(viz.RF_EYE)
jump_signal.disable([viz.LIGHTING, viz.INTERSECTION, viz.DEPTH_TEST, viz.SHADOW_CASTING])
jump_signal.drawOrder(100)
jump_texture = viz.addTexture('art/jump.png')
jump_signal.texture(jump_texture)

#jump_sound = viz.addAudio('art/jump_sound.wav')
#jump_sound.volume(0.8)
def jumpSignal():
#	jump_signal.visible(0)
	jump_signal.visible(1)
	jump_signal.runAction(vizact.fadeTo(0.8,begin=0,time=2))
	#jump_sound.play()


# Create quad for flashing screen during jump
jump_flash = viz.addTexQuad(size=100, pos=[0,0,1], color=viz.BLACK)
jump_flash.setReferenceFrame(viz.RF_EYE)
jump_flash.disable([viz.LIGHTING, viz.INTERSECTION, viz.DEPTH_TEST, viz.SHADOW_CASTING])
jump_flash.blendFunc(viz.GL_ONE, viz.GL_ONE)
jump_flash.drawOrder(100)
jump_flash.visible(False)

def jumpFlash():
	# Display jump flash
	jump_flash.visible(True)
	jump_flash.runAction(vizact.fadeTo(viz.BLACK, begin=viz.WHITE, time=2.0, interpolate=vizact.easeOutStrong))
	jump_flash.addAction(vizact.method.visible(False))


waitKey1 = viztask.waitKeyDown('1')
waitKey2 = viztask.waitKeyDown('2')
wait10 = viztask.waitTime(5)
waitJumpTime = 5

def scenesTask():
	
	while True:
		
		# Scene 1 events
		vp1[0].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp1[0].remove(display)
		vp1[1].add(display)
		vizconnect.resetViewpoints()
		scene1.waterSound.volume(0.05)
		scene1.choir_sound.minmax(0,3)
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		scene1.waterSound.volume(0.2)
		scene1.choir_sound.minmax(5,15)
		jumpFlash()
		vp1[1].remove(display)
		vp1[2].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp1[2].remove(display)
		vp1[3].add(display)
		vizconnect.resetViewpoints()
		scene1.timer.setEnabled(viz.ON)
		yield viztask.waitEvent(scene1.WATER_RISE_EVENT)
		yield scene1.BlurTask()
		scene1.enableUnderWater()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		manager.removeSensor(scene1.stoneSensor)
		jumpFlash()
		vp1[3].remove(display)
		
		# Scene 2 events
		scene1.setActive(False)
		scene2.setActive(True)
		grabTool.setItems(scene2.getGrabObjects())
		vp2[0].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp2[0].remove(display)
		vp2[1].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp2[1].remove(display)
		vp2[2].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp2[2].remove(display)
		vp2[3].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		vp2[3].remove(display)
				
		# Scene 3 events
		scene2.setActive(False)
		scene3.setActive(True)
		vp3[0].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitAny([waitKey1,wait10])
		scene3.lowerBox()
		yield viztask.waitAny([waitKey2,wait10])
		scene3.raiseWalls()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp3[0].remove(display)
		vp3[1].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp3[1].remove(display)
		vp3[2].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		jumpFlash()
		vp3[2].remove(display)
		vp3[3].add(display)
		vizconnect.resetViewpoints()
		yield viztask.waitTime(waitJumpTime)
		jumpSignal()
		yield viztask.waitEvent(CHANGE_SCENES_EVENT)
		jump_signal.visible(0)
		vp3[3].remove(display)
		scene3.setActive(False)
		scene3.raiseBox()
		scene1.setActive(True)
		
viztask.schedule( scenesTask() )

# Proximity code
manager = vizproximity.Manager()

# Add main viewpoint as proximity target
target = vizproximity.Target(viz.MainView)
manager.addTarget(target)

# Add scene1 proximity sensor
manager.addSensor(scene1.stoneSensor)

scaleAction = vizact.sequence([vizact.sizeTo(size=[1.3,1.3,1.3],time=1),vizact.sizeTo(size=[1,1,1],time=1)], viz.FOREVER)
fadeAction = vizact.sequence([vizact.fadeTo([0.63,0.32,0.18],time=2),vizact.fadeTo(viz.WHITE,time=2)], viz.FOREVER)

def onGrab(e):
	e.grabbed.runAction(fadeAction,pool=1)
	e.grabbed.runAction(scaleAction,pool=2)    
	if scene2.getActive():
		scene2.music.play()
		viz.window.setPolyMode(viz.POLY_POINT)

	
def onRelease(e):
	e.released.endAction(pool=viz.ALL_POOLS)
	pos=viz.MainView.getPosition()
	action=vizact.moveTo(pos,speed=0.5)
	e.released.addAction(action)
	
	
	viz.window.setPolyMode(viz.POLY_FILL)
#	vizact.ontimer2(5,0,viz.window.setPolyMode,viz.POLY_FILL)
	

from tools import grabber
viz.callback(grabber.GRAB_EVENT, onGrab)
viz.callback(grabber.RELEASE_EVENT, onRelease)