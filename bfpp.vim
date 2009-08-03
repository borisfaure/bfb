" Vim syntax file
" Language:	Brainfuck++
" Maintainer:	Boris 'billiob' Faure <billiob@gmail.com>
" Last Change:	07-02-2009

syntax match  Comment        "."
syntax match  Todo           "D"
syntax match  Identifier     "[+-]"
syntax match  Type           "[<>]"
syntax match  Conditional    "[[\]]"
syntax match  PreProc        "[.,%!^#:;]"
syntax region Include   start="^\s*@include(" end=")"
syntax region Comment   start="^=" skip="\\$" end="$" keepend

let b:current_syntax = "bfpp"

" vim: ts=8
