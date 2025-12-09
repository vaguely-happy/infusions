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


features = load_json(get_gvar("0731aeee-9e69-488b-a809-0b3e280fc7f9"))

feature = [x for x in features if not help and infusion.lower() in x.infusion.lower()]
#Check for non unique match and output 
if valid and len(feature) > 1:
	valid = False
	return infusionlib.duplicateMessage(feature)
elif valid and len(feature) == 0:
	return infusionlib.noMatchFound(infusion)
elif valid :
	feature = feature[0]
		
if help:
	helptext = get_gvar("39ba85fc-9ea5-4ed2-af57-e37242fe5267")
	outputstring += f'''!embed -title "{name} Needs replicate help" -desc "{helptext}" -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" \n'''
else:
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

	
	
return outputstring
</drac2>
