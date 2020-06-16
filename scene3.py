import viz
import vizact
import vizproximity
import vizfx
import vizact

scene3 = vizfx.addChild('art/scene3.osgb')
scene3.hint(viz.OPTIMIZE_INTERSECT_HINT)
#viz.clearcolor(viz.SLATE)

obj_vis = []
obj_vis.append(scene3)

scene3_music = viz.addAudio('art/scene3 paradise.wav')
scene3_music.volume(1)

# Get handle to starting_box object
starting_box = scene3.getChild('Starting Box-GEODE')
starting_box_height = 6.91645
starting_box.audio_start = viz.addAudio('sounds/platform_start.wav')
starting_box.audio_running = viz.addAudio('sounds/platform_running.wav',loop=True)
starting_box.audio_stop = viz.addAudio('sounds/platform_stop.wav')

wallHeights = [4.91645, 14.91645, 24.91645, 34.91645, 44.91645, 54.91645, 64.91645, 74.91645, 84.91645] 
leftWalls = []
rightWalls = []

def lowerWalls():
	for i in range(1,10):
		leftWallName = 'Left' + str(i) +'-GEODE'
		rightWallName = 'Right' + str(i) + '-GEODE'
		leftWall = scene3.getChild(leftWallName)
		rightWall = scene3.getChild(rightWallName)
		height = wallHeights[i-1]
		leftWall.setPosition([0,-height,0],viz.REL_LOCAL)
		rightWall.setPosition([0,-height,0],viz.REL_LOCAL)
		leftWalls.append(leftWall)
		rightWalls.append(rightWall)
	
walls = viz.addGroup(pos=[0,0,50])
walls.audio_running = viz.addAudio('sounds/pit_running.wav',loop=True)
walls.audio_stop = viz.addAudio('sounds/pit_stop.wav')
walls.audio_running.volume(0.5)
walls.audio_stop.volume(0.5)

def raiseWalls():
	for i, height in enumerate(wallHeights):
		leftWalls[i].runAction(vizact.move(0,2,0,time=(height/2)))
		rightWalls[i].runAction(vizact.move(0,2,0,time=(height/2)))
		if i == len(wallHeights) - 1:
			walls.audio_running.play()
			walls.runAction(vizact.move(0,2,0,time=(height/2)))
			walls.addAction(vizact.call(walls.audio_stop.play))
			walls.addAction(vizact.call(walls.audio_running.pause))

def lowerBox():
	starting_box.audio_start.stop()
	starting_box.audio_start.play()
	starting_box.audio_running.play()
	starting_box.runAction(vizact.move(0,-2,0,time=(starting_box_height/2)))
	starting_box.addAction(vizact.call(starting_box.audio_stop.play))
	starting_box.addAction(vizact.call(starting_box.audio_running.pause))	
		
def raiseBox():
	starting_box.setPosition([0,starting_box_height,0],viz.REL_LOCAL)

active = True
def setActive(value):
	global active
	if value == True:
		for obj in obj_vis:
			obj.visible(viz.ON)
		active = True
		scene3_music.play()
	else:
		lowerWalls()
		for obj in obj_vis:
			obj.visible(viz.OFF)
		active = False
		scene3_music.stop()

def getActive():
	return active

if __name__ == '__main__':
	viz.go()
	viz.MainView.getHeadLight().disable()
	vizact.onkeydown('1',lowerBox)
	vizact.onkeydown('2',raiseWalls)