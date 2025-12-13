multiline
<drac2>
a = &ARGS&
alev,name,args = int(get("ArtificerLevel",0)),get("name",""),argparse(a)
arg1, arg2 = (&ARGS& + ["N/A", "N/A"])[:2]
if "N/A" in arg1:
	err("You must specify a replication which you wish to transmute. `!replicate transmute <name1> <name2>`")
if "N/A" in arg2:
	err("You must specify a replication which you wish to create. `!replicate transmute <name1> <name2>`")

common, uncommon, rare = "common" in args, "uncommon" in args, "rare" in args
noval = common or uncommon or rare # we cannot validate or do much at all with generic replications right now

outputstring = ""
using(
    infusionlib="52f4547e-72c5-4d34-a930-14367d4c1db5"
)
ch = character()
cclass = "Artificer"
infusion = arg1
replication = arg2
help = "help" in args or "?" in args

# Allow server admin to suppress the passive ieffects if they want to
infusionset, usepassive = ["passive","action-2","action"], True
if get_svar("infusion_nopassive"):
	infusionset = ["action-2","action"]
	usepassive = False

cc = "Transmute Magic Item"

if not ch.cc_exists(cc):
	err("You do not have the Magic Item Tinker feature in order to be able to Transmute Magic Item")
	
if ch.get_cc(cc) < 1:
	err("You have no more uses of Transmute Magic Item, you cannot transmute another item until you long rest")

# lets help the user out by fuzzy matching to a possible infusion to be deleted
infusion  = infusionlib.matchInfusion(infusion)
features = load_json(get_gvar("0731aeee-9e69-488b-a809-0b3e280fc7f9"))
if noval:
	replication = "common : " + replication if common else "uncommon : " + replication if uncommon else "rare : " + replication
else:	

	footer = f'''-footer "{{ctx.prefix+ctx.alias}} |  by vaguely_happy"'''
	feature = [x for x in features if not help and replication.lower() in x.infusion.lower()]
	#Check for non unique match and output 
	if len(feature) > 1:
		valid = False
		return infusionlib.duplicateMessage(feature)
	elif len(feature) == 0:
		return infusionlib.noMatchFound(replication)
	else:
		feature = feature[0]
		replication = feature.infusion
		
oldgeneric = infusion.startswith("common :") or infusion.startswith("uncommon :") or infusion.startswith("rare :")
if not oldgeneric:
	oldfeature = 	[x for x in features if not help and infusion.lower() in x.infusion.lower()]
	oldfeature = oldfeature[0]  # No need for the other checks as its an existing replication that would have been checked on creation


if help:
	helptext = get_gvar("39ba85fc-9ea5-4ed2-af57-e37242fe5267")
	outputstring += f'''!embed -title "{name} Needs replicate help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''
else:
	if infusionlib.isInfusion(replication):
		return f'''!embed -title "Replicate" -desc "You already have one {replication} replicated, you cannot have two of the same type." -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
	if infusionlib.isLoans(infusion):
		return f'''!embed -title "Replicate" -desc "Your infusion {infusion} is on loan and is not one of your own creations, you cannot transmute it." -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
	elif not infusionlib.isInfusion(infusion):
		return f'''!embed -title "Replicate" -desc "You do not have {infusion} replicated, you cannot transform it." -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
	
	else:
		armor = infusionlib.isArmorInf(infusion)
		if armor:
			infusionlib.addArmorInf(replication)
		# Note we always put the infusion on the combined list
		infusionlib.addInfusion(replication)
		if not noval:
			infusionlib.createCC(feature)
			for x in infusionset:
				if x in feature:
					outputstring += f'''!a import {feature[x]}\n'''
		# Now do the delete part
		infusionlib.delInfusion(infusion)
		ch.mod_cc(cc, -1)
		if not oldgeneric:
			infusionlib.deleteCC(oldfeature)

			for x in infusionset:
				if x in oldfeature:
					actionname = infusionlib.getActionName(oldfeature[x])
					outputstring += f'''!a delete "{actionname}"\n'''
		if noval:
			outputstring += f'''!embed -title "Replicate" -desc "Transmuted {infusion} into  {replication}\n\nNo built in automation support for generic items.\n\n**{cc}**\n{ch.cc_str(cc)} -1" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
		else:
			outputstring += f'''!embed -title "Replicate" -desc "Transmuted {infusion} into  {feature.infusion}\n\n{feature.text}\n{feature.passivetext if usepassive and "passivetext" in feature else ""}\n\n**{cc}**\n{ch.cc_str(cc)} -1" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

return outputstring
</drac2>
