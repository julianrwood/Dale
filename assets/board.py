from pxr import Usd, UsdUtils, Sdf, UsdGeom, Gf, UsdShade
import numpy as np

class Board:
    def __init__(self, name, length, width, thickness, appFunctions):
        # Create a new stage
        self.stage = appFunctions.getSceneStage()

        # Define the root xform for organization
        root = UsdGeom.Xform.Define(self.stage, f"/world/geo/{name}")
        self.mesh = UsdGeom.Mesh.Define(self.stage, f"/world/geo/{name}")

        # Define the vertices for the cube (centered at origin)
        # Dimensions: 2400mm x 1200mm x 16mm
        # Define half dimensions for centering
        half_x = length / 2
        half_y = width / 2
        half_z = thickness / 2

        # Define the vertices for the cube
        points = [
            (-half_x, -half_y, -half_z),  # 0 Back Bottom Left
            (half_x, -half_y, -half_z),  # 1 Back Bottom Right
            (half_x, half_y, -half_z),  # 2 Back Top Right
            (-half_x, half_y, -half_z),  # 3 Back Top Left
            (-half_x, -half_y, half_z),  # 4 Front Bottom Left
            (half_x, -half_y, half_z),  # 5 Front Bottom Right
            (half_x, half_y, half_z),  # 6 Front Top Right
            (-half_x, half_y, half_z),  # 7 Front Top Left
        ]

        # Define the faces of the cube
        faces = [
            [0, 1, 2, 3],  # Back
            [4, 5, 6, 7],  # Front
            [0, 4, 7, 3],  # Left
            [1, 5, 6, 2],  # Right
            [0, 1, 5, 4],  # Bottom
            [3, 2, 6, 7],  # Top
        ]

        # Flatten the face indices
        face_vertex_indices = [i for face in faces for i in face]

        # Set vertex counts for each face (4 for quads)
        face_vertex_counts = [4] * len(faces)

        # Define UV coordinates for each vertex
        uvs = [
            (0, 0), (1, 0), (1, 1), (0, 1),  # Back
            (0, 0), (1, 0), (1, 1), (0, 1),  # Front
            (0, 0), (1, 0), (1, 1), (0, 1),  # Left
            (0, 0), (1, 0), (1, 1), (0, 1),  # Right
            (0, 0), (1, 0), (1, 1), (0, 1),  # Bottom
            (0, 0), (1, 0), (1, 1), (0, 1),  # Top
        ]

        # Set attributes on the mesh
        self.mesh.CreatePointsAttr([Gf.Vec3f(*p) for p in points])
        self.mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
        self.mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
        self.mesh.CreateExtentAttr([(-half_x, -half_y, -half_z), (half_x, half_y, half_z)])

        # Set UV coordinates as a primvar
        tex_coords = UsdGeom.PrimvarsAPI(self.mesh).CreatePrimvar(
            "st", Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.faceVarying
        )
        tex_coords.Set([Gf.Vec2f(*uv) for uv in uvs])

        material = UsdShade.Material.Define(self.stage, '/materials/tasiOak')

        pbrShader = UsdShade.Shader.Define(self.stage, '/materials/tasiOak/PBRShader')
        pbrShader.CreateIdAttr("UsdPreviewSurface")
        pbrShader.CreateInput("roughness", Sdf.ValueTypeNames.Float).Set(0.4)
        pbrShader.CreateInput("metallic", Sdf.ValueTypeNames.Float).Set(0.0)

        material.CreateSurfaceOutput().ConnectToSource(pbrShader.ConnectableAPI(), "surface")

        stReader = UsdShade.Shader.Define(self.stage, '/materials/tasiOak/stReader')
        stReader.CreateIdAttr('UsdPrimvarReader_float2')

        diffuseTextureSampler = UsdShade.Shader.Define(self.stage, '/materials/tasiOak/diffuseTexture')
        diffuseTextureSampler.CreateIdAttr('UsdUVTexture')
        diffuseTextureSampler.CreateInput('file', Sdf.ValueTypeNames.Asset).Set("/media/projects/python/draftAlot/ui/assets/textures/polytech/tasmanian-oak.jpg")
        diffuseTextureSampler.CreateInput("st", Sdf.ValueTypeNames.Float2).ConnectToSource(stReader.ConnectableAPI(),
                                                                                           'result')
        diffuseTextureSampler.CreateOutput('rgb', Sdf.ValueTypeNames.Float3)
        pbrShader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).ConnectToSource(
            diffuseTextureSampler.ConnectableAPI(), 'rgb')

        stInput = material.CreateInput('frame:stPrimvarName', Sdf.ValueTypeNames.Token)
        stInput.Set('st')

        stReader.CreateInput('varname', Sdf.ValueTypeNames.Token).ConnectToSource(stInput)

        self.mesh.GetPrim().ApplyAPI(UsdShade.MaterialBindingAPI)
        UsdShade.MaterialBindingAPI(self.mesh).Bind(material)

        # Save the stage
        self.stage.GetRootLayer().Save()
