
@include(fill_address.b)
%+[-
  @include(clear_memory.b)
  @include(join_irc.b)
  @include(ping_or_else.b)
]

