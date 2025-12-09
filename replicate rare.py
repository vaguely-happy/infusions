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
modifier = arg2

help = "help" in args or "?" in args

nullinfusion = "N/A" in infusion
armor, loan, delete = "armor" in args, "l" in args, "del" in args

cc = "Replicate Item"

# If it is a delete action lets help the user out by fuzzy matching to a possible infusion to be deleted
if delete:
	infusion  = infusionlib.matchInfusion(infusion)
	
infusion_choice = "rare : " + infusion

if armor:
	subclass = load_json(get("subclass","{}")).get(cclass + "Level","")
	if "armorer" in subclass.lower() and alev > 8:
		cc = "Armor Modifications"
		infusionlib.checkArmorer(cc)
	else:
		err("Character does not have the Armor Modifications feature")

if alev < 14:
	if not loan:
		err("Character cannot make rare Replications. If this is a loan Replication use `-l artificerlevel` to specify a loan and which level artificer it is from")
	else:
		alev = int(args.get("l")[0])

elif loan: # over-write the artificer level as we are handling an artificer to artificer loan
	alev = int(args.get("l")[0])
		
if help or nullinfusion:
	helptext = get_gvar("39ba85fc-9ea5-4ed2-af57-e37242fe5267")
	outputstring += f'''!embed -title "{name} Needs replicate help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''

elif 14 > alev:
	outputstring += f'''!embed -title "Replicate" -desc "Replication {feature. infusion} is not available at this artificer level" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''
elif delete:
	if infusionlib.isArmorInf(infusion_choice):
		cc = "Armor Modifications"
	if not infusionlib.isInfusion(infusion_choice) and not infusionlib.isInfusion(infusion):
		return f'''!embed -title "Replicate" -desc "You do not have {infusion_choice} replicated, you cannot remove it." -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''
	else:
		if infusionlib.isLoans(infusion_choice):
			infusionlib.delInfusion(infusion_choice)
			outputstring += f'''!embed -title "Replicate" -desc "{infusion_choice} removed" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''

		elif infusionlib.remInfusionCC(cc):
			infusionlib.delInfusion(infusion_choice)
			outputstring += f'''!embed -title "Replicate" -desc "{infusion_choice} removed\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''
		else:
			outputstring += f'''!embed -title "Replicate" -desc "Could not find the counter **{cc}**\n" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''

else:
	
	if infusionlib.isInfusion(infusion_choice):
		return f'''!embed -title "Replicate" -desc "You already have one {infusion} replicated, you cannot have two of the same type." -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''
	else:
		if loan:
			infusionlib.addInfusion(infusion_choice)
			infusionlib.addLoans(infusion_choice)
			outputstring += f'''!embed -title "Replicate" -desc "Replication {infusion_choice} created\n\n{feature.text}\n" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''

		
		
		elif infusionlib.useInfusionCC(cc):
			if armor:
				infusionlib.addArmorInf(infusion_choice)
			# Note we always put the infusion on the combined list
			infusionlib.addInfusion(infusion_choice)
			outputstring += f'''!embed -title "Replicate" -desc "Replication {infusion_choice} created\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''
		else:
			outputstring += f'''!embed -title "Replicate" -desc "No more replications available\n\n**{cc}**\n{ch.cc_str(cc)}" -footer "{ctx.prefix+ctx.alias} |  by vaguely_happy"  -thumb {image}\n'''

	
return outputstring
</drac2>
