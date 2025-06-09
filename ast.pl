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

% Declarations
dsd(int_decl(Id, Expr)) --> [int], ll(Id), ['='], e(Expr).
# dsd(list_decl(Id, FuncCall)) --> [list], ll(Id), ['='], fcl(FuncCall).
dsd(list_decl(Id, list(Elements))) --> [list], ll(Id), ['='], ['['], lc(Elements), [']'].

% Function definition
fd(fun_def(Name, Params, Body)) -->
    [fun], ul(Name), ['('], fdps(Params), [')'], ['{'], fc(Body), ['}'].

fdps([P | Ps]) --> fp(P), fps_tail(Ps).
fdps([]) --> [].

fp(param(Type, Name)) --> dst(Type), ll(Name).

fps_tail([P | Ps]) --> [',' ], fp(P), fps_tail(Ps).
fps_tail([]) --> [].

% Function body (could be a block, conditional, or return)
fc(Block) --> l(Block).
fc(Cond) --> ifelse(Cond).
fc(Return) --> rs(Return).

% Function call (list version)
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

re(Var) --> ll(Var).
re(FuncCall) --> fcl(FuncCall).
re(Expr) --> ien(Expr).

% If/Else
ifelse(if_else(Cond, Then, Else)) -->
    ['?'], be(Cond), rs(Then), [':'], rs(Else).

% Expressions
e(Expr) --> ie(Expr).
e(Expr) --> be(Expr).
e(num(N)) --> num(N).
e(FuncCall) --> fcl(FuncCall).

% Integer expression
ie(binop(Op, L, R)) --> ['('], ien(L), nop(Op), ien(R), [')'].

ien(num(N)) --> num(N).
ien(var_access(Id, Attr)) --> ll(Id), dsr_attr(Attr).

% Boolean expression
be(Expr) --> ['('], jb(Expr), [')'].
be(Expr) --> ['('], cb(Expr), [')'].

jb(bool_call(Id, Attr)) --> ll(Id), dsr_attr_b(Attr).

cb(compare(Op, L, R)) --> ien(L), cop(Op), ien(R).

% Data structure reference
dsr(dsr(Base, Attr)) --> ll(Base), dsr_tail(Attr).
dsr_tail(Attr) --> dsr_attr(Attr).
dsr_tail(none) --> [].

dsr_attr(head) --> ['.head'].
dsr_attr(tail) --> ['.tail'].
dsr_attr(length) --> ['.length'].
dsr_attr(pop_head) --> ['.popHead'].
dsr_attr(pop_tail) --> ['.popTail'].
dsr_attr(push_head(E)) --> ['.pushHead'], ['('], e(E), [')'].
dsr_attr(push_tail(E)) --> ['.pushTail'], ['('], e(E), [')'].
dsr_attr(empty) --> ['.empty'].

dsr_attr_b(empty) --> ['.empty'].

% List of constants
lc([N | Rest]) --> num(N), lct(Rest).
lc([]) --> [].

lct([N | Rest]) --> [','], lc([N | Rest]).
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
