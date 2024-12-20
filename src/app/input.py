import util

from enum   import Enum
from typing import Callable

class Operator(Enum):
    LESS       = 0
    LESS_EQ    = 1
    GREATER    = 2
    GREATER_EQ = 3
    EQ         = 4

def input_color() -> util.Color:
    util.print_output('请任选一种格式输入颜色值:')
    util.print_ps('分量格式: 255,255,255')
    util.print_ps('十六进制格式: #FFFFFF')
    ans = util.get_input().strip()
    c   = ans if ans.startswith('#') else tuple(map(int, ans.split(',')))
    c   = util.Color(c)
    util.print_output('请任选一种格式输入不透明度:')
    util.print_ps('百分比格式: 100%')
    util.print_ps('十进制格式: 255')
    util.print_ps('十六进制格式: #FF')
    ans = util.get_input().strip()
    if   ans.endswith('%'):
        opc = int(ans[:-1]) / 100 * 255
    elif ans.startswith('#'):
        opc = int(ans[1:], 16)
    else:
        opc = int(ans)
    if opc < 0 or opc > 255:
        raise ValueError(f'非法不透明度值: \'{ans}\'.')
    c._a = int(opc)
    return c

IntLimit   = tuple[int,   bool]
FloatLimit = tuple[float, bool]

def input_int(lLimit: IntLimit = None, uLimit: IntLimit = None) -> int:
    value = int(util.get_input())
    if lLimit != None and (value < lLimit[0] if lLimit[1] else value <= lLimit[0]) or \
       uLimit != None and (value > uLimit[0] if uLimit[1] else value >= uLimit[0]):
        raise ValueError(f'非法的整数值: {value}.')
    return value

def input_float(lLimit: FloatLimit = None, uLimit: FloatLimit = None) -> float:
    value = float(util.get_input())
    if lLimit != None and (value < lLimit[0] if lLimit[1] else value <= lLimit[0]) or \
       uLimit != None and (value > uLimit[0] if uLimit[1] else value >= uLimit[0]):
        raise ValueError(f'非法的浮点数值: {value}.')
    return value

IntRange   = tuple[Operator, int]
FloatRange = tuple[Operator, float]

def _range_to_predicate(range: tuple) -> Callable:
    if range == None:
        return lambda v: True
    if range[0] == Operator.LESS:
        return lambda v: v < range[1]
    if range[0] == Operator.LESS_EQ:
        return lambda v: v <= range[1]
    if range[0] == Operator.GREATER:
        return lambda v: v > range[1]
    if range[0] == Operator.GREATER_EQ:
        return lambda v: v >= range[1]
    if range[0] == Operator.EQ:
        return lambda v: v == range[1]

def input_int_coordinate(xRange: IntRange = None, yRange: IntRange = None) -> tuple[int, int]:
    ans = list(map(int, util.get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'非法的整数坐标值: \'{ans}\'.')
    x_pre = _range_to_predicate(xRange)
    y_pre = _range_to_predicate(yRange)
    if not x_pre(ans[0]) or not y_pre(ans[1]):
        raise ValueError(f'非法的整数坐标值: \'{ans}\'.')
    return tuple(ans)

def input_float_coordinate(xRange: FloatRange = None, yRange: FloatRange = None) -> tuple[float, float]:
    ans = list(map(float, util.get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'非法的浮点数坐标值: \'{ans}\'.')
    x_pre = _range_to_predicate(xRange)
    y_pre = _range_to_predicate(yRange)
    if not x_pre(ans[0]) or not y_pre(ans[1]):
        raise ValueError(f'非法的浮点数坐标值: \'{ans}\'.')
    return tuple(ans)

def input_size(xRange: FloatRange = None, yRange: FloatRange = None) -> tuple:
    ans = list(map(str, util.get_input().split(',')))
    if len(ans) != 2:
        raise ValueError(f'非法的尺寸值: \'{ans}\'.')
    for i in range(2):
        ans[i] = ans[i].strip()
    
    if not ans[0] == '*':
        x_pre = _range_to_predicate(xRange)
        ans[0] = int(ans[0])
        if not x_pre(ans[0]):
            raise ValueError(f'非法的尺寸值分量: \'{ans[0]}\'.')
    if not ans[1] == '*':
        y_pre = _range_to_predicate(yRange)
        ans[1] = int(ans[1])
        if not y_pre(ans[1]):
            raise ValueError(f'非法的尺寸值分量: \'{ans[1]}\'.')
    return tuple(ans)

def input_valid_sequence(source: list[str]) -> tuple[str]:
    ans = util.get_input().strip().split()
    add = set()
    for effect in ans:
        if effect not in source:
            raise ValueError(f'非法的输入值: \'{effect}\'.')
        add.add(effect)
    if len(add) != 3:
        raise ValueError('错误的输入值分量: 缺少值或值重复.')
    return tuple(ans)
