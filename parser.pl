% Start
s --> l, sc, s.
s --> [].

% Line Possibilities
l --> dsd.
l --> fd.
l --> wc.
l --> [].

sc --> [';'].

% Data Structure Declarations
dsd --> id.
dsd --> ld.

% Function Declarations
fd --> [fun], ul, ['('], fdps, [')'], ['{'], fc, ['}'].

% Write Call
wc --> [write], ['('], dsr, [')'].

% Integer/List Declarations
id --> [int], ll, ['='], ie. 
ld --> [list], ll, ['='], fcl.
ld --> [list], ll, ['='], ['['], lc, [']'].

% Allowed data structure/function names
ul --> [X], { atom(X), atom_chars(X, [C]), char_type(C, upper) }.
ll --> [X], { atom(X), atom_chars(X, [C]), char_type(C, lower) }.

% Function Parameters
fdps --> fp, fps_tail.
fdps --> [].
fp --> dst, ll.
fps_tail --> [',' ], fp, fps_tail.
fps_tail --> [].

% Function Contents
fc --> fls, fr.

fls --> l, sc, fls.
fls --> [].

fr --> rs.
fr --> ifelse.

% Data Structure Types/References with optional tail
dst --> [int].
dst --> [list].

dsr --> ll, dsr_tail.
dsr_tail --> dsr_attr.
dsr_tail --> [].

dsr_attr --> dsr_attr_n.
dsr_attr --> dsr_attr_b.
dsr_attr --> dsr_attr_l.

dsr_attr_n --> ['.head'].
dsr_attr_n --> ['.tail'].
dsr_attr_n --> ['.length'].
dsr_attr_l --> ['.popHead'].
dsr_attr_l --> ['.popTail'].
dsr_attr_l --> ['.pushHead'], ['('], e, [')'].
dsr_attr_l --> ['.pushTail'], ['('], e, [')'].
dsr_attr_b --> ['.empty'].

% Expressions
e --> ie.
e --> be.

ie --> num.
ie --> ['('], ie, nop, ie, [')'].
ie --> ll.
ie --> ll, dsr_attr_n.
ie --> fcl.

% List Contents
lc --> ie, lct. % (can be various integer expressions, can be empty)
lc --> [].

lct --> [','], lc.
lct --> [].

% If/Else Structure
ifelse --> if, else.
if --> ['?'], be, rs.
else --> [':'], rs.

% Bool Expressions
be --> ['('], jb, [')'].
be --> ['('], cb, [')'].

jb --> ll, dsr_attr_b.
cb --> ie, cop, ie.

% Return Statements
% (can return data structure reference, whether just the name, or)
% (or with attribute that returns the new list, or integer expr)
rs --> [return], re, sc.

re --> ll.
re --> ll, dsr_attr_l.
re --> ie.

% Function Calls
fcl --> ul, ['('], fclps, [')'].

% Function Call Params
fclps --> fclp, fclp_tail. % (can have no parameters)
fclps --> [].

fclp --> re. % (param can be anything returnable)

fclp_tail --> [','], fclp, fclp_tail.
fclp_tail --> [].

% Operators
nop --> ['+'].
nop --> ['-'].
nop --> ['*'].
nop --> ['/'].

cop --> ['='].
cop --> ['<'].
cop --> ['>'].
cop --> ['<='].
cop --> ['>='].

% Numbers
num --> [N], { number(N) }.


parse_code(Code) :-
    phrase(s, Code).