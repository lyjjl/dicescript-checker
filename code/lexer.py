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
        # 'IDENTIFIER',   # 
        'TEMP_VAR',     # 临时变量 ($t)
        'PERSONAL_VAR', # 个人变量 ($m)
        'GROUP_VAR',    # 群变量 ($g)
        'BUILTIN_VAR',  # 内置变量
        'CONSTANT_VAR', # 无前缀变量

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
    
    # $t
    def t_TEMP_VAR(self, t):
        r'\$t[A-Za-z0-9\u4E00-\u9FFF]+'
        return t

    # 骰子表达式
    def t_DICE(self, t):
        r'\d+d\d+'
        return t    
    
    # -----------------------------------------------------------------------------
    # 辅助方法
    # -----------------------------------------------------------------------------
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        return self.lexer
