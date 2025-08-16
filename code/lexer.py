import ply.lex as lex

# 文件所有注释均为上注释或后注释
# 如果遇到其他情况请 issue 或直接 pr

class BaoLexer:
    # token 列表
    tokens = [
        # 关键字
        'KEYWORD',      # 关键字的总和
        # 'IF',           # if 语句 条件判断
        # 'ELSE',         # else 语句 通常与 if 配合使用

        # 执行块标记
        'EXEC_START',   # 执行块开始标记 {%
        'EXEC_END',     # 执行块结束标记 %}

        # 运算符
        'ASSIGN',       # 赋值运算符 =
        'PLUS',         # 加法运算符 +
        'MINUS',        # 减法运算符 -
        'TIMES',        # 乘法运算符 *
        'DIVIDE',       # 除法运算符 /
        'MODULO',       # 取模（求余数）运算符 %
        'POWER',        # 幂运算运算符 **

        # 比较运算符
        'EQ',           # 等于 ==
        'NE',           # 不等于 !=
        'GT',           # 大于 >
        'LT',           # 小于 <
        'GE',           # 大于等于 >=
        'LE',           # 小于等于 <=

        # 逻辑运算符
        'AND',          # 逻辑与 &&
        'OR',           # 逻辑或 ||
        'NOT',          # 逻辑非 !

        # 标点符号
        'QUESTION',     # 问号
        # 'COLON',        # 冒号
        'SEMICOLON',    # 分号 结束一个语句
        'LPAREN',       # 左括号 (
        'RPAREN',       # 右括号 )
        'LBRACE',       # 左大括号 {
        'RBRACE',       # 右大括号 }
        'LBRACKET',     # 左中括号 [
        'RBRACKET',     # 右中括号 ]
        'COMMA',        # 逗号 ,

        # 字面量和变量类型
        'NUMBER',       # 数字字面量 例如 123 或 3.14
        'STRING_SINGLE',# 单引号字符串 例如 'hello'
        'STRING_DOUBLE',# 双引号字符串 例如 "world"
        'STRING_BACK',  # 反引号字符串 例如`template`
        
        # 变量
        'IDENTIFIER',     # 所有类型的变量都在一起
        # 'TEMP_VAR',     # 临时变量 ($t)
        # 'PERSONAL_VAR', # 个人变量 ($m)
        # 'GROUP_VAR',    # 群变量 ($g)
        # 'BUILTIN_VAR',  # 内置变量
        # 'CONSTANT_VAR', # 无前缀变量

        # 特殊类型
        'CUSTOM_TEXT',  # 自定义文本
        'DICE',         # 骰子表达式
        'DRAW',         # 牌堆表达式
        'ENDEL'         # 换行符

        # 内置变量 - 玩家和账号信息
        'BUILTIN_PLAYER',              # 当前人物卡名 不存在则为群或 QQ 昵称
        'BUILTIN_PLAYER_RAW',          # 同上 但不含<>
        'BUILTIN_QQ_NICKNAME',         # QQ 昵称
        'BUILTIN_ACCOUNT_ID',          # 海豹格式的账号 ID 如 QQ:123456789
        'BUILTIN_ACCOUNT_ID_RAW',      # 原始格式的账号 ID 如 123456789
        'BUILTIN_QQ',                  # 海豹格式的账号 ID 同 $t账号 ID
        # 内置变量 - 群组信息
        'BUILTIN_GROUP_NAME',          # 群名
        'BUILTIN_GROUP_ID',            # 海豹格式的群 ID 如 QQ-Group:987654321
        'BUILTIN_GROUP_ID_RAW',        # 原始格式的群 ID 如 987654321
        # 内置变量 - 时间信息
        'BUILTIN_DATE',                # 数字格式的日期 如 20230109
        'BUILTIN_YEAR',                # 数字格式的年份 如 2023
        'BUILTIN_MONTH',               # 数字格式的月份 如 1
        'BUILTIN_DAY',                 # 数字格式的日期 如 9
        'BUILTIN_WEEKDAY',             # 数字格式的星期（1-7）
        'BUILTIN_HOUR',                # 数字格式的小时
        'BUILTIN_MINUTE',              # 数字格式的分钟
        'BUILTIN_SECOND',              # 数字格式的秒
        'BUILTIN_TIMESTAMP',           # 10 位时间戳
        # 内置变量 - 消息和环境信息
        'BUILTIN_TEXT_LENGTH',         # 消息文本长度 汉字长度为 3
        'BUILTIN_PLATFORM',            # 触发平台 如 QQ
        'BUILTIN_GAME_MODE',           # 游戏模式 如 coc7 或 dnd
        'BUILTIN_MESSAGE_TYPE',        # 消息类型 'group' 或 'private'
        'BUILTIN_MESSAGE_ID',          # 消息 ID 仅自定义回复可用
        'BUILTIN_PERSONAL_DICE_SIDES', # 个人骰子面数
        'BUILTIN_LOG_ON',              # 日志是否开启 true 或 false
        # 内置变量 - 娱乐和常量
        'BUILTIN_TODAY_LUCK',          # 今日人品
        'BUILTIN_CONSTANT_APPNAME',    # 软件名 SealDice
        'BUILTIN_CONSTANT_VERSION'     # 版本号 如 1.5.0-dev
    ]

    def __init__(self):
        # 保留字字典 处理关键字和标识符的冲突
        self.reserved = {
            'if': 'IF',
            'else': 'ELSE'
        }

        self.builtin_vars = {
            # 基本上照抄手册介绍 - https://docs.sealdice.com/advanced/script.html#%E5%8F%98%E9%87%8F
            # 玩家和账号信息
            '$t玩家': 'BUILTIN_PLAYER',               # 当前人物卡名 不存在则为群或 QQ 昵称
            '$t玩家_RAW': 'BUILTIN_PLAYER_RAW',       # 同上 但不含<>
            '$tQQ 昵称': 'BUILTIN_QQ_NICKNAME',       # QQ 昵称
            '$t账号 ID': 'BUILTIN_ACCOUNT_ID',        # 海豹格式的账号 ID 如 QQ:123456789
            '$t账号 ID_RAW': 'BUILTIN_ACCOUNT_ID_RAW',# 原始格式的账号 ID 如 123456789
            '$tQQ': 'BUILTIN_QQ',                     # 海豹格式的账号 ID 同 $t账号 ID

            # 群组信息
            '$t群名': 'BUILTIN_GROUP_NAME',           # 群名
            '$t群号': 'BUILTIN_GROUP_ID',             # 海豹格式的群 ID 如 QQ-Group:987654321
            '$t群号_RAW': 'BUILTIN_GROUP_ID_RAW',     # 原始格式的群 ID 如 987654321

            # 时间信息
            '$tDate': 'BUILTIN_DATE',                 # 数字格式的日期 如 20230109
            '$tYear': 'BUILTIN_YEAR',                 # 数字格式的年份 如 2023
            '$tMonth': 'BUILTIN_MONTH',               # 数字格式的月份 如 1
            '$tDay': 'BUILTIN_DAY',                   # 数字格式的日期 如 9
            '$tWeekday': 'BUILTIN_WEEKDAY',           # 数字格式的星期（1-7）
            '$tHour': 'BUILTIN_HOUR',                 # 数字格式的小时
            '$tMinute': 'BUILTIN_MINUTE',             # 数字格式的分钟
            '$tSecond': 'BUILTIN_SECOND',             # 数字格式的秒
            '$tTimestamp': 'BUILTIN_TIMESTAMP',       # 10 位时间戳

            # 消息和环境信息
            '$t文本长度': 'BUILTIN_TEXT_LENGTH',       # 消息文本长度 汉字长度为 3
            '$t平台': 'BUILTIN_PLATFORM',             # 触发平台 如 QQ
            '$t游戏模式': 'BUILTIN_GAME_MODE',         # 游戏模式 如 coc7 或 dnd
            '$t消息类型': 'BUILTIN_MESSAGE_TYPE',     # 消息类型 'group' 或 'private'
            '$tMsgID': 'BUILTIN_MESSAGE_ID',           # 消息 ID 仅自定义回复可用
            '$t个人骰子面数': 'BUILTIN_PERSONAL_DICE_SIDES', # 个人骰子面数
            '$t日志开启': 'BUILTIN_LOG_ON',             # 日志是否开启 true 或 false

            # 娱乐和常量
            '娱乐：今日人品': 'BUILTIN_TODAY_LUCK',      # 今日人品
            '常量:APPNAME': 'BUILTIN_CONSTANT_APPNAME', # 软件名 SealDice
            '常量:VERSION': 'BUILTIN_CONSTANT_VERSION'  # 版本号 如 1.5.0-dev
        }
        self.lexer = None
        self.warnings = []
        self.errors = []
    
    # -----------------------------------------------------------------------------
    # 词法分析规则
    # -----------------------------------------------------------------------------
    
    # 简单规则
    # 执行块标记
    t_EXEC_START = r'\{%'   # 匹配 {% 执行块的开始
    t_EXEC_END   = r'%\}'   # 匹配 %} 执行块的结束

    # 算术和赋值运算符
    t_ASSIGN     = r'='     # 匹配单个 = 赋值
    t_PLUS       = r'\+'    # 匹配 + 加法运算
    t_MINUS      = r'-'     # 匹配 - 减法运算
    t_TIMES      = r'\*'    # 匹配 * 乘法运算
    t_DIVIDE     = r'/'     # 匹配 / 除法运算
    t_MODULO     = r'%'     # 匹配 % 取模（求余）运算
    t_POWER      = r'\*\*'   # 匹配 ** 幂运算

    # 比较运算符
    t_EQ         = r'=='    # 匹配 == 等于
    t_NE         = r'!='    # 匹配 != 不等于
    t_GT         = r'>'     # 匹配 > 大于
    t_LT         = r'<'     # 匹配 < 小于
    t_GE         = r'>='    # 匹配 >= 大于等于
    t_LE         = r'<='    # 匹配 <= 小于等于

    # 逻辑运算符
    t_AND        = r'\&\&'
    t_OR         = r'\|\|'
    t_NOT        = r'!'

    # 标点符号
    t_QUESTION   = r'\?'    # 匹配 ? 问号
    t_SEMICOLON  = r';'     # 匹配 ; 结束一个语句
    t_LPAREN     = r'\('    # 匹配 ( 左括号
    t_RPAREN     = r'\)'    # 匹配 ) 右括号
    t_LBRACE     = r'\{'    # 匹配 { 左大括号
    t_RBRACE     = r'\}'    # 匹配 } 右大括号
    t_LBRACKET   = r'\['    # 匹配 [ 左中括号
    t_RBRACKET   = r'\]'    # 匹配 ] 右中括号
    t_COMMA      = r','     # 匹配 , 用于分隔列表或函数参数

    # 忽略规则
    t_ignore = ' \n\t'

    # 错误处理
    def t_error(self, t):
        print(f"非法字符 '{t.value[0]}' 在第 {t.lineno} 行")
        t.lexer.skip(1)

    # -----------------------------------------------------------------------------
    # 规则函数
    # -----------------------------------------------------------------------------
    
    # 保留关键字
    def t_KEYWORD(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        # 仅在字典中匹配到的情况下处理
        if t.value in self.reserved:
            t.type = self.reserved[t.value]
            return t

    def t_STRING_SINGLE(self, t):
        r"'([^'\n]|\\')*'" # 单引号
        t.value = t.value[1:-1]  # 去掉引号
        return t

    def t_STRING_DOUBLE(self, t):
        r'"([^"\n]|\\")*"' # 双引号
        t.value = t.value[1:-1]  # 去掉引号
        return t

    def t_STRING_BACK(self, t):
        r"`([^`\n]|\\`)*`" # 反引号
        t.value = t.value[1:-1]  # 去掉引号
        return t

    # 骰子表达式
    def t_DICE(self, t):
        r'\d+d\d+'
        return t

    # 牌堆表达式
    def t_DRAW(self, t):
        r'\#\{DRAW\-[A-Za-z0-9\u4E00-\u9FFF]+\}'
        return t
    
    # 换行符
    def t_ENDEL(self, t):
        r'\n+|\#\{SPLIT\}'
        t.lexer.lineno += len(t.value)
        return None

    # 标识符（变量）
    def t_IDENTIFIER(self, t):
        # 尝试匹配内置变量字典
        if t.value in self.builtin_vars:
            # 使用字典中对应的 type
            t.type = self.builtin_vars[t.value]
            return t
        else:
            if t.value.startswith('$t'):
                t.type = 'TEMP_VAR' # 临时变量
            elif t.value.startswith('$m'):
                t.type = 'PERSONAL_VAR' # 个人变量
            elif t.value.startswith('$g'):
                t.type = 'GROUP_VAR' # 群变量
            else:
                t.type = 'CONSTANT_VAR' # 无前缀变量
        return t
    
    # -----------------------------------------------------------------------------
    # 辅助方法
    # -----------------------------------------------------------------------------
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

# 构建词法分析器
lexer = lex.lex()


# -----------------------------------------------------------------------------
# 废码留档
# -----------------------------------------------------------------------------

#$# # $t
#$# # 由于优先级问题 更换处理方式
#$# def t_TEMP_VAR(self, t):
#$#     r'\$t[A-Za-z0-9\u4E00-\u9FFF]+'
#$#     return t
        
#$# # $m
#$# def t_PERSONAL_VAR(self, t):
#$#     r'\$m[A-Za-z0-9\u4E00-\u9FFF]+'
#$#     return t
    
#$# # $g
#$# def t_GROUP_VAR(self, t):
#$#     r'\$g[A-Za-z0-9\u4E00-\u9FFF]+'
#$#     return t
    
#$# # 内置变量
#$# def t_BUILTIN_VAR(self, t):
#$#     r'\$t[A-Za-z0-9_\u4E00-\u9FFF]+|娱乐：今日人品 | 常量:APPNAME|常量:VERSION'
#$#     if t.value in self.builtin_vars:
#$#         t.type = self.builtin_vars[t.value]
#$#     return t
    
#$# # 无前缀变量
#$# def t_CONSTANT_VAR(self, t):
#$#     r' [A-Za-z0-9\u4E00-\u9FFF]+ '
#$#     return t
