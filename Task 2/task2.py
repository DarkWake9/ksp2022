import bpy
import math
import numpy.random as rand 
import numpy as np
 
pi = np.pi

for material in bpy.data.worlds:
    material.user_clear()
    bpy.data.worlds.remove(material)

for material in bpy.data.materials:
    material.user_clear()
    bpy.data.materials.remove(material)
   
for material in bpy.data.lights:
    material.user_clear()
    bpy.data.lights.remove(material) 
    
for material in bpy.data.meshes:
    material.user_clear()
    bpy.data.meshes.remove(material)

#NOTSUN
notsun = bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.name = "notsun"
bpy.ops.transform.resize(value=(5.17778, 5.17778, 5.17778))



#SUN
sun = bpy.ops.mesh.primitive_uv_sphere_add(location = (0,0,0))
'''bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.time_limit = 0.01
bpy.context.scene.cycles.device = 'GPU'
'''

'''bpy.context.scene.eevee.use_bloom = True
bpy.context.scene.eevee.use_gtao = True
bpy.context.scene.eevee.use_ssr = True'''
bpy.ops.transform.resize(value=(5.17778, 5.17778, 5.17778))
bpy.context.object.name = "Sun"
sun = bpy.data.objects["Sun"]

sss = bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.object.shade_smooth()




bpy.ops.object.quick_smoke()
s_smoke = bpy.data.objects["Smoke Domain"]
bpy.ops.transform.resize(value=(1, 1, 0.8), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.resize(value=(1.0897016, 1.0897016, 1.0897016), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
bpy.ops.transform.translate(value=(-0, -0, -1), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

bpy.ops.object.effector_add(type='FORCE')
s_sforce = bpy.data.objects["Force"]

sun.modifiers["Fluid"].flow_settings.flow_type = 'FIRE'
sun.modifiers["Fluid"].flow_settings.surface_distance = 0.1

s_smoke.modifiers["Fluid"].domain_settings.flame_max_temp = 0
s_smoke.modifiers["Fluid"].domain_settings.flame_ignition = 0
s_smoke.modifiers["Fluid"].domain_settings.effector_weights.gravity = 0
s_smoke.modifiers["Fluid"].domain_settings.resolution_max = 64
s_smoke.modifiers["Fluid"].domain_settings.cache_frame_end = 799

s_sforce.field.strength = 20
s_sforce.field.flow = 2
s_sforce.field.noise = 1



s_mat = bpy.data.materials["Smoke Domain Material"]

nodes = s_mat.node_tree.nodes
links = s_mat.node_tree.links

s_op = nodes["Material Output"]
s_vol = nodes["Principled Volume"]


s_mat.node_tree.nodes["Principled Volume"].inputs[8].default_value = 1
s_mat.node_tree.nodes["Principled Volume"].inputs[7].default_value = (1, 0.254462, 0.0518582, 1)


satb = nodes.new(type = "ShaderNodeAttribute")
nodes["Attribute"].attribute_name = "flame"

smul = nodes.new(type = "ShaderNodeMath")
smul.operation = "MULTIPLY"

links.new(satb.outputs[2], smul.inputs[0])
links.new(smul.outputs[0], s_vol.inputs[6])

s_vol.inputs[10].default_value = 400
s_vol.inputs[2].default_value = 0
smul.inputs[1].default_value = 1.8

bpy.context.object.name = "Sun"
bpy.context.object.display_type = 'SOLID'

su_mat = bpy.data.materials.new(name = "smat")

su_mat.name = "smat"
su_mat.use_nodes = True 

nodes = su_mat.node_tree.nodes
links = su_mat.node_tree.links

su_op = nodes.get("Material Output")
su_bsdf = nodes.get("Principled BSDF")

#su_bsdf.inputs[9] = 1
links.new(su_bsdf.outputs[0], su_op.inputs[0])
#links.new(n_sun.outputs[0], s_bsdf.inputs[0])
if sun.data.materials: 
    sun.data.materials[0] = su_mat
else:
    sun.data.materials.append(su_mat)


sunti = nodes.new(type="ShaderNodeTexImage")
sunti.image = bpy.data.images.load("/home/darkwake/Videos/Blender-outputs/Task 2/2k_sun.jpg")

su_hs = nodes.new(type="ShaderNodeHueSaturation")
su_hs.inputs[0].default_value = 0.49
su_bp = nodes.new(type="ShaderNodeBump")
su_bp.inputs[0].default_value = 0.13

su_ntx = nodes.new(type="ShaderNodeTexNoise")
su_ntx.inputs[2].default_value = 45
su_ntx.inputs[3].default_value = 32

su_cr = nodes.new(type="ShaderNodeValToRGB")
su_crr = nodes["ColorRamp"].color_ramp
su_crr.elements.new(0.610)
su_crr.elements.new(0.687)
su_crr.elements.new(0.76)
su_crr.elements[0].position = 0.484
su_crr.elements[4].position = 0.842
su_crr.elements[1].color = (0.208794, 0, 0.000526887, 1)
su_crr.elements[2].color = (0.552541, 0.0890048, 0.000867319, 1)


su_crr.elements[3].color = (1, 0.651946, 0.0788165, 1)


su_mix = nodes.new(type="ShaderNodeMixRGB")
su_mix.blend_type = "ADD"

su_fl = nodes.new(type="ShaderNodeFresnel")
su_em = nodes.new(type="ShaderNodeEmission")
su_smx = nodes.new(type="ShaderNodeMixShader")
su_em.inputs[0].default_value = (1, 0.597093, 0.0649826, 1)
su_em.inputs[1].default_value = 5.1
su_fl.inputs[0].default_value = 1.08
su_bsdf.inputs[9].default_value = 1


 
links.new(su_ntx.outputs[1], su_cr.inputs[0])
links.new(sunti.outputs[0], su_bp.inputs[2])
links.new(sunti.outputs[0], su_hs.inputs[4])
links.new(su_hs.outputs[0], su_mix.inputs[1])
links.new(su_cr.outputs[0], su_mix.inputs[2])
links.new(su_mix.outputs[0], su_bsdf.inputs[0])
links.new(su_mix.outputs[0], su_bsdf.inputs[19])
links.new(su_bp.outputs[0], su_bsdf.inputs[22])
links.new(su_fl.outputs[0], su_smx.inputs[0])
links.new(su_bsdf.outputs[0], su_smx.inputs[1])
links.new(su_em.outputs[0], su_smx.inputs[2])
links.new(su_smx.outputs[0], su_op.inputs[0])

#sun.display_type = "SOLID"

#Background

wld=bpy.ops.world.new()
wld = bpy.data.scenes.data.worlds['World']
bpy.data.scenes['Scene'].world = wld
#wld = bpy.data.worlds["World"]

#bpy.data.scenes.world = wld
wld.use_nodes = True
wn = bpy.data.worlds[wld.name].node_tree.nodes
wl = bpy.data.worlds[wld.name].node_tree.links
#bpy.context.space_data.shader_type = 'WORLD'
#b1 = wn.new(type="ShaderNodeBackground")
#bbo = wn.new(type="ShaderNodeOutputWorld")
bb1 = wn["Background"]
bbo = wn["World Output"]
bbi = wn.new(type="ShaderNodeTexEnvironment")
bbi.image = bpy.data.images.load("/home/darkwake/Videos/Blender-outputs/Task 2/2k_stars_milky_way.jpg")
wl.new(bbi.outputs[0], bb1.inputs[0])
wl.new(bbi.outputs[0], bb1.inputs[0])
wl.new(bb1.outputs[0], bbo.inputs[0])

#bpy.ops.node.nw_add_texture()
#



#SUNLIGHT
bpy.ops.object.light_add(type='POINT', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
light = bpy.data.lights['Point']
light.name = "sunlight"
light.energy = 50000
light.shadow_soft_size = 7
light.color = (1, 0.865382, 0.503445)



###################################################################################

###################################################################################

#Earth
notearth = bpy.ops.object.empty_add(type='SPHERE', location=(0,0,0))
bpy.context.object.name = "notearth"
notearth = bpy.data.objects["notearth"]


cube = bpy.ops.mesh.primitive_uv_sphere_add(location = (0,0,0))
bpy.context.object.name = "Earth"
cube = bpy.data.objects["Earth"]

ss = bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.object.shade_smooth()


c_mat = bpy.data.materials.new(name = "mat")
c_mat.use_nodes = True 

nodes = c_mat.node_tree.nodes
links = c_mat.node_tree.links

m_op = nodes.get("Material Output")
bsdf = nodes.get("Principled BSDF")

n_earth = nodes.new(type="ShaderNodeTexImage")
n_earth.image = bpy.data.images.load("/home/darkwake/Videos/Blender-outputs/Task 2/2k_earth_daymap.jpg")

e_hs = nodes.new(type="ShaderNodeHueSaturation")
e_hs.inputs[0].default_value = 0.49
e_bp = nodes.new(type="ShaderNodeBump")
e_bp.inputs[0].default_value = 0.13
nodes["Principled BSDF"].inputs[20].default_value = 0


#cube.rotation_euler[0] = 23.5 * pi / 180.0

links.new(bsdf.outputs[0], m_op.inputs[0])
links.new(n_earth.outputs[0], e_bp.inputs[2])
links.new(n_earth.outputs[0], e_hs.inputs[4])
links.new(e_bp.outputs[0], bsdf.inputs[22])
links.new(e_hs.outputs[0], bsdf.inputs[0])
links.new(e_hs.outputs[0], bsdf.inputs[19])
#links.new(n_earth.outputs[0], bsdf.inputs[0])
if cube.data.materials: 
    cube.data.materials[0] = c_mat
else:
    cube.data.materials.append(c_mat)
#cube.data.materials[-1] = c_mat 

#notearth.parent = cube









#MOON
moon = bpy.ops.mesh.primitive_uv_sphere_add(location = (6, 0, 0))
bpy.ops.transform.resize(value=(0.27, 0.27, 0.27))
bpy.context.object.name = "moon"
moon = bpy.data.objects["moon"]
ss = bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.modifier_apply(modifier="Subdivision")
bpy.ops.object.shade_smooth()
moon.parent = bpy.data.objects["notearth"]
m_mat = bpy.data.materials.new(name = "mmat")
m_mat.use_nodes = True 

nodes = m_mat.node_tree.nodes
links = m_mat.node_tree.links

mm_op = nodes.get("Material Output")
m_bsdf = nodes.get("Principled BSDF")

n_moon = nodes.new(type="ShaderNodeTexImage")
n_moon.image = bpy.data.images.load("/home/darkwake/Videos/Blender-outputs/Task 2/2k_moon.jpg")

m_hs = nodes.new(type="ShaderNodeHueSaturation")
m_hs.inputs[0].default_value = 0.49
m_bp = nodes.new(type="ShaderNodeBump")
m_bp.inputs[0].default_value = 0.13
nodes["Principled BSDF"].inputs[20].default_value = 0

#cube.rotation_euler[0] = 23.5 * pi / 180.0

links.new(m_bsdf.outputs[0], mm_op.inputs[0])
links.new(n_moon.outputs[0], m_bp.inputs[2])
links.new(n_moon.outputs[0], m_hs.inputs[4])
links.new(m_bp.outputs[0], m_bsdf.inputs[22])
links.new(m_hs.outputs[0], m_bsdf.inputs[0])
links.new(m_hs.outputs[0], m_bsdf.inputs[19])
links.new(m_bsdf.outputs[0], mm_op.inputs[0])
#links.new(n_moon.outputs[0], m_bsdf.inputs[0])
if moon.data.materials: 
    moon.data.materials[0] = m_mat
else:
    moon.data.materials.append(m_mat)







frame_number = 0
#Motion
for i in range(0,41): 
       
    x = 15.2 * np.cos(i*pi/10.0)
    xr = np.deg2rad(i*pi/10.0) 
    y = 15.2 * np.sin(i*pi/10.0)
    z = 0
    xm = 19.2 * np.cos(i*pi/10.0) - 10 * np.cos(21.2*i*pi/60)
    ym = 19.2 * np.sin(i*pi/10.0) - 10 * np.sin(21.2*i*pi/60)
    cube = bpy.data.objects["Earth"]
    notearth = bpy.data.objects["notearth"]
    moon = bpy.data.objects["moon"]
    bpy.context.scene.frame_set(frame_number)     
    cube.location = (x, y, z)
    notearth.location = (x, y, z)
    cube.rotation_euler[2] = 1.5 * i * pi
    notearth.rotation_euler[2] = 2.7 * i * pi/10.0

    notearth.keyframe_insert(data_path = "location", index=-1)
    notearth.keyframe_insert(data_path = "rotation_euler", index=-1) 
    #moon.location = (xm, ym, 0) 
    moon.rotation_euler[2] = 2.7 * i * pi/10.0
    #moon.keyframe_insert(data_path = "location", index=-1)
    moon.keyframe_insert(data_path = "rotation_euler", index=-1)
    cube.keyframe_insert(data_path = "location", index=-1)
    cube.keyframe_insert(data_path = "rotation_euler", index=-1)
    frame_number+=20
    
    
    
   
#OUTPUTS

scene = bpy.data.scenes["Scene"]

scene.frame_end = 799

render = scene.render
render.resolution_x = 1920
render.resolution_y = 1080

render.filepath = "/home/darkwake/Videos/Blender-outputs/"

render.image_settings.file_format = 'FFMPEG'
render.ffmpeg.format = "MPEG4"
render.ffmpeg.constant_rate_factor = "PERC_LOSSLESS"
render.ffmpeg.gopsize = 20

bpy.ops.render.render(animation=True, write_still=True)