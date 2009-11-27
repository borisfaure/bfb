= TODO:
=   read the possible username until ! (or \r\n => return)
=   check for PRIVMSG
=   check for "bfb" => handlecommand.b
=   check for "#geek" => check for % then handlecommand.b
= :boris!~boris@localhost PRIVMSG #geek :PLOP
= :boris!~boris@localhost PRIVMSG bfb :PLOP
= Current pointer is 6
= | 0 | 0 | 0 | 1 | 0 | 1 | 0# |
[-]>[-]+[>
  [>]
  >![.
    = Move CUR to CUR-1
    [-<+>]




    <
    ----------
    >[-]+>[-]<<[>>
      = ! \n
      =<<++++++++++>>
      <<-----------------------
=      >>
      = IF NOT '!'
      [>>
        = TODO: +++++
      <<>-]>
      [>
      = IF ('!')
        +[>
        ![.
          ----------
            >[-]+>[-]<<[>>
              = ! \n
              = TODO: read till ' '
            <<[-]>-]>[>
              = \n => break the loop
               <<<->>>
            <<>->]<<

        ]
        <]
      <<>->]<<
      >[-]+>[-]
    <<>-]>[
      = =\n
      -<<
      [[-]<]
      >>
    ]<<
    >



  ]<
  [<]
  >
]<
