# replication / infusions
An alias to manage artificer replicate magic item on your characters. This will retain the legacy infusion alias for older 2014 characters and to aid migration of characters to the new rules. It will keep track of replications made and will add counters and actions for the replicated items.

Also supports lending of replicated to non-artificers who will gain the same counters and actions.

See `!replicate help` for details of how to use

The main parts of the code are in replicate (the alias) sub-aliases and infusionlib (held as a gvar lib)

The data is all held in infusiondefs which is deployed as a gvar. This is written and maintained in infusions 2024.xlsx and for legacy the infusions.xlsx which is where the individual actions are stored in a more accessible form.

TODO. Under active development is the 20th level Cheat Death feature. Other than that this should be a feature complete set of aliases for things directly relating to replications
