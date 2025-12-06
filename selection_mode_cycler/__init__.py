import bpy

def cycle_selection_mode(forward=True):

    mode_types = ['VERT', 'EDGE', 'FACE']
    current_mode = None

    if bpy.context.tool_settings.mesh_select_mode[1]:
        current_mode = 'EDGE'
    elif bpy.context.tool_settings.mesh_select_mode[2]:
        current_mode = 'FACE'
    else:
        current_mode = 'VERT'

    current_index = mode_types.index(current_mode)

    if forward:
        next_index = (current_index + 1) % len(mode_types)
    else:
        next_index = (current_index - 1) % len(mode_types)  
        if next_index < 0:
            next_index += len(mode_types)

    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type=mode_types[next_index])

class CycleSelectionModeForwardOperator(bpy.types.Operator):
    bl_idname = "object.cycle_selection_mode_forward"
    bl_label = "Cycle Selection Mode Forward"

    @classmethod
    def poll(cls, context):
        return context.active_object != None or bpy.context.active_object.mode != 'EDIT'

    def execute(self, context):
        cycle_selection_mode(forward=True)
        return {'FINISHED'}

class CycleSelectionModeBackwardOperator(bpy.types.Operator):
    bl_idname = "object.cycle_selection_mode_backward"
    bl_label = "Cycle Selection Mode Backward"

    @classmethod
    def poll(cls, context):
        return context.active_object != None or bpy.context.active_object.mode != 'EDIT'

    def execute(self, context):
        cycle_selection_mode(forward=False)
        return {'FINISHED'}

def add_keymaps():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')

    kmi_forward = km.keymap_items.new(CycleSelectionModeForwardOperator.bl_idname, 'BUTTON5MOUSE', 'PRESS')
    kmi_backward = km.keymap_items.new(CycleSelectionModeBackwardOperator.bl_idname, 'BUTTON4MOUSE', 'PRESS')

    return (km, kmi_forward, kmi_backward)

def remove_keymaps(keymap_tuple):
    km, kmi_forward, kmi_backward = keymap_tuple
    km.keymap_items.remove(kmi_forward)
    km.keymap_items.remove(kmi_backward)
    bpy.context.window_manager.keyconfigs.addon.keymaps.remove(km)

keymap_tuple = None

def register():
    global keymap_tuple
    bpy.utils.register_class(CycleSelectionModeForwardOperator)
    bpy.utils.register_class(CycleSelectionModeBackwardOperator)
    keymap_tuple = add_keymaps()

def unregister():
    global keymap_tuple
    bpy.utils.unregister_class(CycleSelectionModeForwardOperator)
    bpy.utils.unregister_class(CycleSelectionModeBackwardOperator)
    if keymap_tuple:
        remove_keymaps(keymap_tuple)

if __name__ == "__main__":
    register()
