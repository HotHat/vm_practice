-- local a,b
funcA.name()()

-- (chunk (block (stat (functioncall (prefix (nameOrExp funcA) (prefix_ (nameAndArgs (args ( ))) prefix_)) (nameAndArgs (args ( ))) (nameAndArgs (args ( )))))) <EOF>)
-- (chunk (block (stat (functioncall funcA (nameAndArgs (args ( ))) (nameAndArgs (args ( ))) (nameAndArgs (args ( )))))) <EOF>)
-- (chunk (block (stat (functioncall funcA (nameAndArgs (args ( ))) (nameAndArgs (args ( )))))) <EOF>)
-- (chunk (block (stat (functioncall (prefix (nameOrExp funcA) (prefix_ . name (prefix_ [ (exp (prefixexp (var_ idx))) ] (prefix_ (nameAndArgs (args ( ))) prefix_)))) . name (nameAndArgs (args ( ))) (nameAndArgs (args ( )))))) <EOF>)
