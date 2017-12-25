"""
Manifest is a *.pp puppet file or a directory thats ingested by puppet.
puppet.conf is the default primary manifest file.

To check which puppet manifest your server uses, use the cmd:
`puppet config print manifest --section master --environment <ENVIRONMENT>.`

Puppet uses a key-value store called heira where it stores all the configuration keys and values.

Puppet has a master and agent.
`puppet master --configprint <SETTING>`
`puppet agent --configprint <SETTING>`
`puppet apply --configprint <SETTING>`

"""