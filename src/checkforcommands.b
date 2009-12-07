= Algorithm
=   read the possible username until ' ' (or \r\n => return)
=   read back to a '!'
=   if found, check for commands PRIVMSG/JOIN...
=   else, skiplinesocket

[-]+ = Main loop
>[-]
>[-]+
<<[>> = Main Loop
  [>]
  ![.

    ----------
    >[-]+>[-]<<[>>
      = IF NOT('\n')
      <<----------------------

      [
        = IF NOT ' '
        = +32
        >+++[>++++[<<++>>-]<-]
      ]>
      [>
      = IF (' ')
        <
        -
        <<
        [
          >+++++[<------>-]<---
          >[-]+>[-]<<[>>
            = IF NOT ('!')
          <<[-]>-]>[>
            = IF ('!')
            <-
            @include(switchservercommands.b)
            +>
          <-<<[[-]<]
          <->
          >>+>
          <->]<<

        [-]<]

        <[
          @include(skiplinesocket.b)
        [-]
        ]>
        >+>
        +>

      <->]<<
      >[-]+>[-]
    <-]>[
      = =\n
      -<<
      [[-]<]
      >>
    ]<<
    >

  ]<
  [<]
  <
]
>
>-
<<
