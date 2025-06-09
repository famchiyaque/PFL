% Entry point
s([L | S]) --> l(L), sc, s(S).
s([]) --> [].

% Statement separator
sc --> [';'].

% Statement types
l(Ast) --> dsd(Ast).
l(Ast) --> fd(Ast).
l(Ast) --> wc(Ast).
l(skip) --> [].

% Data Structure Declarations
dsd(int_decl(Id, Expr)) --> [int], ll(Id), ['='], ie(Expr).
dsd(list_decl(Id, FuncCall)) --> [list], ll(Id), ['='], fcl(FuncCall).
dsd(list_decl(Id, list(Elements))) --> [list], ll(Id), ['='], ['['], lc(Elements), [']'].

% Function definition
fd(fun_def(Name, Params, Body)) -->
    [fun], ul(Name), ['('], fdps(Params), [')'], ['{'], fc(Body), ['}'].

fdps([P | Ps]) --> fp(P), fps_tail(Ps).
fdps([]) --> [].

fp(param(Type, Name)) --> dst(Type), ll(Name).

fps_tail([P | Ps]) --> [',' ], fp(P), fps_tail(Ps).
fps_tail([]) --> [].

% Function body - Updated to match new grammar
% fc(block_with_return(Line, Return)) --> l(Line), rs(Return).
% fc(Cond) --> ifelse(Cond).
fc(block_with_return(Lines, Return)) --> fls(Lines), rs(Return).
fc(block_with_conditional(Lines, Cond)) --> fls(Lines), ifelse(Cond).

% Function lines - 0 or more lines with semicolons
fls([Line|Rest]) --> l(Line), sc, fls(Rest).
fls([]) --> [].

% Function call
fcl(func_call(Name, Args)) --> ul(Name), ['('], fclps(Args), [')'].

fclps([Arg | Rest]) --> fclp(Arg), fclp_tail(Rest).
fclps([]) --> [].

fclp(Arg) --> re(Arg).

fclp_tail([Arg | Rest]) --> [','], fclp(Arg), fclp_tail(Rest).
fclp_tail([]) --> [].

% Write call
wc(write(Expr)) --> [write], ['('], dsr(Expr), [')'].

% Return statement
rs(return(Val)) --> [return], re(Val), sc.

re(var(Var)) --> ll(Var).
re(list_op(Var, Op)) --> ll(Var), dsr_attr_l(Op).
re(Expr) --> ie(Expr).

% If/Else - Fixed to match grammar structure
ifelse(if_else(Cond, Then, Else)) -->
    if(Cond, Then), else(Else).

if(Cond, Then) --> ['?'], be(Cond), rs(Then).
else(Else) --> [':'], rs(Else).

% Expressions
e(Expr) --> ie(Expr).
e(Expr) --> be(Expr).

% Integer expression
ie(num(N)) --> num(N).
ie(Var) --> ll(Var).
ie(binop(Op, L, R)) --> ['('], ie(L), nop(Op), ie(R), [')'].
ie(var_access(Id, Attr)) --> ll(Id), dsr_attr_n(Attr).
ie(FuncCall) --> fcl(FuncCall).

% Boolean expressions
be(Expr) --> ['('], jb(Expr), [')'].
be(Expr) --> ['('], cb(Expr), [')'].

jb(bool_call(Id, Attr)) --> ll(Id), dsr_attr_b(Attr).

cb(compare(Op, L, R)) --> ie(L), cop(Op), ie(R).

% Data structure reference
dsr(dsr(Base, Attr)) --> ll(Base), dsr_tail(Attr).
dsr_tail(Attr) --> dsr_attr(Attr).
dsr_tail(none) --> [].

% Data structure attributes (split by return type)
dsr_attr(Attr) --> dsr_attr_n(Attr).
dsr_attr(Attr) --> dsr_attr_b(Attr).
dsr_attr(Attr) --> dsr_attr_l(Attr).

dsr_attr_n(head) --> ['.head'].
dsr_attr_n(tail) --> ['.tail'].
dsr_attr_n(length) --> ['.length'].

dsr_attr_l(pop_head) --> ['.popHead'].
dsr_attr_l(pop_tail) --> ['.popTail'].
dsr_attr_l(push_head(E)) --> ['.pushHead'], ['('], e(E), [')'].
dsr_attr_l(push_tail(E)) --> ['.pushTail'], ['('], e(E), [')'].

dsr_attr_b(empty) --> ['.empty'].

% List contents
lc([Elem | Rest]) --> ie(Elem), lct(Rest).
lc([]) --> [].

lct(Rest) --> [','], lc(Rest).
lct([]) --> [].

% Function/variable names
ul(X) --> [X], { atom(X), atom_chars(X, [C]), char_type(C, upper) }.

ll(X) --> [X], { 
    atom(X),
    atom_chars(X, [C]),
    char_type(C, lower)
}.

% Types
dst(int) --> [int].
dst(list) --> [list].

% Numbers
num(N) --> [N], { number(N) }.

% Operators
nop('+') --> ['+'].
nop('-') --> ['-'].
nop('*') --> ['*'].
nop('/') --> ['/'].

cop('=') --> ['='].
cop('<') --> ['<'].
cop('>') --> ['>'].
cop('<=') --> ['<='].
cop('>=') --> ['>='].

% Parse entry
parse_code(Code, AST) :-
    phrase(s(AST), Code).