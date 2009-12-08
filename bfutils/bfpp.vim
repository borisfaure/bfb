" Vim syntax file
" Language:	Brainfuck++
" Maintainer:	Boris 'billiob' Faure <billiob@gmail.com>
" Last Change:	07-02-2009

syntax match  Comment    "."
syntax match  bfppDebug      "D"
syntax match  bfppPM         "[+-]"
syntax match  bfppMv         "[<>]"
syntax match  bfppCond       "[[\]]"
syntax match  bfppOOp        "[.,%!^#:;]"
syntax region Include   start="^\s*@include(" end=")"

syntax keyword bfppTodo contained TODO FIXME XXX
syntax region bfppComment   start="=" skip="\\$" end="$" keepend contains=bfppTodo

hi def link bfppComment        Comment
hi def link bfppDebug          Error
hi def link bfppPM             Identifier
hi def link bfppMv             Type
hi def link bfppCond           Conditional
hi def link bfppOOp            PreProc
hi def link bfppTodo           Todo

let b:current_syntax = "bfpp"

" vim: ts=8
