= TODO:
=   read the possible username until ! (or \r\n => return)
=   check for PRIVMSG
=   check for "bfb" => handlecommand.b
=   check for "#geek" => check for % then handlecommand.b
= :boris!~boris@localhost PRIVMSG #geek :PLOP
= :boris!~boris@localhost PRIVMSG bfb :PLOP

@include(skiplinesocket.b)

