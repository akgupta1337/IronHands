import bpy
import math

context = bpy.context.copy()

for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        context['area'] = area
        bpy.ops.screen.screen_full_area(context, use_hide_panels=True)
        bpy.context.space_data.show_gizmo = False
        bpy.context.space_data.overlay.show_overlays = False
# Get the active object (you may need to adjust this based on your needs)
obj = bpy.context.active_object

# Specify complete file path for this repo
new_path = "E:\\IronHands"
while True:
    
    with open("new_path\\scale.txt", 'r') as file:
        # Read the scale factor from the file
        scale_factor = (file.read().strip())
        if scale_factor == "NULL":
            break
        if scale_factor != '':
            scale_factor = float(scale_factor)
            obj.scale.x = scale_factor
            obj.scale.y = scale_factor
            obj.scale.z = scale_factor
    with open("new_path\\rotate.txt","r") as file:
        s = file.read().strip()
        if s != '':
            rotation_angle_degrees = float(s) 
            # Convert the rotation angle to radians
            rotation_angle_radians = math.radians(rotation_angle_degrees)

            # Rotate the object around the Z-axis
            obj.rotation_euler[2] += rotation_angle_radians
    with open("new_path\\pan.txt","r") as file:
        try:
            s = file.read().split(" ")
            if s[0] == "NULL":
                break
            if s and s != '' and s != ' ':
                x = (float(s[0]))
                z = (float(s[1]))  
                obj.location = (x,0.0,z)
        except Exception:
            continue
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
