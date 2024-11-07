<prog> -> begin <calculo> end
<calculo> -> LAMBDA | <com><calculo>
<com> -> <atrib>|<if>|<leitura>|<impressao>|<bloco>
<atrib> -> ident = <exp> ;
<if> ->  if ( <exp> ) then <com> <else_opc>
<else_opc> -> LAMBDA | else <com> 
<leitura> -> read ( string , ident ) ;
<impressao> -> write ( <lista_out> ) ;
<lista_out> -> <out><restoOut>
<restoOut> -> LAMBDA | ,<out><restoOut>
<out> -> num | ident | string
<bloco> -> { <calculo> }

<exp> -> <disj>
<disj> -> <conj> <restoDisj>
<restoDisj> -> LAMBDA | or <conj> <restoDisj>
<conj> -> <nao> <restoConj>
<restoConj> -> LAMBDA | and <nao> <restoConj>
<nao> -> not <nao> | <rel>
<rel> -> <soma> <restoRel>
<restoRel> -> LAMBDA | oprel <soma>
<soma> -> <mult> <restoSoma>
<restoSoma> -> LAMBDA | + <mult> <restoSoma> | - <mult> <restoSoma>
<mult> -> <uno> <restoMult>
<restoMult> -> LAMBDA | / <uno> <restoMult> | * <uno> <restoMult>
<uno> -> + <uno> | - <uno> | <folha>
<folha> -> num | ident | ( <exp> )