import ply.lex as lex

class BaoLexer:
    # token 列表
    tokens = [
        'IF',
        'ELSE',
        'ASSIGN',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULO',
        'POWER',
        'EQ',
        'NE',
        'GT',
        'LT',
        'GE',
        'LE',
        'AND',
        'OR',
        'NOT',
        'QUESTION',
        'COLON',
        'SEMICOLON',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'LBRACKET',
        'RBRACKET',
        'COMMA',
        'NUMBER',
        'STRING_SINGLE',
        'STRING_DOUBLE',
        'STRING_BACK',
        'IDENTIFIER',
        'TEMP_VAR',
        'PERSONAL_VAR',
        'GROUP_VAR',
        'BUILTIN_VAR',
        'CONSTANT_VAR',
        'CUSTOM_TEXT',
        'DICE',
        'DRAW',
        'ENDEL'
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
