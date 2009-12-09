= 0| 1 | X | X | X | X | 0 | 0#
= where XXXX is the user who did the action
![.
  >++++++++[<---------->-]<
  >+<[
    = IF NOT 'P'
    ++++++
    [
      = IF NOT 'J'
      >+++++[>+++++[<<+++>>-]<-]<-
      @include(skip_line_socket.b)
    ]>[
      = IF 'J'
      ![.
        >>++++[<++++++>-]<++[<--->-]<-
        >+<[
          = IF NOT 'O'
          >>++++[<++++++>-]<++[<+++>-]<+
          @include(skip_line_socket.b)
        ]>[
          = IF 'O'
          ![.
            >++++++[>+++[<<---->>-]<-]<-
            >+<[
              = IF NOT 'I'
              >++++++[>+++[<<++++>>-]<-]<+
              @include(skip_line_socket.b)
            ]>[
              = IF 'I'
              ![.
                >>++++[<++++++>-]<++[<--->-]<
                >+<[
                  = IF NOT 'N'
                  >>++++[<++++++>-]<++[<+++>-]<
                  @include(skip_line_socket.b)
                ]>[
                  = IF 'N'
                  ![.
                    >++++[>++++[<<-->>-]<-]<
                    >+<[
                      = IF NOT ' '
                      >++++[>++++[<<++>>-]<-]<
                      @include(skip_line_socket.b)
                    ]>[
                      = IF ' '
                      ![.
                        >>+++++[<++++++>-]<-[<-->-]<
                        >+<[
                          = IF NOT ':'
                          >>+++++[<++++++>-]<-[<++>-]<
                          @include(skip_line_socket.b)
                        ]>[
                          = IF ':'
                          @include(srv_cmd_join.b)
                        ]<
                      ]
                    ]<
                  ]
                ]<
              ]
            ]<
          ]
        ]<
      ]
    ]<

  ]>[
    = IF 'P'
    @include(skip_line_socket.b)
    ![.
      >+++++[>++++[<<---->>-]<-]<--
      >+<[
        = IF NOT 'R'
        >+++++[>++++[<<++++>>-]<-]<++
        @include(skip_line_socket.b)
      ]>[
        = IF 'R'
        ![.
          >++++++[>+++[<<---->>-]<-]<-
          >+<[
            = IF NOT 'I'
            >++++++[>+++[<<++++>>-]<-]<+
            @include(skip_line_socket.b)
          ]>[
            = IF 'I'
            ![.
              >>++++[<++++>-]<+[<----->-]<-
              >+<[
                = IF NOT 'V'
                >>++++[<++++>-]<+[<+++++>-]<+
                @include(skip_line_socket.b)
              ]>[
                = IF 'V'
                ![.
                  >>++[<+++++>-]<+[<------->-]<
                  >+<[
                    = IF NOT 'M'
                    >>++[<+++++>-]<+[<+++++++>-]<
                    @include(skip_line_socket.b)
                  ]>[
                    = IF 'M'
                    ![.
                      >+++++[>++++[<<---->>-]<-]<---
                      >+<[
                        = IF NOT 'S'
                        >+++++[>++++[<<++++>>-]<-]<+++
                        @include(skip_line_socket.b)
                      ]>[
                        = IF 'S'
                        ![.
                          >+++++[>+++++++[<<-->>-]<-]<-
                          >+<[
                            = IF NOT 'G'
                            >+++++[>+++++++[<<++>>-]<-]<+
                            @include(skip_line_socket.b)
                          ]>[
                            = IF 'G'
                            ![.
                              >++++[>++++[<<-->>-]<-]<
                              >+<[
                                = IF NOT ' '
                                >++++[>++++[<<++>>-]<-]<
                                @include(skip_line_socket.b)
                              ]>[
                                = IF ' '
                                @include(srv_cmd_privmsg.b)
                              ]<
                            ]
                          ]<
                        ]
                      ]<
                    ]
                  ]<
                ]
              ]<
            ]
          ]<
        ]
      ]<
    ]
  ]<
]
