= Is it me or someone else ?
-
<<<<<<<<
>+++++++[>+++++++[<<-->>-]<-]<
>+<[
  = IF NOT 'b'
  >-<
  >+++++++[>+++++++[<<++>>-]<-]<
  >
  =@include(skip_line_socket.b)
  @include(send_welcome.b)
]>[
  = IF 'b'
  +++[<++++>-]<+[<------>-]<
  >+<[
    = IF NOT 'f'
    >-<
    >>++++[<++++>-]<+[<++++++>-]<
    >
    >+++++++[>+++++++[<<++>>-]<-]<
    >
    =@include(skip_line_socket.b)
    @include(send_welcome.b)
  ]>[
    = IF 'f'
    -<
    +++++++[>+++++++[<<-->>-]<-]<
    >+<[
      = IF NOT 'b'
      >++++++[>+++++++[<<++>>-]<-]<
      >
      >>++++[<++++>-]<+[<++++++>-]<
      >
      >+++++++[>+++++++[<<++>>-]<-]<
      >>
      =@include(skip_line_socket.b)
      @include(send_welcome.b)
    ]>[
      = IF 'b'
      -<
      +<-[
        = IF NOT 0x1
        +
        >
        >++++++[>+++++++[<<++>>-]<-]<
        >
        >>++++[<++++>-]<+[<++++++>-]<
        >
        >+++++++[>+++++++[<<++>>-]<-]<
        >>>
        =@include(skip_line_socket.b)
        @include(send_welcome.b)
      ]>[
        = IF 0x1
        <+>>>>>
        =@include(skip_line_socket.b)
        @include(send_hi.b)
      ]<
    ]<
  ]<
]<

>>>>>>>
