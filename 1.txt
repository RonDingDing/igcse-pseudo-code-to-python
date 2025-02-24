DECLARE <identifier> : <data type>
DECLARE <identifier> : ARRAY[<num1>:<num2> (, <num3>: <num4>...)] OF <data type>
CONSTANT <identifier> ← <value>
<identifier> ← <value>
<identifier>[<num1> (, <num2>...)]
<identifier> ← (<unary operator>) <value> (<binary opeartor> <value> ...)
FOR <identifier> ←  1 TO 30
    <statement> 
    (<statement>)...
NEXT <identifier>

INPUT <identifier>
OUTPUT <value(s)>

DIV(<identifier1>, <identifier2>)
MOD(<identifier1>, <identifier2>)

IF <condition>
  THEN
    <statements>
    (<statement>)
  (ELSE
    <statements>)
    (<statement>)...
ENDIF

CASE OF <identifier>
  <value 1> : <statement>
  <value 2> : <statement>
  ...
ENDCASE

REPEAT
    <Statements> 
UNTIL <condition>

WHILE <condition> DO
 <statements> 
ENDWHILE

PROCEDURE <identifier>(<param1>:<datatype>, (<param2>:<datatype>...))
    <statements> 
ENDPROCEDURE

CALL <identifier> (Value1,Value2...)

FUNCTION <identifier>(<param1>:<datatype>, <param2>:<datatype>...) RETURNS <data type>
   <statements> 
ENDFUNCTION

FUNCTION <identifier> RETURNS <data type>
   <statements> 
ENDFUNCTION

OPENFILE <File identifier> FOR <File mode>
READFILE <File Identifier>, <Variable>
CLOSEFILE <File identifier>