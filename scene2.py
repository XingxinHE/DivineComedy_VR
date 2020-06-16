import viz
import vizfx
import vizact
import vizshape
import random

obj_vis = []
scene2 = viz.addChild('art/scene2.osgb')
#scene2 = vizfx.addChild('scene2.osgb')
scene2.hint(viz.ALLOW_NPOT_TEXTURE_HINT)
obj_vis.append(scene2)

#vizact.ontimer2(3.0,viz.window.setPolyMode,viz.POLY_POINT)

##--------------------------------------------add the direction light---------------------------------
#mylight = vizfx.addSpotLight()
mylight = viz.addLight()
mylight.position(0,0,0) 
mylight.direction(0,0,1) 
mylight.spread(30) 
mylight.intensity(1.5)

def set_vie_with_position():
    my_light_pos=viz.MainView.getPosition()
    my_light_euler=viz.MainView.getEuler()
    
    mylight.setPosition(my_light_pos[0],my_light_pos[1],my_light_pos[2])
    mylight.setEuler(my_light_euler[0],my_light_euler[1],my_light_euler[2])


updateLight = vizact.onupdate(0,set_vie_with_position)

#------------------------------------------------add the direction light------------------------------------




#----------------------------------------add the sphere behaviour----------------------------------------
##----------------------------------------------------------sphere one---------------------------------


center_pos=([2.93414, 1.54399, 0.42421],
[3.55752, 0.85784, -3.36570],
[5.35982, 0.66285, -1.46127],
[8.87976, 0.83787, -3.06492],
[6.42717, 1.45201, -6.80490],
[10.99663, 1.60214, 2.41580],
[8.13910, 0.88974, 4.26806],
[10,-1.4,-4.23],
[16.99663, 1.50214, -1.3241580],
[23.42136, 2.83873, -2.73446])



center_num=len(center_pos)

groups_grbber=[]


groups_groups = []
groups_groups_sphere=[]
groups_groups_groups_sphere2=[]
group_num=8
group_trail_num=30
#size_sphere_around=15.0
#radius_sphere=0.02


size_main_sphere=0.05
size_sphere_around=8.0
radius_sphere=0.08

larger_ball_main_r=2.0

larger_ball_around=2.0
larger_ball_sphere2=0.70




tranparent=0.4

#grabber = vizconnect.getRawTool('grabber')

#music= viz.addAudio('art/beijing.wav')
#music_scene2_keep=viz.addAudio('art/Lana Del Rey - Dark Paradise.wav')

music= viz.addAudio('art/scene2-ghost.wav')
music_scene2_keep=viz.addAudio('art/scene2 horror.wav')

grabObjects = []

for iii in range(center_num): 
    tmp_main_radius=size_main_sphere
    if iii==center_num-1:
        tmp_main_radius=larger_ball_main_r

    
    mainSphere = vizshape.addSphere(radius=tmp_main_radius,pos=center_pos[iii],color=viz.RED)
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
    
#	 xc=(1,0,1,0,1,1)
#    yc=(0,1,1,0,1,1)
#    zc=(1,1,0,1,0,0)

    for izx in range(group_num):
        
        tmp_radius=radius_sphere
        tmp_sphere_around=size_sphere_around
        
        
        if iii==center_num-1:
            tmp_radius=larger_ball_sphere2
            tmp_sphere_around=larger_ball_around
        
        
        rand_x = random.randint(-1,1)
        rand_y = random.randint(-1,1)
        rand_z = random.randint(-1,1)
        x = vizact.randfloat(-10,10)
        y = vizact.randfloat(-10,10)
        z = vizact.randfloat(-10,10)
        tmp_b_cen=(rand_x/tmp_sphere_around+0.0001,rand_y/tmp_sphere_around+0.0001,rand_z/tmp_sphere_around+0.0001)
    
        speed_r = random.randint(80,200)
        alpha_r = random.randint(30,80)
    
#    for itrail in range(12):
        sphere = vizshape.addSphere(radius=tmp_radius,pos=tmp_b_cen,color=(120,0,0),slices = 6,stacks = 6)
        sphere.alpha(tranparent)
        sphere.emissive([1,0,0])
        
    
        
        for zzz in range(group_trail_num):
            sphere2 = vizshape.addSphere(radius=tmp_radius,pos=tmp_b_cen,color=(120,0,0),slices = 6,stacks = 6)
            sphere2.alpha(1)
            groups_groups_groups_sphere2[iii][izx].append(sphere2)
            sphere2.emissive([1,0,0])
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

updateFrame = vizact.onupdate(0,my_frame_cunction)

def getGrabObjects():
    return grabObjects

active = True
def setActive(value):
    global active
    if value == True:
        music_scene2_keep.play()
        music_scene2_keep.loop()
        for obj in obj_vis:
            obj.visible(viz.ON)
        mylight.enable()
        viz.MainView.getHeadLight().disable()
        updateLight.setEnabled(viz.ON)
        updateFrame.setEnabled(viz.ON)
        active = True
    else:
        for obj in obj_vis:
            obj.visible(viz.OFF)
        mylight.disable() 
        updateLight.setEnabled(viz.OFF)
        updateFrame.setEnabled(viz.OFF)
        music.stop()
        music_scene2_keep.stop()
        active = False
        
def getActive():
	return active