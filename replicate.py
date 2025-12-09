multiline
<drac2>
a = &ARGS&
alev,name,args = int(get("ArtificerLevel",0)),get("name",""),argparse(a)
arg1, arg2, arg3 = (&ARGS& + ["N/A", "N/A", "N/A"])[:3]
outputstring = ""
using(
    infusionlib="52f4547e-72c5-4d34-a930-14367d4c1db5"
)
ch = character()
cclass = "Artificer"
infusion = arg1
valid = False
help = "help" in args or "?" in args

# Allow server admin to suppress the passive ieffects if they want to
infusionset, usepassive = ["passive","action-2","action"], True
if get_svar("infusion_nopassive"):
	infusionset = ["action-2","action"]
	usepassive = False

args.ignore(infusion)
add, delete, armor, loan, listall = "add" in args, "del" in args, "armor" in args, "l" in args, "list" in args or "list" in infusion

valid += add or delete
cc = "Replicate Item"

# If it is a delete action lets help the user out by fuzzy matching to a possible infusion to be deleted
if delete:
	infusion  = infusionlib.matchInfusion(infusion)
	
if armor:
	subclass = load_json(get("subclass","{}")).get(cclass + "Level","")
	if "armorer" in subclass.lower() and alev > 8:
		cc = "Armor Modifications"
		infusionlib.checkArmorer(cc)
	else:
		err("Character does not have the Armor Modifications feature")

features = load_json(get_gvar("0731aeee-9e69-488b-a809-0b3e280fc7f9"))
footer = f'''-footer "{{ctx.prefix+ctx.alias}} |  by vaguely_happy"'''
feature = [x for x in features if not help and infusion.lower() in x.infusion.lower()]
#Check for non unique match and output 
if valid and len(feature) > 1:
	valid = False
	return infusionlib.duplicateMessage(feature)
elif valid and len(feature) == 0:
	return infusionlib.noMatchFound(infusion)
elif valid :
	feature = feature[0]
	

if alev < 2:
	if add and not loan:
		err("Character cannot make Replications. If this is a loan Replication use `-l artificerlevel` to specify a loan and which level artificer it is from")
	elif loan:
		alev = int(args.get("l")[0])
	elif delete:
	# no need to worry if it was really a higher level artificer, we just want to say it was at least the minimum
		alev = feature.level
elif loan: # over-write the artificer level as we are handling an artificer to artificer loan
	alev = int(args.get("l")[0])
		
if help:
	helptext = get_gvar("39ba85fc-9ea5-4ed2-af57-e37242fe5267")
	outputstring += f'''!embed -title "{name} Needs replicate help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''
elif listall:
	liststring = "__Replications for Artificer level " + alev + "__\n"
	if infusion != "N/A":
		liststring += "Showing replications matching `" + infusion + "`\n`"
	for x in features:
		if x.level <= alev:
			if infusion == "N/A":
				liststring += "\n" + x.infusion
			else:
				if infusion.lower() in x.infusion.lower():
					liststring += "\n" + x.infusion

	outputstring += f'''!embed -title "Replicate" -desc "{liststring}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
elif not valid:
	listtext = ""
	infList = infusionlib.getInfusions()
	loanList = infusionlib.getLoans()
	listtext += "**Current active replications**\n\n"
	for x in infList:
		listtext += f'''{x}{" (Loan)" if x in loanList else "" }\n'''
	for x in ["Replicate Item", "Armor Modifications"]:
		if ch.cc_exists(x):
			listtext += f'''\n**{x}**\n{ch.cc_str(x)}\n'''
	outputstring += f'''!embed -title "Replicate" -desc "{listtext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

elif feature.level > alev:
	outputstring += f'''!embed -title "Replicate" -desc "Replication {feature. infusion} is not available at this artificer level" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

elif add:
	if infusionlib.isInfusion(feature.infusion):
		return f'''!embed -title "Replicate" -desc "You already have one {feature.infusion} replicated, you cannot have two of the same type." -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
	else:
		if loan:
			infusionlib.addInfusion(feature.infusion)
			infusionlib.addLoans(feature.infusion)
			infusionlib.createCC(feature)
			for x in infusionset:
				if x in feature:
					# do funky manipulation here to substitute the level
					featuretext = feature[x].replace("ArtificerLevel", str(alev))
					outputstring += f'''!a import {featuretext}\n'''
			outputstring += f'''!embed -title "Replicate" -desc "Replication {feature.infusion} created\n\n{feature.text}\n{feature.passivetext if usepassive and "passivetext" in feature else ""}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

		
		
		elif infusionlib.useInfusionCC(cc):
			if armor:
				infusionlib.addArmorInf(feature.infusion)
			# Note we always put the infusion on the combined list
			infusionlib.addInfusion(feature.infusion)
			infusionlib.createCC(feature)
			for x in infusionset:
				if x in feature:
					outputstring += f'''!a import {feature[x]}\n'''
			outputstring += f'''!embed -title "Replicate" -desc "Replication {feature.infusion} created\n\n{feature.text}\n{feature.passivetext if usepassive and "passivetext" in feature else ""}\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
		else:
			outputstring += f'''!embed -title "Replicate" -desc "No more replications available\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
		return outputstring
elif delete:
	if infusionlib.isArmorInf(feature.infusion):
		cc = "Armor Modifications"
	if not infusionlib.isInfusion(feature.infusion):
		return f'''!embed -title "Replicate" -desc "You do not have {feature.infusion} replicated, you cannot remove it." -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
	else:
		if infusionlib.isLoans(feature.infusion):
			infusionlib.delInfusion(feature.infusion)
			infusionlib.deleteCC(feature)
			for x in infusionset:
				if x in feature:
					actionname = infusionlib.getActionName(feature[x])
					outputstring += f'''!a delete "{actionname}"\n'''
			outputstring += f'''!embed -title "Replicate" -desc "{feature.infusion} removed" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

		elif infusionlib.remInfusionCC(cc):
			infusionlib.delInfusion(feature.infusion)
			infusionlib.deleteCC(feature)
			for x in infusionset:
				if x in feature:
					actionname = infusionlib.getActionName(feature[x])
					outputstring += f'''!a delete "{actionname}"\n'''
			outputstring += f'''!embed -title "Replicate" -desc "{feature.infusion} removed\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
		else:
			outputstring += f'''!embed -title "Replicate" -desc "Could not find the counter **{cc}**\n" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''

	
	
return outputstring
</drac2>
