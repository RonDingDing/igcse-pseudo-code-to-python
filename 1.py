from __future__ import annotations
import re
import json


token_specs = [
    (r"DECLARE\b", "DECLARE"),
    (r"ARRAY\b", "ARRAY"),
    (r"OF\b", "OF"),
    (r"CONSTANT\b", "CONSTANT"),
    (r"PROCEDURE\b", "PROCEDURE"),
    (r"FUNCTION\b", "FUNCTION"),
    (r"RETURNS\b", "RETURNS"),
    (r"FOR\b", "FOR"),
    (r"TO\b", "TO"),
    (r"NEXT\b", "NEXT"),
    (r"IF\b", "IF"),
    (r"THEN\b", "THEN"),
    (r"ELSE\b", "ELSE"),
    (r"ENDIF\b", "ENDIF"),
    (r"CASE\b", "CASE"),
    (r"ENDCASE\b", "ENDCASE"),
    (r"REPEAT\b", "REPEAT"),
    (r"UNTIL\b", "UNTIL"),
    (r"WHILE\b", "WHILE"),
    (r"DO\b", "DO"),
    (r"ENDWHILE\b", "ENDWHILE"),
    (r"INPUT\b", "INPUT"),
    (r"OUTPUT\b", "OUTPUT"),
    (r"DIV\b", "DIV"),
    (r"MOD\b", "MOD"),
    (r"OPENFILE\b", "OPENFILE"),
    (r"CLOSEFILE\b", "CLOSEFILE"),
    (r"READFILE\b", "READFILE"),
    (r"CALL\b", "CALL"),
    (r"←", "ASSIGN"),
    (r":", "COLON"),
    (r",", "COMMA"),
    (r"\[", "LBRACKET"),
    (r"\]", "RBRACKET"),
    (r"\(", "LPAREN"),
    (r"\)", "RPAREN"),
    (r"\d+", "NUMBER"),
    (r'"[^"]*"', "STRING"),
    (r"\b(INTEGER|STRING|BOOLEAN)\b", "DATATYPE"),
    (r"==", "EQ"),
    (r"!=", "NEQ"),
    (r">=", "GEQ"),
    (r"<=", "LEQ"),
    (r">", "GT"),
    (r"<", "LT"),
    (r"AND\b", "AND"),
    (r"OR\b", "OR"),
    (r"&", "CONCAT"),
    (r"\s+", None),  # Skip whitespace
    (r"//.*", None),  # Comments
    (r"\[", "LBRACKET"),
    (r"\]", "RBRACKET"),
    (r"\(", "LPAREN"),
    (r"\)", "RPAREN"),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENTIFIER"),  # 放在最后
]


def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        for pattern, token_type in token_specs:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                if token_type:
                    value = match.group()
                    if token_type == "NUMBER":
                        value = int(value)
                    elif token_type == "STRING":
                        value = value[1:-1]  # Remove quotes
                    tokens.append(Token(token_type, value))
                pos = match.end()
                break
        else:
            raise SyntaxError(f"Unexpected character at {pos}: {code[pos]}")
    return tokens


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


token_specs = [
    (r"DECLARE\b", "DECLARE"),
    (r"ARRAY\b", "ARRAY"),
    (r"OF\b", "OF"),
    (r"CONSTANT\b", "CONSTANT"),
    (r"PROCEDURE\b", "PROCEDURE"),
    (r"FUNCTION\b", "FUNCTION"),
    (r"RETURNS\b", "RETURNS"),
    (r"FOR\b", "FOR"),
    (r"TO\b", "TO"),
    (r"NEXT\b", "NEXT"),
    (r"IF\b", "IF"),
    (r"THEN\b", "THEN"),
    (r"ELSE\b", "ELSE"),
    (r"ENDIF\b", "ENDIF"),
    (r"CASE\b", "CASE"),
    (r"ENDCASE\b", "ENDCASE"),
    (r"REPEAT\b", "REPEAT"),
    (r"UNTIL\b", "UNTIL"),
    (r"WHILE\b", "WHILE"),
    (r"DO\b", "DO"),
    (r"ENDWHILE\b", "ENDWHILE"),
    (r"INPUT\b", "INPUT"),
    (r"OUTPUT\b", "OUTPUT"),
    (r"DIV\b", "DIV"),
    (r"MOD\b", "MOD"),
    (r"OPENFILE\b", "OPENFILE"),
    (r"CLOSEFILE\b", "CLOSEFILE"),
    (r"READFILE\b", "READFILE"),
    (r"CALL\b", "CALL"),
    (r"==", "EQ"),
    (r"!=", "NEQ"),
    (r">=", "GEQ"),
    (r"<=", "LEQ"),
    (r">", "GT"),
    (r"<", "LT"),
    (r"←", "ASSIGN"),
    (r"&", "CONCAT"),
    (r":", "COLON"),
    (r",", "COMMA"),
    (r"\[", "LBRACKET"),
    (r"\]", "RBRACKET"),
    (r"\(", "LPAREN"),
    (r"\)", "RPAREN"),
    (r"\d+", "NUMBER"),
    (r'"[^"]*"', "STRING"),
    (r"\b(INTEGER|STRING|BOOLEAN)\b", "DATATYPE"),
    (r"AND\b", "AND"),
    (r"OR\b", "OR"),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENTIFIER"),
    (r"\s+", None),
    (r"//.*", None),
]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, lookahead=0):
        index = self.pos + lookahead
        return self.tokens[index] if index < len(self.tokens) else None

    def consume(self, expected_type=None):
        if self.pos >= len(self.tokens):
            raise SyntaxError("Unexpected end of input")
        token = self.tokens[self.pos]
        if expected_type and token.type != expected_type:
            raise SyntaxError(
                f"Expected {expected_type}, got {token.type} at position {self.pos}"
            )
        self.pos += 1
        return token

    def parse_program(self):
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            statements.append(stmt)
        return {"type": "Program", "statements": statements}

    def parse_statement(self):
        token = self.peek()
        if token is None:
            raise SyntaxError("Unexpected end of input")
        
        if token.type == "DECLARE":
            return self.parse_declaration()
        elif token.type == "CONSTANT":
            return self.parse_constant()
        elif token.type == "FOR":
            return self.parse_for_loop()
        elif token.type == "IF":
            return self.parse_if()
        elif token.type == "CALL":
            return self.parse_procedure_call()
        elif token.type == "OUTPUT":
            return self.parse_output()
        elif token.type == "INPUT":
            return self.parse_input()
        elif token.type == "IDENTIFIER":
            # 检查下一个 Token 是否为 ASSIGN
            next_token = self.peek(1)
            if next_token and next_token.type == "ASSIGN":
                return self.parse_assignment()
            else:
                # 尝试解析为表达式（如函数调用、数组访问）
                return {"type": "ExprStatement", "expr": self.parse_expression()}
        else:
            raise SyntaxError(f"Unsupported statement: {token.type} at position {self.pos}")
    def parse_declaration(self):
        self.consume("DECLARE")
        ident = self.consume("IDENTIFIER").value
        self.consume("COLON")
        if self.peek().type == "ARRAY":
            return self.parse_array_declaration(ident)
        else:
            dtype = self.consume("DATATYPE").value
            return {"type": "VarDecl", "id": ident, "dtype": dtype}

    def parse_array_declaration(self, ident):
        self.consume("ARRAY")
        self.consume("LBRACKET")
        dimensions = []
        while self.peek().type != "RBRACKET":
            start = self.consume("NUMBER").value
            self.consume("COLON")
            end = self.consume("NUMBER").value
            dimensions.append((start, end))
            if self.peek().type == "COMMA":
                self.consume("COMMA")
        self.consume("RBRACKET")
        self.consume("OF")
        dtype = self.consume("DATATYPE").value
        return {"type": "ArrayDecl", "id": ident, "dims": dimensions, "dtype": dtype}

    def parse_constant(self):
        self.consume("CONSTANT")
        ident = self.consume("IDENTIFIER").value
        self.consume("ASSIGN")
        value = self.parse_expression()
        return {"type": "ConstantDecl", "id": ident, "value": value}

    def parse_assignment(self):
        left = self.parse_primary()  # 解析左值（如数组访问）
        self.consume("ASSIGN")
        right = self.parse_expression()
        return {"type": "Assign", "left": left, "right": right}

    def parse_for_loop(self):
        self.consume("FOR")
        var = self.consume("IDENTIFIER").value
        self.consume("ASSIGN")
        start = self.consume("NUMBER").value
        self.consume("TO")
        end = self.consume("NUMBER").value
        body = []
        while self.peek() and self.peek().type != "NEXT":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
        self.consume("NEXT")
        next_var = self.consume("IDENTIFIER").value
        if next_var != var:
            raise SyntaxError(f"Expected NEXT {var}, got {next_var}")
        return {"type": "ForLoop", "var": var, "start": start, "end": end, "body": body}

    def parse_if(self):
        self.consume("IF")
        condition = self.parse_condition()
        self.consume("THEN")
        then_block = []
        while self.peek() and self.peek().type not in ["ELSE", "ENDIF"]:
            stmt = self.parse_statement()
            if stmt:
                then_block.append(stmt)
        else_block = []
        if self.peek() and self.peek().type == "ELSE":
            self.consume("ELSE")
            while self.peek() and self.peek().type != "ENDIF":
                stmt = self.parse_statement()
                if stmt:
                    else_block.append(stmt)
        self.consume("ENDIF")
        return {
            "type": "IfStatement",
            "condition": condition,
            "then": then_block,
            "else": else_block,
        }

    def parse_condition(self):
        left = self.parse_expression()
        op_token = self.consume()
        if op_token.type not in ["EQ", "NEQ", "GT", "LT", "GEQ", "LEQ", "AND", "OR"]:
            raise SyntaxError(f"Invalid operator: {op_token.type}")
        right = self.parse_expression()
        return {"type": "Condition", "left": left, "op": op_token.type, "right": right}

    def parse_procedure_call(self):
        self.consume("CALL")
        name = self.consume("IDENTIFIER").value
        self.consume("LPAREN")
        args = []
        while self.peek() and self.peek().type != "RPAREN":
            args.append(self.parse_expression())
            if self.peek() and self.peek().type == "COMMA":
                self.consume("COMMA")
        self.consume("RPAREN")
        return {"type": "ProcedureCall", "name": name, "args": args}

    def parse_output(self):
        self.consume("OUTPUT")
        value = self.parse_expression()
        return {"type": "Output", "value": value}

    def parse_input(self):
        self.consume("INPUT")
        ident = self.consume("IDENTIFIER").value
        return {"type": "Input", "target": ident}

    def parse_expression(self):
        return self.parse_concat()

    def parse_concat(self):
        expr = self.parse_add()
        while self.peek() and self.peek().type == "CONCAT":
            op = self.consume().type
            right = self.parse_add()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr

    def parse_add(self):
        expr = self.parse_multiply()
        while self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.consume().type
            right = self.parse_multiply()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr

    def parse_multiply(self):
        expr = self.parse_primary()
        while self.peek() and self.peek().type in ("MULTIPLY", "DIV", "MOD"):
            op = self.consume().type
            right = self.parse_primary()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr

    def parse_primary(self):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected end of input")
        
        if token.type == "NUMBER":
            return {"type": "Literal", "value": self.consume().value}
        elif token.type == "STRING":
            return {"type": "Literal", "value": self.consume().value}
        elif token.type == "IDENTIFIER":
            ident = self.consume().value
            indices = []
            # 处理数组访问 arr[i][j]...
            while self.peek() and self.peek().type == "LBRACKET":
                self.consume("LBRACKET")
                index = self.parse_expression()
                self.consume("RBRACKET")
                indices.append(index)
            # 处理函数调用
            if self.peek() and self.peek().type == "LPAREN":
                self.consume("LPAREN")
                args = []
                while self.peek() and self.peek().type != "RPAREN":
                    args.append(self.parse_expression())
                    if self.peek() and self.peek().type == "COMMA":
                        self.consume("COMMA")
                self.consume("RPAREN")
                return {"type": "FunctionCall", "name": ident, "args": args}
            elif indices:
                return {"type": "ArrayAccess", "id": ident, "indices": indices}
            else:
                return {"type": "VarRef", "id": ident}
        elif token.type == "LPAREN":
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")

    def parse_identifier_expression(self):
        ident = self.consume("IDENTIFIER").value
        # 处理数组访问 arr[i]
        if self.peek() and self.peek().type == "LBRACKET":
            indices = []
            while self.peek() and self.peek().type == "LBRACKET":
                self.consume("LBRACKET")
                indices.append(self.parse_expression())
                self.consume("RBRACKET")
            return {"type": "ArrayAccess", "id": ident, "indices": indices}
        # 处理函数调用 DIV(x, 2)
        elif self.peek() and self.peek().type == "LPAREN":
            self.consume("LPAREN")
            args = []
            while self.peek() and self.peek().type != "RPAREN":
                args.append(self.parse_expression())
                if self.peek() and self.peek().type == "COMMA":
                    self.consume("COMMA")
            self.consume("RPAREN")
            return {"type": "FunctionCall", "name": ident, "args": args}
        else:
            return {"type": "VarRef", "id": ident}


# 测试用例2
if __name__ == "__main__":
    code = """
    CONSTANT MAX_SIZE ← 100
    DECLARE score : INTEGER
    INPUT score

    IF score > MAX_SIZE THEN
        OUTPUT "Exceeded limit"
        CALL LogError("Score too high")
    ELSE
        OUTPUT "Valid score"
    ENDIF
    """
    code = """
    DECLARE x : INTEGER
    DECLARE arr : ARRAY[1:10] OF STRING
    x ← 50
    FOR i ← 1 TO 10
        arr[i] ← "Item"  
        OUTPUT arr[i]
    NEXT i
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse_program()
    print(json.dumps(ast, indent=2))
