import ply.lex as lex

class BaoLexer:
    # token 列表
    tokens = [
        # 关键字
        'IF',           # 'if' 语句，用于条件判断
        'ELSE',         # 'else' 语句，通常与 'if' 配合使用

        # 运算符
        'ASSIGN',       # 赋值运算符，例如 `=`
        'PLUS',         # 加法运算符，例如 `+`
        'MINUS',        # 减法运算符，例如 `-`
        'TIMES',        # 乘法运算符，例如 `*`
        'DIVIDE',       # 除法运算符，例如 `/`
        'MODULO',       # 取模（求余数）运算符，例如 `%`
        'POWER',        # 幂运算运算符，例如 `**`

        # 比较运算符
        'EQ',           # 等于，例如 `==`
        'NE',           # 不等于，例如 `!=`
        'GT',           # 大于，例如 `>`
        'LT',           # 小于，例如 `<`
        'GE',           # 大于等于，例如 `>=`
        'LE',           # 小于等于，例如 `<=`

        # 逻辑运算符 (Logical Operators) - 用于布尔逻辑运算
        'AND',          # 逻辑与，例如 `&&` 或 `and`
        'OR',           # 逻辑或，例如 `||` 或 `or`
        'NOT',          # 逻辑非，例如 `!` 或 `not`

        # 标点符号 (Punctuation) - 用于分隔和组织代码结构
        'QUESTION',     # 问号
        # 'COLON',        # 冒号
        'SEMICOLON',    # 分号，结束一个语句
        'LPAREN',       # 左括号 `(`
        'RPAREN',       # 右括号 `)`
        'LBRACE',       # 左大括号 `{`
        'RBRACE',       # 右大括号 `}`
        'LBRACKET',     # 左中括号 `[`
        'RBRACKET',     # 右中括号 `]`
        'COMMA',        # 逗号 `,`

        # 字面量和变量类型
        'NUMBER',       # 数字字面量，例如 `123` 或 `3.14`
        'STRING_SINGLE',# 单引号字符串，例如 `'hello'`
        'STRING_DOUBLE',# 双引号字符串，例如 `"world"`
        'STRING_BACK',  # 反引号字符串，例如 `` `template` ``
        
        # 标识符
        'IDENTIFIER',   # 所有类型的变量
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
    ]

    def __init__(self):
        # 保留字字典，用于处理关键字和标识符的冲突
        self.reserved = {
            'if': 'IF',
            'else': 'ELSE'
        }

        self.builtin_vars = {
            # 基本上照抄手册介绍
            # 玩家和账号信息
            '$t玩家': 'BUILTIN_PLAYER',               # 当前人物卡名，不存在则为群或 QQ 昵称
            '$t玩家_RAW': 'BUILTIN_PLAYER_RAW',       # 同上，但不含<>
            '$tQQ 昵称': 'BUILTIN_QQ_NICKNAME',       # QQ 昵称
            '$t账号 ID': 'BUILTIN_ACCOUNT_ID',        # 海豹格式的账号 ID，如 QQ:123456789
            '$t账号 ID_RAW': 'BUILTIN_ACCOUNT_ID_RAW',# 原始格式的账号 ID，如 123456789
            '$tQQ': 'BUILTIN_QQ',                     # 海豹格式的账号 ID，同 $t账号 ID

            # 群组信息
            '$t群名': 'BUILTIN_GROUP_NAME',           # 群名
            '$t群号': 'BUILTIN_GROUP_ID',             # 海豹格式的群 ID，如 QQ-Group:987654321
            '$t群号_RAW': 'BUILTIN_GROUP_ID_RAW',     # 原始格式的群 ID，如 987654321

            # 时间信息
            '$tDate': 'BUILTIN_DATE',                 # 数字格式的日期，如 20230109
            '$tYear': 'BUILTIN_YEAR',                 # 数字格式的年份，如 2023
            '$tMonth': 'BUILTIN_MONTH',               # 数字格式的月份，如 1
            '$tDay': 'BUILTIN_DAY',                   # 数字格式的日期，如 9
            '$tWeekday': 'BUILTIN_WEEKDAY',           # 数字格式的星期（1-7）
            '$tHour': 'BUILTIN_HOUR',                 # 数字格式的小时
            '$tMinute': 'BUILTIN_MINUTE',             # 数字格式的分钟
            '$tSecond': 'BUILTIN_SECOND',             # 数字格式的秒
            '$tTimestamp': 'BUILTIN_TIMESTAMP',       # 10 位时间戳

            # 消息和环境信息
            '$t文本长度': 'BUILTIN_TEXT_LENGTH',       # 消息文本长度，汉字长度为 3
            '$t平台': 'BUILTIN_PLATFORM',             # 触发平台，如 QQ
            '$t游戏模式': 'BUILTIN_GAME_MODE',         # 游戏模式，如 coc7 或 dnd
            '$t消息类型': 'BUILTIN_MESSAGE_TYPE',     # 消息类型，'group' 或 'private'
            '$tMsgID': 'BUILTIN_MESSAGE_ID',           # 消息 ID，仅自定义回复可用
            '$t个人骰子面数': 'BUILTIN_PERSONAL_DICE_SIDES', # 个人骰子面数
            '$t日志开启': 'BUILTIN_LOG_ON',             # 日志是否开启，true 或 false

            # 娱乐和常量
            '娱乐：今日人品': 'BUILTIN_TODAY_LUCK',      # 今日人品
            '常量:APPNAME': 'BUILTIN_CONSTANT_APPNAME', # 软件名，SealDice
            '常量:VERSION': 'BUILTIN_CONSTANT_VERSION', # 版本号，如 1.5.0-dev
        }
        self.lexer = None
        self.warnings = []
        self.errors = []
    
    # -----------------------------------------------------------------------------
    # 词法分析规则
    # -----------------------------------------------------------------------------
    
    # 忽略规则
    t_ignore = ' \t'

    # 错误处理
    def t_error(self, t):
        print(f"非法字符 '{t.value[0]}' at line {t.lineno}")
        t.lexer.skip(1)

    # -----------------------------------------------------------------------------
    # 规则函数
    # -----------------------------------------------------------------------------
    

    # 标识符（变量）
    def t_IDENTIFIER(self, t):
        if t.value in self.builtin_vars: # 尝试匹配内置变量字典
            t.type = self.builtin_vars[t.value] # 使用字典中对应的 type
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

    # 骰子表达式
    def t_DICE(self, t):
        r'\d+d\d+'
        return t

    # 牌堆表达式
    def t_DRAW(self, t):
        r'\#{DRAW\-[A-Za-z0-9\u4E00-\u9FFF]+}'
        return t
    
    # 换行符
    def t_ENDEL(self, t):
        r'\n+|\#{SPLIT}'
        t.lexer.lineno += len(t.value)
        return None
    
    # -----------------------------------------------------------------------------
    # 辅助方法
    # -----------------------------------------------------------------------------
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer

    # -----------------------------------------------------------------------------
    # 废码留档
    # -----------------------------------------------------------------------------

    '''
    # $t
    # 由于优先级问题，更换处理方式
    def t_TEMP_VAR(self, t):
        r'\$t[A-Za-z0-9\u4E00-\u9FFF]+'
        return t
        
    # $m
    def t_PERSONAL_VAR(self, t):
        r'\$m[A-Za-z0-9\u4E00-\u9FFF]+'
        return t
    
    # $g
    def t_GROUP_VAR(self, t):
        r'\$g[A-Za-z0-9\u4E00-\u9FFF]+'
        return t
    
    # 内置变量
    def t_BUILTIN_VAR(self, t):
        r'\$t[A-Za-z0-9_\u4E00-\u9FFF]+|娱乐：今日人品 | 常量:APPNAME|常量:VERSION'
        if t.value in self.builtin_vars:
            t.type = self.builtin_vars[t.value]
        return t
    
    # 无前缀变量
    def t_CONSTANT_VAR(self, t):
        r' [A-Za-z0-9\u4E00-\u9FFF]+ '
        return t
    '''