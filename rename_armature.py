import bpy
import csv
import re
import os

class RenameArmatureOperator(bpy.types.Operator):
    bl_idname = "object.rename_armature"
    bl_label = "Rename Armature"
    
    def execute(self, context):
        # 获取选中的骨架对象
        armature_obj = context.active_object
        if armature_obj.type != 'ARMATURE':
            self.report({'ERROR'}, "Please select an armature object.")
            return {'CANCELLED'}
        
        # 获取用户选择的CSV文件路径
        csv_filepath = bpy.path.abspath(bpy.context.window_manager.rename_armature_csv_filepath)
        
        # 读取CSV文件
        with open(csv_filepath, 'r') as file:
            csv_data = csv.reader(file)
            csv_rows = list(csv_data)
        
        # 删除第一列非PmxBone的行
        csv_rows = [row for row in csv_rows if row[0] == 'PmxBone']
        
        # 重命名骨架
        armature = armature_obj.data
        for bone in armature.bones:
            # 提取骨骼名称中的序号
            match = re.search(r'No_(\d+)', bone.name)
            if match:
                bone_number = int(match.group(1))
                
                # 在CSV文件中查找对应的行号
                for i, row in enumerate(csv_rows):
                    if i == bone_number:
                        new_name = row[1]
                        bone.name = new_name
                        break
        
        return {'FINISHED'}

class RenameArmaturePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_rename_armature"
    bl_label = "Rename Armature"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.prop(context.window_manager, "rename_armature_csv_filepath", text="CSV File")
        
        row = layout.row()
        row.operator("object.rename_armature", text="Rename Armature")

def register():
    bpy.utils.register_class(RenameArmatureOperator)
    bpy.utils.register_class(RenameArmaturePanel)
    bpy.types.WindowManager.rename_armature_csv_filepath = bpy.props.StringProperty(subtype="FILE_PATH")

def unregister():
    bpy.utils.unregister_class(RenameArmatureOperator)
    bpy.utils.unregister_class(RenameArmaturePanel)
    del bpy.types.WindowManager.rename_armature_csv_filepath

if __name__ == "__main__":
    register()