# 平面图转模型
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def create_building_model(plan_curve, wall_thickness, wall_height):
    # 获取平面曲线的长度
    plan_length = rs.CurveLength(plan_curve)
    # 创建一个空的Brep
    building_brep = rg.Brep()
    # 遍历平面曲线的每个点
    for i in range(rs.CurvePointCount(plan_curve)):
        # 获取当前点的位置和切线
        point = rs.CurvePoint(plan_curve, i)
        tangent = rs.CurveTangent(plan_curve, i)
        # 创建当前点的墙面
        wall_srf = create_panel_surface(wall_thickness, wall_height, plan_length / rs.CurvePointCount(plan_curve), plan_curve)
        # 将墙面移动到当前点的位置
        rs.MoveObject(wall_srf, point)
        # 将墙面旋转到当前点的切线方向
        rs.RotateObject(wall_srf, tangent, point)
        # 将墙面添加到建筑Brep中
        building_brep = rg.Brep.CreateBooleanUnion([building_brep, wall_srf], 0.001)[0]
    return building_brep

# 测试代码
plan_curve = rs.GetObject("Select plan curve", rs.filter.curve)
wall_thickness = rs.GetReal("Enter wall thickness", 0.1)
wall_height = rs.GetReal("Enter wall height", 3.0)
building_model = create_building_model(plan_curve, wall_thickness, wall_height)
rs.AddBrepObject(building_model)