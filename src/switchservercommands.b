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
      @include(skiplinesocket.b)
    ]>[
      = IF 'J'
      ![.
        >>++++[<++++++>-]<++[<--->-]<-
        >+<[
          = IF NOT 'O'
          >>++++[<++++++>-]<++[<+++>-]<+
          @include(skiplinesocket.b)
        ]>[
          = IF 'O'
          ![.
            >++++++[>+++[<<---->>-]<-]<-
            >+<[
              = IF NOT 'I'
              >++++++[>+++[<<++++>>-]<-]<+
              @include(skiplinesocket.b)
            ]>[
              = IF 'I'
              ![.
                >>++++[<++++++>-]<++[<--->-]<
                >+<[
                  = IF NOT 'N'
                  >>++++[<++++++>-]<++[<+++>-]<
                  @include(skiplinesocket.b)
                ]>[
                  = IF 'N'
                  ![.
                    >++++[>++++[<<-->>-]<-]<
                    >+<[
                      = IF NOT ' '
                      >++++[>++++[<<++>>-]<-]<
                      @include(skiplinesocket.b)
                    ]>[
                      = IF ' '
                      ![.
                        >>+++++[<++++++>-]<-[<-->-]<
                        >+<[
                          = IF NOT ':'
                          >>+++++[<++++++>-]<-[<++>-]<
                          @include(skiplinesocket.b)
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
    @include(skiplinesocket.b)
    ![.
      >+++++[>++++[<<---->>-]<-]<--
      >+<[
        = IF NOT 'R'
        >+++++[>++++[<<++++>>-]<-]<++
        @include(skiplinesocket.b)
      ]>[
        = IF 'R'
        ![.
          >++++++[>+++[<<---->>-]<-]<-
          >+<[
            = IF NOT 'I'
            >++++++[>+++[<<++++>>-]<-]<+
            @include(skiplinesocket.b)
          ]>[
            = IF 'I'
            ![.
              >>++++[<++++>-]<+[<----->-]<-
              >+<[
                = IF NOT 'V'
                >>++++[<++++>-]<+[<+++++>-]<+
                @include(skiplinesocket.b)
              ]>[
                = IF 'V'
                ![.
                  >>++[<+++++>-]<+[<------->-]<
                  >+<[
                    = IF NOT 'M'
                    >>++[<+++++>-]<+[<+++++++>-]<
                    @include(skiplinesocket.b)
                  ]>[
                    = IF 'M'
                    ![.
                      >+++++[>++++[<<---->>-]<-]<---
                      >+<[
                        = IF NOT 'S'
                        >+++++[>++++[<<++++>>-]<-]<+++
                        @include(skiplinesocket.b)
                      ]>[
                        = IF 'S'
                        ![.
                          >+++++[>+++++++[<<-->>-]<-]<-
                          >+<[
                            = IF NOT 'G'
                            >+++++[>+++++++[<<++>>-]<-]<+
                            @include(skiplinesocket.b)
                          ]>[
                            = IF 'G'
                            ![.
                              >++++[>++++[<<-->>-]<-]<
                              >+<[
                                = IF NOT ' '
                                >++++[>++++[<<++>>-]<-]<
                                @include(skiplinesocket.b)
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
