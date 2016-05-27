import pymel.core as pm
import maya.cmds as mc

""" https://github.com/BigRoy/mayaVrayCommandDocs/wiki/vray-addAttributesFromGroup """


# For Mesh
class vrayAttrActivation():
    def __init__(self):
        
        # Default values on init                    
        self.selObjs = None
        self.objIDOn = 0
        self.objIDVal = None
        self.useAttrOn = 0
        self.useAttrVal = None
        self.matIDOn = 0
        self.matIDVal = None
        self.matIDCol = None
        
        
        if mc.window('vrayAttr', exists = True): 
            mc.deleteUI('vrayAttr') 
        
        mc.window( 'vrayAttr', t = "Set Vray Attribute", iconName = 'Vray Attrs', w = 220 )
        mc.rowColumnLayout( nc = 1, cal = [1, 'left'], rs = [1, 7], cs = [1, 20], cw = [1, 180] )
        
        mc.separator( st = 'none', h = 17 )
        
        # Set Selected Objects to selObjs variable
        mc.button( l = 'Select Objects', c = self.selectObjects, w = 50 )
        
        mc.separator( h = 25, st = 'in' )
        
        # Enable and set Vray ObjectID
        self.guiObjIDOn = mc.checkBox( l = 'Object ID' )        
        mc.text( l = 'Object ID Value' )
        self.guiObjIDVal = mc.textField( )
        
        mc.separator( h = 25, st = 'in' )
        
        # Enable and set Vray User Attributes        
        self.guiUseAttrOn = mc.checkBox( l = 'User attributes' )       
        mc.text( l = 'Enter User attributes' )
        self.guiUseAttrVal = mc.textField( )
        
        mc.separator( h = 25, st = 'in' )
        
        # Enable and set Vray Material ID
        self.guiMatIDOn = mc.checkBox( l = 'Material ID' )        
        mc.text( l = 'Multimatte ID' )
        
        self.guiMatIDVal = mc.textField( )
        mc.text( l = 'Material ID' )

        self.guiMatIDCol = mc.radioCollection()
        mc.radioButton('red', label='Red' )
        mc.radioButton('green', label='Green' )
        mc.radioButton('blue', label='Blue' )
        mc.radioButton('white', label='White' )
        mc.radioButton('black', label='Black' )
                
        mc.separator( h = 25, st = 'in' )
        
        # Activate on Geo or Material
        mc.button( l = 'Apply Settings to Geometry', c = self.vrayMeshAttrSet, w = 50 )
        mc.separator( st = 'none' )
        mc.button( l = 'Apply Settings to Materials', c = self.vrayMtrlIDSet, w = 50 )
        mc.separator( st = 'none', h = 17 )
        
        
        mc.showWindow( )
    
    def selectObjects(self, *args):
        """ Saves all Selected items - geo or material - to selObjs variable. """
        self.selObjs = pm.selected()


    def evalAttrOns(self, *args):
        """ Quereies and returns values from the GUI. """
        
        # Object ID
        self.objIDOn = mc.checkBox( self.guiObjIDOn, q = 1, v = 1 )
        self.objIDVal = mc.textField( self.guiObjIDVal, q = 1, tx = 1 )
        
        # User Attributes
        self.useAttrOn = mc.checkBox( self.guiUseAttrOn, q = 1, v = 1 )        
        self.useAttrVal = mc.textField( self.guiUseAttrVal, q = 1, tx = 1 )
        
        # Material ID
        self.matIDOn = mc.checkBox( self.guiMatIDOn, q = 1, v = 1 )
        self.matIDVal = mc.textField( self.guiMatIDVal, q = 1, tx = 1 )
        self.matIDCol = mc.radioCollection( self.guiMatIDCol, q = 1, sl = 1 ) 
        

    def vrayMeshAttrSet(self, *args):
        """ 
            Applies Vray attributes to selected geometry. 
            (Will not effect materials if also included in the selected objects.) 
        
        """
        
        self.evalAttrOns()

        for obj in self.selObjs:
            #print obj.type()
           
            if (obj.type() == 'transform'):
                objShape = obj.getShape()    
                
                
                # Object ID
                if self.objIDOn:
                    pm.vray("addAttributesFromGroup", obj, "vray_objectID", 1)
                    pm.vray("addAttributesFromGroup", objShape, "vray_objectID", 1)
                    if self.objIDVal is not None:
                        if self.objIDVal.isdigit():
                            obj.attr('vrayObjectID').set(int(self.objIDVal))
                            objShape.attr('vrayObjectID').set(int(self.objIDVal))
                else:
                    pm.vray("addAttributesFromGroup", obj, "vray_objectID", 0)
                    pm.vray("addAttributesFromGroup", objShape, "vray_objectID", 0)
    
                # User Attribute
                if self.useAttrOn:
                    pm.vray("addAttributesFromGroup", obj, "vray_user_attributes", 1)
                    pm.vray("addAttributesFromGroup", objShape, "vray_user_attributes", 1)
                    if self.useAttrVal is not None:
                        obj.attr('vrayUserAttributes').set('%s' % self.useAttrVal)
                        objShape.attr('vrayUserAttributes').set('%s' % self.useAttrVal)
                else:
                    pm.vray("addAttributesFromGroup", obj, "vray_user_attributes", 0)
                    pm.vray("addAttributesFromGroup", objShape, "vray_user_attributes", 0)
    
                
                # Multimatte Color and Material ID 
                if self.matIDOn:
                    pm.vray("addAttributesFromGroup", obj, "vray_material_id", 1)
                    pm.vray("addAttributesFromGroup", objShape, "vray_material_id", 1)
                    self.setMatteColor(obj, self.matIDCol)
                    self.setMatteColor(objShape, self.matIDCol)
                    if self.matIDVal is not None:
                        if self.matIDVal.isdigit():
                            obj.attr('vrayMaterialId').set(int(self.matIDVal))
                            objShape.attr('vrayMaterialId').set(int(self.matIDVal))
                else:
                    pm.vray("addAttributesFromGroup", obj, "vray_material_id", 0)
                    pm.vray("addAttributesFromGroup", objShape, "vray_material_id", 0)
    
                
                # All Other Attributes - To be built into GUI later...
                # pm.vray("addAttributesFromGroup", geoShape, "vray_subdivision", 0)
                # pm.vray("addAttributesFromGroup", geoShape, "vray_subquality", 0)
                # pm.vray("addAttributesFromGroup", geoShape, "vray_displacement", 0)
                # pm.vray("addAttributesFromGroup", geoShape, "vray_roundedges", 0)


    def vrayMtrlIDSet(self, *args):
        """ 
            Applies Vray attributes to selected materials. 
            (Will not effect geometry if also included in the selected objects.) 
        
        """
        
        self.evalAttrOns()
        
        for obj in self.selObjs:
            if (obj.type() == 'VRayMtl'):
                
                # Multimatte Color and Material ID
                if self.matIDOn:
                    pm.vray("addAttributesFromGroup", obj, "vray_material_id", 1)
                    pm.vray("addAttributesFromGroup", objShape, "vray_material_id", 1)
                    self.setMatteColor(obj, self.matIDCol)
                    self.setMatteColor(objShape, self.matIDCol)
                    if self.matIDVal is not None:
                        if self.matIDVal.isdigit():
                            obj.attr('vrayMaterialId').set(int(self.matIDVal))
                            objShape.attr('vrayMaterialId').set(int(self.matIDVal))
                else:
                    pm.vray("addAttributesFromGroup", obj, "vray_material_id", 0)
                    pm.vray("addAttributesFromGroup", objShape, "vray_material_id", 0)
                
    
    def setMatteColor(self, obj = None, idCol = None, *args):
        """ Sets Multimatte Color based on selection. """
        
        if (idCol == 'red'):
            # Red
            obj.attr('vrayColorId').set(1, 0, 0)
        elif (idCol == 'green'):
            # Blue
            obj.attr('vrayColorId').set(0, 1, 0)
        elif (idCol == 'blue'):
            # Green
            obj.attr('vrayColorId').set(0, 0, 1)
        elif (idCol == 'black'):
            # Black
            obj.attr('vrayColorId').set(0, 0, 0)
        elif (idCol == 'white'):
            # Black
            obj.attr('vrayColorId').set(1, 1, 1)
        else:    
            # Black
            obj.attr('vrayColorId').set(0, 0, 0)


allObjs = vrayAttrActivation()
