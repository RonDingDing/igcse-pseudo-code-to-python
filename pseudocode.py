from __future__ import annotations
import re
import json
from typing import Optional, Any, Sequence


class Tokenizer:
    keywords = [
        (r"\bDECLARE\b", "DECLARE"),
        (r"\bARRAY\b", "ARRAY"),
        (r"\bOF\b", "OF"),
        (r"\bCONSTANT\b", "CONSTANT"),
        (r"\bPROCEDURE\b", "PROCEDURE"),
        (r"\bENDPROCEDURE\b", "ENDPROCEDURE"),
        (r"\bFUNCTION\b", "FUNCTION"),
        (r"\bENDFUNCTION\b", "ENDFUNCTION"),
        (r"\bRETURNS\b", "RETURNS"),
        (r"\bRETURN\b", "RETURN"),
        (r"\bFOR\b", "FOR"),
        (r"\bTO\b", "TO"),
        (r"\bSTEP\b", "STEP"),
        (r"\bNEXT\b", "NEXT"),
        (r"\bIF\b", "IF"),
        (r"\bTHEN\b", "THEN"),
        (r"\bELSE\b", "ELSE"),
        (r"\bENDIF\b", "ENDIF"),
        (r"\bCASE\b", "CASE"),
        (r"\bOTHERWISE\b", "OTHERWISE"),
        (r"\bENDCASE\b", "ENDCASE"),
        (r"\bREPEAT\b", "REPEAT"),
        (r"\bUNTIL\b", "UNTIL"),
        (r"\bWHILE\b", "WHILE"),
        (r"\bDO\b", "DO"),
        (r"\bENDWHILE\b", "ENDWHILE"),
        (r"\bINPUT\b", "INPUT"),
        (r"\bOUTPUT\b", "OUTPUT"),
        (r"\bOPENFILE\b", "OPENFILE"),
        (r"\bCLOSEFILE\b", "CLOSEFILE"),
        (r"\bREADFILE\b", "READFILE"),
        (r"\bWRITEFILE\b", "WRITEFILE"),
        (r"\bCALL\b", "CALL"),
        (r"\b(READ|WRITE)\b", "FILEMODE"),
    ]

    binary_operators = [
        (r"\+", "ADD"),
        (r"\-", "SUB"),
        (r"\*", "MUL"),
        (r"\/", "DIW"),
        (r"\<\>", "NEQ"),
        (r"\>\=", "GEQ"),
        (r"\<\=", "LEQ"),
        (r"\<\-", "ASSIGN"),
        (r"\>", "GT"),
        (r"\<", "LT"),
        (r"\=", "EQ"),
        (r"\^", "POW"),
        # (r"\:", "COLON"),
        (r"\←", "ASSIGN"),
        (r"\bAND\b", "AND"),
        (r"\bOR\b", "OR"),
        (r"\bNOT\b", "NOT"),
    ]
    binary_operators_types = [x[1] for x in binary_operators]

    unary_operators_types = ["ADD", "SUB"]

    functions = [
        (r"\bDIV\b", "DIV"),
        (r"\bMOD\b", "MOD"),
        (r"\bLENGTH\b", "LENGTH"),
        (r"\bLCASE\b", "LCASE"),
        (r"\bUCASE\b", "UCASE"),
        (r"\bSUBSTRING\b", "SUBSTRING"),
        (r"\bRANDOM\b", "RANDOM"),
        (r"\bROUND\b", "ROUND"),
    ]

    specs = [
        (r"\:", "COLON"),
        (r",", "COMMA"),
        (r"\[", "LBRACKET"),
        (r"\]", "RBRACKET"),
        (r"\(", "LPAREN"),
        (r"\)", "RPAREN"),
        (r"\{", "LBRACE"),
        (r"\}", "RBRACE"),
        (r'"[^"]*"', "STRING"),
        (r"'[^']*'", "STRING"),
        (r"\b(INTEGER|STRING|CHAR|BOOLEAN|REAL)\b", "DATATYPE"),
        (r"\bTRUE\b", "BOOLEAN"),
        (r"\bFALSE\b", "BOOLEAN"),
        (r"[a-zA-Z0-9_\.]+", "ALLIDENTIFIER"),  # 放在最后
    ]

    empty = [
        (r"[ \t]+", None),  # Skip whitespace
        (r"\n", None),  # new line
        (r"\/\/.*", None),  # Comments
    ]

    token_specs = empty + keywords + binary_operators + functions + specs

    def __init__(self, code: str) -> None:
        self.code = code

    def tokenize(self) -> list[Token]:
        code = self.code
        tokens = []
        pos = 0
        line = 1
        last_col_num = 0
        while pos < len(self.code):
            for pattern, token_type in self.token_specs:
                regex = re.compile(pattern)
                match = regex.match(code, pos)
                if match:
                    if pattern == r"\n":
                        line += 1
                        last_col_num = match.end()
                    if token_type:
                        value = match.group()
                        token = Token(
                            token_type,
                            value,
                            line,
                            match.start() - last_col_num + 1,
                            match.end() - last_col_num + 1,
                        )
                        tokens.append(token)
                    pos = match.end()
                    break
            else:
                raise SyntaxError(
                    f"Unexpected character at line: {line}:{pos - last_col_num + 1} : {code[pos]}"
                )
        return tokens


class Token:
    def __init__(self, types: str, value: Any, line: int, start: int, end: int) -> None:
        self._type = types
        self.value = value
        self.line = line
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        if self.value == "\n":
            return f"Token({self.type}, \\n)"
        return f"Token({self.type}, {self.value}, {self.line}:{self.start}-{self.end})"

    @property
    def type(self) -> str:
        if self._type == "ALLIDENTIFIER":
            if re.match(r"^\d+(\.\d+)?$", self.value):
                return "NUMBER"
            elif re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", self.value):
                return "VARIDENTIFIER"
            return "FILEIDENTIFIER"
        return self._type


############
class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
        self.scope_stack = [{}]  # 作用域栈，初始为全局作用域

    def enter_scope(self) -> None:
        self.scope_stack.append({})

    def exit_scope(self) -> None:
        self.scope_stack.pop()

    def declare_identifier(self, name: str, data_type: str) -> None:
        self.scope_stack[-1][name] = data_type

    def get_identifier_type(self, identifier: dict) -> str:
        """获取标识符的类型"""
        if identifier["type"] == "Identifier":
            for scope in reversed(self.scope_stack):
                if identifier["name"] in scope:
                    return scope[identifier["name"]]
        return "UNKNOWN"

    def peek(self, lookahead: int = 0) -> Optional[Token]:
        if self.pos + lookahead < len(self.tokens):
            return self.tokens[self.pos + lookahead]
        return None

    def consume(self, token_type: Optional[str] = None) -> Optional[Token]:
        if not self.current_token:
            previous_token = self.tokens[self.pos - 1]
            raise SyntaxError(
                f"Expected {token_type}, but there is no tokens {previous_token.line}:{previous_token.start}."
            )

        if token_type and self.current_token and self.current_token.type != token_type:
            raise SyntaxError(
                f"Expected {token_type}, got {self.current_token.type}, {self.current_token}"
            )
        token = self.current_token
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return token

    def parse_program(self) -> dict:
        """Program ::= Statement+"""
        statements = []
        while self.current_token:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return {"type": "Program", "statements": statements}

    def parse_statement(self) -> dict:
        """Statement ::= Declaration | Assignment | ControlStructure | IOStatement | ProcedureCall | ReturnStatement"""
        token = self.current_token
        if not token:
            return {}

        # 变量/常量声明
        result = {}
        token_type = token.type
        if token_type == "DECLARE":
            result = self.parse_declaration()

        elif token_type == "CONSTANT":
            result = self.parse_constant()

        # 控制结构
        elif token_type in ("IF", "WHILE", "REPEAT", "FOR"):
            result = self.parse_control_structure()

        # 过程调用
        elif token_type == "CALL":
            result = self.parse_call()

        # 打开文件语句
        elif token_type == "OPENFILE":
            result = self.parse_openfile()

        # 读取文件语句
        elif token_type == "READFILE":
            result = self.parse_readfile()

        # 写入文件语句
        elif token_type == "WRITEFILE":
            result = self.parse_writefile()

        # 关闭文件语句
        elif token_type == "CLOSEFILE":
            result = self.parse_closefile()

        # 输入语句
        elif token_type == "INPUT":
            result = self.parse_input()

        # 输出语句
        elif token_type == "OUTPUT":
            result = self.parse_output()

        # case 语句
        elif token_type == "CASE":
            return self.parse_case()

        # 过程定义
        elif token_type == "PROCEDURE":
            result = self.parse_procedure()

        # 函数定义
        elif token_type == "FUNCTION":
            result = self.parse_function()

        # 函数返回
        elif token_type == "RETURN":
            result = self.parse_return()

        # 其他语句（如表达式语句）
        else:
            result = {
                "type": "ExpressionStatement",
                "expression": self.parse_expression(),
            }
        return result

    def parse_return(self) -> dict:
        """RETURN <expression>"""
        self.consume("RETURN")
        expr = self.parse_expression()
        return {"type": "ReturnStatement", "expression": expr}

    def parse_case(self) -> dict:
        """Case语句解析
        CASE OF <expression>
            <value> : <statements>
            [OTHERWISE <statements>]
        ENDCASE
        """
        start_pos = self.pos
        self.consume("CASE")
        self.consume("OF")

        # 解析判断表达式
        case_expression = self.parse_expression()

        cases = []
        otherwise = None

        # 解析各个分支
        while self.current_token and self.current_token.type not in (
            "ENDCASE",
            "OTHERWISE",
        ):
            # 解析条件表达式
            condition = self.parse_expression()

            # 检查冒号分隔符
            if not (self.current_token and self.current_token.type == "COLON"):
                raise SyntaxError(f"Expected ':' after case condition")
            self.consume("COLON")

            # 解析分支语句块
            stmt = self.parse_statement()
            cases.append({"condition": condition, "body": stmt})

        # 处理OTHERWISE分支
        if self.current_token and self.current_token.type == "OTHERWISE":
            self.consume("OTHERWISE")
            otherwise = []
            while self.current_token and self.current_token.type != "ENDCASE":
                stmt = self.parse_statement()
                if stmt:
                    otherwise.append(stmt)

        # 验证ENDCASE
        if not self.current_token or self.current_token.type != "ENDCASE":
            raise SyntaxError(f"Unclosed CASE statement")
        self.consume("ENDCASE")
        return {
            "type": "CaseStatement",
            "expression": case_expression,
            "cases": cases,
            "otherwise": otherwise,
        }

    def parse_closefile(self) -> dict:
        """CLOSEFILE <file_identifier>"""
        self.consume("CLOSEFILE")
        file_id_token = self.consume("FILEIDENTIFIER")
        if not file_id_token:
            raise SyntaxError("Expected file identifier after CLOSEFILE")
        file_id = file_id_token.value
        return {"type": "CloseFile", "file": file_id}

    def parse_readfile(self) -> dict:
        """READFILE <file_identifier>, <variable>"""
        self.consume("READFILE")
        file_id_token = self.consume("FILEIDENTIFIER")
        if not file_id_token:
            raise SyntaxError("Expected file identifier after READFILE")
        file_id = file_id_token.value
        self.consume("COMMA")
        target = self.parse_expression()  # 目标变量（Identifier）
        return {"type": "ReadFile", "file": file_id, "target": target}

    def parse_writefile(self) -> dict:
        """WRITEFILE <file_identifier>, <variable>"""
        self.consume("WRITEFILE")
        file_id_token = self.consume("FILEIDENTIFIER")
        if not file_id_token:
            raise SyntaxError("Expected file identifier after WRITEFILE")
        file_id = file_id_token.value
        self.consume("COMMA")
        target = self.parse_expression()  # 目标变量（Identifier）
        return {"type": "WriteFile", "file": file_id, "target": target}

    def parse_openfile(self) -> dict:
        """OPENFILE <file_identifier> FOR <mode>"""
        self.consume("OPENFILE")
        file_id_token = self.consume("FILEIDENTIFIER")
        if not file_id_token:
            raise SyntaxError("Expected file identifier after OPENFILE")
        file_id = file_id_token.value
        self.consume("FOR")
        mode_token = self.consume()
        if not mode_token:
            raise SyntaxError("Expected file identifier after CLOSEFILE")
        mode = mode_token.value
        if mode not in ("READ", "WRITE"):
            raise SyntaxError(f"Invalid file mode: {mode}")
        return {"type": "OpenFile", "file": file_id, "mode": mode}

    def parse_procedure(self) -> dict:
        return self.parse_procedure_or_function("PROCEDURE")

    def parse_function(self) -> dict:
        return self.parse_procedure_or_function("FUNCTION")

    def parse_procedure_or_function(self, typin: str) -> dict:
        """解析过程定义
        PROCEDURE <identifier>
            <statements>
        ENDPROCEDURE

        PROCEDURE <identifier>(<param1>:<datatype>, <param2>:<datatype>...)
            <statements>
        ENDPROCEDURE

        FUNCTION <identifier> RETURN <datatype>
            <statements>
        ENDFUNCTION

        FUNCTION <identifier>(<param1>:<datatype>, <param2>:<datatype>...) RETURN <datatype>
            <statements>
        ENDFUNCTION
        """
        start_keyword = "PROCEDURE" if typin == "PROCEDURE" else "FUNCTION"
        end_keyword = "ENDPROCEDURE" if typin == "PROCEDURE" else "ENDFUNCTION"
        stage_name = (
            "ProcedureDeclaration" if typin == "PROCEDURE" else "FunctionDeclaration"
        )

        # 消耗 PROCEDURE 关键字
        self.consume(start_keyword)

        # 获取过程名称
        name_token = self.consume("VARIDENTIFIER")
        if not name_token:
            raise SyntaxError("Expected identifier in procedure declaration")

        name = name_token.value

        # 解析参数列表
        parameters = []
        if self.current_token and self.current_token.type == "LPAREN":
            self.consume("LPAREN")
            while self.current_token and self.current_token.type != "RPAREN":
                # 解析单个参数 <param>:<datatype>
                param_token = self.consume("VARIDENTIFIER")
                if not param_token:
                    raise SyntaxError("Expected identifier in procedure declaration")
                param_name = param_token.value
                self.consume("COLON")
                param = self.parse_data_type(param_name)
                parameters.append(param)
                # 处理逗号分隔符
                if self.current_token and self.current_token.type == "COMMA":
                    self.consume("COMMA")
            self.consume("RPAREN")

        if typin == "FUNCTION":
            self.consume("RETURNS")
            returned = self.parse_data_type("")

        # 解析过程体
        self.enter_scope()
        for param in parameters:
            self.declare_identifier(param["identifier"], param["data_type"])
        body = []
        while self.current_token and self.current_token.type != end_keyword:
            body.append(self.parse_statement())
        self.exit_scope()

        # 消耗结尾词
        self.consume(end_keyword)

        dic = {
            "type": stage_name,
            "name": name,
            "parameters": parameters,
            "body": body,
        }
        if typin == "FUNCTION":
            dic["return_type"] = returned

        return dic

    def parse_input(self) -> dict:
        self.consume("INPUT")
        elements = []
        # 必须包含至少一个变量
        while True:
            if not self.current_token:
                break
            if self.current_token.type != "VARIDENTIFIER":
                raise SyntaxError("Expected identifier after INPUT")
            identifier = self.parse_primary()
            identifier_type = self.get_identifier_type(identifier)
            elements.append(
                {"identifier": identifier, "identifier_type": identifier_type}
            )
            if self.current_token.type != "COMMA":
                break
            self.consume("COMMA")
        return {"type": "InputStatement", "elements": elements}

    def parse_output(self) -> dict:
        """OUTPUT ::= 'OUTPUT' expression (',' expression)*"""
        self.consume("OUTPUT")
        expressions = []
        # 解析输出表达式列表
        while True:
            expr = self.parse_expression()
            expressions.append(expr)
            if not self.current_token:
                break
            if self.current_token.type == "COMMA":
                self.consume("COMMA")
            else:
                break
        return {"type": "OutputStatement", "expressions": expressions}

    def parse_declaration(self) -> dict:
        """Declaration ::= 'DECLARE' Identifier ':' DataType | ArrayDeclaration"""
        self.consume("DECLARE")
        id_token = self.consume("VARIDENTIFIER")
        if not id_token:
            raise SyntaxError("Expected identifier after DECLARE")
        identifier = id_token.value
        self.consume("COLON")
        if not self.current_token:
            return {}
        declaration = self.parse_data_type(identifier)
        if declaration["is_array"]:
            dimensions = len(declaration["dimensions"])
            self.declare_identifier(
                identifier,
                f"ARRAY{'[' * dimensions + ']' * dimensions} OF {declaration['data_type']}",
            )
        else:
            self.declare_identifier(identifier, declaration["data_type"])
        return declaration

    def parse_data_type(self, identifier: str = "") -> dict:
        if not self.current_token:
            raise SyntaxError("Expected DATATYPE")
        if self.current_token.type == "ARRAY":
            # 数组声明
            return self.parse_array_declaration(identifier, "ArrayDeclaration")
        else:
            return self.parse_simple_variable_declaration(
                identifier, "SimpleVariableDeclaration"
            )

    def parse_simple_variable_declaration(
        self, identifier: str, node_type: str
    ) -> dict:
        """VariableDeclaration ::= Identifier ':' DataType"""
        # 普通变量声明
        data_type_token = self.consume("DATATYPE")
        if not data_type_token:
            raise SyntaxError("Expected identifier after DECLARE")
        data_type = data_type_token.value
        return {
            "type": node_type,
            "is_array": False,
            "identifier": identifier,
            "data_type": data_type,
        }

    def parse_array_declaration(self, identifier: str, node_type: str) -> dict:
        """ArrayDeclaration ::= 'ARRAY' '[' Range (',' Range)* ']' 'OF' DataType"""
        self.consume("ARRAY")
        dimensions = []

        # 解析维度 [1:30, 1:3]
        self.consume("LBRACKET")
        while self.current_token and self.current_token.type != "RBRACKET":
            lower = self.parse_expression()
            self.consume("COLON")
            upper = self.parse_expression()
            dimensions.append({"lower": lower, "upper": upper})

            if self.current_token.type == "COMMA":
                self.consume("COMMA")
        self.consume("RBRACKET")
        self.consume("OF")
        data_type_token = self.consume("DATATYPE")
        if not data_type_token:
            raise SyntaxError("Expected DATATYPE after OF")
        data_type = data_type_token.value

        dic = {
            "type": node_type,
            "dimensions": dimensions,
            "is_array": True,
            "data_type": data_type,
        }
        if identifier:
            dic["identifier"] = identifier
        return dic

    def parse_expression(self) -> dict:
        """表达式解析（处理运算符优先级）"""
        result = self.parse_unary_expression()
        return result

    def parse_unary_expression(self) -> dict:
        """解析一元表达式"""
        token = self.current_token
        if token and token.type in Tokenizer.unary_operators_types:
            self.consume()
            operand = self.parse_primary()
            return {
                "type": "UnaryExpression",
                "operator": token.type,
                "operand": operand,
            }
        return self.parse_binary_expression(0)

    def get_precedence(self, token_type: str) -> int:
        """运算符优先级定义"""
        precedence = {
            "OR": 1,
            "AND": 2,
            "NOT": 3,
            "EQ": 4,
            "NEQ": 4,
            "LT": 4,
            "LEQ": 4,
            "GT": 4,
            "GEQ": 4,
            "ADD": 5,
            "SUB": 5,
            "MUL": 6,
            "DIV": 6,
            "MOD": 6,
            "POW": 7,
        }
        return precedence.get(token_type, 0)

    def parse_binary_expression(self, min_precedence: int) -> dict:
        """递归处理二元表达式"""
        left = self.parse_primary()

        while True:
            current_token = self.current_token
            if (
                not current_token
                or current_token.type not in Tokenizer.binary_operators_types
            ):
                break

            precedence = self.get_precedence(current_token.type)
            if precedence < min_precedence:
                break

            op_token = self.consume()
            if not op_token:
                raise SyntaxError("Expected operator")
            op = op_token.type
            right = self.parse_binary_expression(precedence + 1)
            left = {
                "type": "BinaryExpression",
                "operator": op,
                "left": left,
                "right": right,
            }

        return left

    def parse_primary(self) -> dict:
        """解析基本元素：字面量、标识符、括号、数组索引"""
        token = self.consume()
        if not token:
            return {}

        # 标识符（可能带索引）
        if token.type == "VARIDENTIFIER":
            # 处理数组索引 x[1, 2]
            if self.current_token and self.current_token.type == "LBRACKET":
                indices = []
                self.consume("LBRACKET")
                indices.append(self.parse_expression())
                while self.current_token.type == "COMMA":
                    self.consume("COMMA")
                    indices.append(self.parse_expression())
                self.consume("RBRACKET")

                return {"type": "ArrayAccess", "array": token.value, "indices": indices}

            # 函数调用
            elif self.current_token and self.current_token.type == "LPAREN":
                params = []
                self.consume("LPAREN")
                while self.current_token and self.current_token.type != "RPAREN":
                    params.append(self.parse_expression())
                    if self.current_token.type == "COMMA":
                        self.consume("COMMA")
                self.consume("RPAREN")
                return {
                    "type": "FunctionCall",
                    "function": token.value,
                    "arguments": params,
                }

            # 普通标识符
            return {"type": "Identifier", "name": token.value}

        # 字面量
        elif token.type in ("NUMBER", "STRING", "BOOLEAN"):
            return {"type": "Literal", "value": self.process_literal_value(token)}

        # 括号表达式
        elif token.type == "LPAREN":
            expr = self.parse_expression()
            self.consume("RPAREN")
            return {"type": "Parenthesis", "operand": expr}

        # 函数调用
        elif token.type in [f[1] for f in Tokenizer.functions]:
            self.consume("LPAREN")
            args = []
            while self.current_token and self.current_token.type != "RPAREN":
                args.append(self.parse_expression())
                if self.current_token.type == "COMMA":
                    self.consume("COMMA")
            self.consume("RPAREN")
            return {"type": "FunctionCall", "function": token.type, "arguments": args}

        elif token.type in Tokenizer.unary_operators_types:
            operand = self.parse_primary()
            return {
                "type": "UnaryExpression",
                "operator": token.type,
                "operand": operand,
            }

        else:
            raise SyntaxError(f"Unexpected token: {token}")

    def parse_if_statement(self) -> dict:
        """IF语句解析"""
        self.consume("IF")
        condition = self.parse_expression()
        self.consume("THEN")

        # 解析THEN块
        then_block = []
        while self.current_token and self.current_token.type not in ("ELSE", "ENDIF"):
            then_block.append(self.parse_statement())

        # 解析ELSE块
        else_block = []
        if self.current_token and self.current_token.type == "ELSE":
            self.consume("ELSE")
            while self.current_token and self.current_token.type != "ENDIF":
                else_block.append(self.parse_statement())

        self.consume("ENDIF")
        return {
            "type": "IfStatement",
            "condition": condition,
            "then_block": then_block,
            "else_block": else_block,
        }

    def parse_control_structure(self) -> dict:
        if not self.current_token:
            raise SyntaxError("Unexpected end of input")
        token_type = self.current_token.type
        if token_type == "IF":
            return self.parse_if_statement()
        elif token_type == "REPEAT":
            return self.parse_repeat_loop()
        elif token_type == "WHILE":
            return self.parse_while_loop()
        elif token_type == "FOR":
            return self.parse_for_loop()
        else:
            raise SyntaxError(f"Unsupported control structure: {token_type}")

    def parse_repeat_loop(self) -> dict:
        """REPEAT...UNTIL结构"""
        self.consume("REPEAT")
        body = []
        while self.current_token and self.current_token.type != "UNTIL":
            body.append(self.parse_statement())
        self.consume("UNTIL")
        condition = self.parse_expression()
        return {"type": "RepeatLoop", "body": body, "condition": condition}

    def parse_while_loop(self) -> dict:
        """WHILE...DO结构"""
        self.consume("WHILE")
        condition = self.parse_expression()
        self.consume("DO")
        body = []
        while self.current_token and self.current_token.type != "ENDWHILE":
            body.append(self.parse_statement())
        self.consume("ENDWHILE")
        return {"type": "WhileLoop", "condition": condition, "body": body}

    def parse_for_loop(self) -> dict:
        """FOR...TO...STEP...NEXT结构"""
        self.consume("FOR")
        var_name_token = self.consume("VARIDENTIFIER")
        if not var_name_token:
            raise SyntaxError("Expected identifier after FOR")
        var_name = var_name_token.value
        self.consume("ASSIGN")
        start = self.parse_expression()
        self.consume("TO")
        end = self.parse_expression()
        step = None
        if self.current_token and self.current_token.type == "STEP":
            self.consume("STEP")
            step = self.parse_expression()
        body = []
        while self.current_token and self.current_token.type != "NEXT":
            body.append(self.parse_statement())
        self.consume("NEXT")
        id_token = self.consume("VARIDENTIFIER")  # 检查循环变量是否匹配
        if not id_token:
            raise SyntaxError("Expected identifier after NEXT")
        if id_token.value != var_name:
            raise SyntaxError(f"Loop variable mismatch: {id_token.value} != {var_name}")

        return {
            "type": "ForLoop",
            "variable": var_name,
            "start": start,
            "end": end,
            "step": step,
            "body": body,
        }

    def parse_call(self) -> dict:
        """CALL语句解析"""
        self.consume("CALL")
        id_token = self.consume("VARIDENTIFIER")
        if not id_token:
            raise SyntaxError("Expected identifier")
        name = id_token.value
        args = []
        if self.current_token and self.current_token.type == "LPAREN":
            self.consume("LPAREN")
            while self.current_token and self.current_token.type != "RPAREN":
                args.append(self.parse_expression())
                if self.current_token and self.current_token.type == "COMMA":
                    self.consume("COMMA")
            self.consume("RPAREN")
        return {"type": "ProcedureCall", "name": name, "arguments": args}

    def parse_constant(self) -> dict:
        """解析常量声明语句（符合IGCSE规范，值必须为字面量）"""
        self.consume("CONSTANT")
        id_token = self.consume("VARIDENTIFIER")
        if not id_token:
            raise SyntaxError("Expected identifier")
        identifier = id_token.value
        self.consume("ASSIGN")  # 消费赋值符号 ←

        # 严格限制为字面量（数字/字符串/布尔值）
        if self.current_token and self.current_token.type not in (
            "NUMBER",
            "STRING",
            "BOOLEAN",
        ):
            raise SyntaxError(f"Invalid constant value at line {self.pos}")

        # 解析字面量值
        value_token = self.consume()
        if not value_token:
            raise SyntaxError("Expected value")
        value = self.process_literal_value(value_token)

        return {"type": "ConstantDeclaration", "identifier": identifier, "value": value}

    def process_literal_value(self, token: Token) -> Any:
        """处理字面量值的类型转换"""
        if token.type == "BOOLEAN":
            return token.value.upper() == "TRUE"
        elif token.type == "NUMBER":
            return float(token.value) if "." in token.value else int(token.value)
        elif token.type == "STRING":
            return token.value[1:-1]  # Remove quotes
        return token.value  # STRING类型直接返回

    def parse_lvalue(self) -> dict:
        """解析可赋值目标（标识符或数组访问）"""
        # 基础标识符
        id_token = self.consume("VARIDENTIFIER")
        if not id_token:
            raise SyntaxError("Expected identifier")
        identifier = id_token.value
        indices = []

        # 处理多维数组访问
        while self.current_token and self.current_token.type == "LBRACKET":
            self.consume("LBRACKET")
            # 解析索引表达式列表（支持逗号分隔）
            index_group = []
            while True:
                index_group.append(self.parse_expression())
                if self.current_token.type == "COMMA":
                    self.consume("COMMA")
                else:
                    break
            self.consume("RBRACKET")
            indices.append(index_group)

        # 构建数据结构
        if indices:
            return {"type": "ArrayAccess", "array": identifier, "indices": indices}
        return {"type": "Identifier", "name": identifier}


class Pseudocode:

    div_pre_string = """
def DIV(a: int, b: int) -> int:
    return a // b

"""
    mod_pre_string = """
def MOD(a: int, b: int) -> int:
    return a % b

"""
    len_pre_string = """
def LENGTH(s: Sequence) -> int:
    return len(s)

"""
    lcase_pre_string = """
def LCASE(s: str) -> str:
    return s.lower()

"""
    ucase_pre_string = """
def UCASE(s: str) -> str:
    return s.upper()

"""
    roundpre_string = """
def ROUND(n: float, d: int) -> float:
    return round(n, d)

"""
    substring_pre_string = """
def SUBSTRING(s: str, start: int, length: int) -> str:
    return s[start:start+length]

"""
    random_pre_string = """
import random

def RANDOM():
    return random.random()
"""
    pre_string_dic = {
        "DIV": div_pre_string,
        "MOD": mod_pre_string,
        "LENGTH": len_pre_string,
        "LCASE": lcase_pre_string,
        "UCASE": ucase_pre_string,
        "ROUND": roundpre_string,
        "SUBSTRING": substring_pre_string,
        "RANDOM": random_pre_string,
    }
    default_values = {
        "INTEGER": "int()",
        "STRING": "str()",
        "CHAR": "str()",
        "BOOLEAN": "bool()",
        "REAL": "float()",
    }
    data_type_conv = {
        "INTEGER": "int",
        "STRING": "str",
        "CHAR": "str",
        "BOOLEAN": "bool",
        "REAL": "float",
    }
    operator_dic = {
        "ADD": "+",
        "SUB": "-",
        "MUL": "*",
        "DIW": "/",
        "NEQ": "!=",
        "GEQ": ">=",
        "LEQ": "<=",
        "GT": ">",
        "LT": "<",
        "EQ": "==",
        "POW": "**",
        "ASSIGN": "=",
        "AND": "and",
        "OR": "or",
        "NOT": "not",
    }

    def __init__(self) -> None:
        self.pre_string = ""

    def ast_to_python(self, ast: dict) -> str:
        """将语法树转换为Python代码"""
        ast_type = ast["type"]
        if ast_type == "Program":
            code = "\n".join(self.ast_to_python(stmt) for stmt in ast["statements"])
            return self.pre_string + code

        elif ast_type == "SimpleVariableDeclaration":
            default_value = self.default_values[ast["data_type"]]
            data_type = self.data_type_conv[ast["data_type"]]
            return f"{ast['identifier']}: {data_type} = {default_value}"

        elif ast_type == "ArrayDeclaration":
            default_value = self.default_values[ast["data_type"]]
            single = f"{default_value}"
            for i in ast["dimensions"]:
                upper = f"{self.ast_to_python(i['upper'])}"
                lower = f"{self.ast_to_python(i['lower'])}"
                pattern = r"[a-zA-Z_][a-zA-Z0-9_]*"
                has_string = False
                if re.search(pattern, upper):
                    has_string = True
                if re.search(pattern, lower):
                    has_string = True
                if has_string:
                    num = f"({upper}) - ({lower})"
                else:
                    num = eval(f"{upper} - {lower}")
                if isinstance(num, str):
                    single = f"[{single}] * ({num})"
                else:
                    single = f"[{single}] * {num}"
            return f"{ast['identifier']}: list = {single}"

        elif ast_type == "ConstantDeclaration":
            return f"{ast['identifier']} = {repr(ast['value'])}"

        elif ast_type == "Assignment":
            target_code = self.ast_to_python(ast["target"])
            value_code = self.ast_to_python(ast["value"])
            if ast["target_type"] in self.data_type_conv:
                value_code = f"{self.data_type_conv[ast['target_type']]}({value_code})"
            return f"{target_code} = {value_code}"

        elif ast_type == "Identifier":
            return ast["name"]

        elif ast_type == "Literal":
            return repr(ast["value"])

        elif ast_type == "UnaryExpression":
            return f"{self.operator_dic[ast['operator']]}({self.ast_to_python(ast['operand'])})"

        elif ast_type == "BinaryExpression":
            return f"{self.ast_to_python(ast['left'])} {self.operator_dic[ast['operator']]} {self.ast_to_python(ast['right'])}"

        elif ast_type == "IfStatement":
            then_block = "\n".join(
                self.ast_to_python(stmt) for stmt in ast["then_block"]
            )
            else_block = (
                "\n".join(self.ast_to_python(stmt) for stmt in ast["else_block"])
                if ast["else_block"]
                else ""
            )
            else_start = "else:\n" if ast["else_block"] else ""
            return f"if {self.ast_to_python(ast['condition'])}:\n{indent(then_block)}\n{else_start}{indent(else_block)}"

        elif ast_type == "WhileLoop":
            body = "\n".join(self.ast_to_python(stmt) for stmt in ast["body"])
            return f"while {self.ast_to_python(ast['condition'])}:\n{indent(body)}"

        elif ast_type == "RepeatLoop":
            body = "\n".join(self.ast_to_python(stmt) for stmt in ast["body"])
            return f"while True:\n{indent(body)}\n    if {self.ast_to_python(ast['condition'])}:\n        break"

        elif ast_type == "ForLoop":
            body = "\n".join(self.ast_to_python(stmt) for stmt in ast["body"])
            step = f", {self.ast_to_python(ast['step'])}" if ast["step"] else ""
            return f"for {ast['variable']} in range({self.ast_to_python(ast['start'])}, {self.ast_to_python(ast['end'])}{step}):\n{indent(body)}"

        elif ast_type == "ProcedureCall":
            args = ", ".join(self.ast_to_python(arg) for arg in ast["arguments"])
            return f"{ast['name']}({args})"

        elif ast_type == "FunctionCall":
            if (
                ast["function"] in self.pre_string_dic
                and self.pre_string_dic[ast["function"]] not in self.pre_string
            ):
                self.pre_string += self.pre_string_dic[ast["function"]]
            args = ", ".join(self.ast_to_python(arg) for arg in ast["arguments"])
            return f"{ast['function']}({args})"

        elif ast_type == "ReturnStatement":
            return f"return {self.ast_to_python(ast['expression'])}"

        elif ast_type == "InputStatement":
            return "\n".join(
                f'{self.ast_to_python(elem["identifier"])} = {self.data_type_conv[elem["identifier_type"]]}(input())'
                for elem in ast["elements"]
            )

        elif ast_type == "OutputStatement":
            expressions = ", ".join(
                self.ast_to_python(expr) for expr in ast["expressions"]
            )
            return f"print({expressions})"

        elif ast_type == "ArrayAccess":
            indices = "".join(
                f"[{self.ast_to_python(index)}]" for index in ast["indices"]
            )
            return f"{ast['array']}{indices}"

        elif ast_type == "OpenFile":
            return f"with open(\"{ast['file']}\", '{ast['mode'][0].lower()}') as __fp:\n    pass"

        elif ast_type == "CloseFile":
            return f""

        elif ast_type == "ReadFile":
            return f"with open(\"{ast['file']}\", 'r') as __fp:\n    {ast['target']['name']} = __fp.read()"

        elif ast_type == "WriteFile":
            return f"with open(\"{ast['file']}\", 'w') as __fp:\n    __fp.write({ast['target']['name']})"

        elif ast_type == "CaseStatement":
            cases = f"__case = {self.ast_to_python(ast['expression'])}\n"
            for i, case in enumerate(ast["cases"]):
                if_key = "elif"
                if i == 0:
                    if_key = "if"
                segment = (
                    f"{if_key} __case == {self.ast_to_python(case['condition'])}:\n"
                )
                segment += f"{indent(self.ast_to_python(case['body']))}\n"
                cases += segment
            otherwise = ""
            if ast.get("otherwise"):
                otherwise = f"else:\n"
                for ot in ast["otherwise"]:
                    otherwise += f"{indent(self.ast_to_python(ot))}"
            return f"{cases}{otherwise}"

        elif ast_type == "ProcedureDeclaration":
            params = ", ".join(
                f"{param['identifier']}: {self.data_type_conv[param['data_type']]}"
                for param in ast["parameters"]
            )
            body = "\n".join(self.ast_to_python(stmt) for stmt in ast["body"])
            return f"def {ast['name']}({params}) -> None:\n{indent(body)}"

        elif ast_type == "FunctionDeclaration":
            params = ", ".join(
                f"{param['identifier']}: {self.data_type_conv[param['data_type']]}"
                for param in ast["parameters"]
            )
            body = "\n".join(self.ast_to_python(stmt) for stmt in ast["body"])
            return_type = (
                "list"
                if ast["return_type"]["is_array"]
                else self.data_type_conv[ast["return_type"]["data_type"]]
            )
            return f"def {ast['name']}({params}) -> {return_type}:\n{indent(body)}"

        elif ast_type == "ExpressionStatement":
            return self.ast_to_python(ast["expression"])

        elif ast_type == "Parenthesis":
            return f"({self.ast_to_python(ast['operand'])})"

        else:
            raise ValueError(f"Unknown AST node type: {ast['type']}")


def indent(code: str, level: int = 1) -> str:
    """缩进代码"""
    return "\n".join("    " * level + line for line in code.split("\n"))


if __name__ == "__main__":

    def run_test(code):
        tokens = Tokenizer(code).tokenize()
        ast = Parser(tokens).parse_program()
        print(json.dumps(ast, indent=2))
        python_code = Pseudocode().ast_to_python(ast)
        return python_code

    import sys

    # f = sys.argv[1]
    f = "C:/Users/Ron/Desktop/Teaching/L2/编程题答案/15.txt"
    with open(f, "r", encoding="utf8") as file:
        print(f"--- {f} ---")
        code = run_test(file.read())
        with open(f + ".py", "w", encoding="utf-8") as fp:
            fp.write(code)
        print()
