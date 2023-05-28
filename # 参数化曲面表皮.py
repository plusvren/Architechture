# 参数化曲面表皮
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def create_panel_surface(width, height, thickness, curve):
    # 创建一个矩形面
    rect = rg.Rectangle3d(rs.WorldXYPlane(), width, height)
    # 创建一个矩形曲面
    rect_srf = rg.Brep.CreateFromRectangle(rect.ToNurbsCurve(), thickness, False)
    # 将曲面移动到曲线上
    rs.MoveObject(rect_srf, rs.CurveStartPoint(curve) - rs.BoundingBox(rect_srf)[0])
    # 将曲面旋转到曲线的方向
    rs.RotateObject(rect_srf, rs.CurveTangent(curve, rs.CurveClosestPoint(curve, rs.BoundingBox(rect_srf)[0])), rs.CurveStartPoint(curve))
    # 将曲面拉伸到曲线的长度
    rs.ScaleObject(rect_srf, rs.CurveLength(curve) / width, 1, 1, rs.CurveStartPoint(curve))
    return rect_srf

def create_panel_mesh(width, height, thickness, curve):
    # 创建一个矩形网格
    rect = rg.Rectangle3d(rs.WorldXYPlane(), width, height)
    # 创建一个矩形曲面网格
    rect_mesh = rg.Mesh.CreateFromPlane(rect.Plane, rg.MeshingParameters.Default)
    # 将网格移动到曲线上
    rs.MoveObject(rect_mesh, rs.CurveStartPoint(curve) - rs.BoundingBox(rect_mesh)[0])
    # 将网格旋转到曲线的方向
    rs.RotateObject(rect_mesh, rs.CurveTangent(curve, rs.CurveClosestPoint(curve, rs.BoundingBox(rect_mesh)[0])), rs.CurveStartPoint(curve))
    # 将网格拉伸到曲线的长度
    rs.ScaleObject(rect_mesh, rs.CurveLength(curve) / width, 1, 1, rs.CurveStartPoint(curve))
    # 将网格转换为Brep
    rect_brep = rg.Mesh.ToBrep(rect_mesh)
    # 将Brep厚度拉伸
    rect_srf = rg.Brep.CreateFromOffsetFace(rect_brep.Faces[0], thickness, False, False)
    return rect_srf