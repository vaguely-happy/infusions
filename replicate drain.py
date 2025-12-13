multiline
<drac2>
a = &ARGS&
name,args = get("name",""),argparse(a)
arg1, arg2, arg3 = (&ARGS& + ["N/A", "N/A", "N/A"])[:3]
outputstring, deletestring = "",""
using(
    infusionlib="52f4547e-72c5-4d34-a930-14367d4c1db5")
ch = character()
cclass = "Artificer"
infusion = arg1
help = "help" in args or "?" in args
infusionset = ["passive","action-2","action"]
if get_svar("infusion_nopassive"):
	infusionset = ["action-2","action"]
	usepassive = False
cc = "Replicate Item"
ccc = "Drain Magic Item"

infusion  = infusionlib.matchInfusion(infusion)

if not ch.cc_exists(ccc):
	err("You do not have the Magic Item Tinker feature in order to be able to Drain Magic Item")
	
if ch.get_cc(ccc) < 1:
	err("You have no more uses of Drain Magic Item, you cannot drain another item until you long rest")

if "N/A" in infusion or help:
	helptext = get_gvar("39ba85fc-9ea5-4ed2-af57-e37242fe5267")
	outputstring += f'''!embed -title "{name} Needs replicate help" -desc "{helptext}"'''
else:
	
	infusion  = infusionlib.matchInfusion(infusion)
	if infusionlib.isInfusion(infusion):
		features = load_json(get_gvar("0731aeee-9e69-488b-a809-0b3e280fc7f9"))
		feature = [x for x in features if not help and infusion.lower() in x.infusion.lower()]
		if feature:
			feature = feature[0]
		common = infusion.startswith("common :")
		sl = 1 if common else 2
		ecc="Font Spell Level " + sl
		infusionlib.delInfusion(infusion)
		if feature:
			infusionlib.deleteCC(feature)
		ch.mod_cc(cc,1)
		ch.mod_cc(ccc,-1)
		outputstring = f'''!embed -title "Replicate" -desc "Drain Magic Item {infusion} \n\n{"Common item" if common else ""} creating a spell slot at level {sl}"'''
		if (ch.spellbook.get_max_slots(sl) == ch.spellbook.get_slots(sl)):
			ch.create_cc_nx(ecc,0,10,"long",dispType="bubble",reset_to=0,initial_value=0)
			ch.mod_cc(ecc,+1)
			outputstring += f''' -f "{ecc} (+1)|{ch.cc_str(ecc)}"'''
		else:
			ch.spellbook.set_slots(sl,ch.spellbook.get_slots(sl)+1)
			outputstring += f''' -f "Spell Slots (-1)|{ch.spellbook.slots_str(sl)}"'''
		if feature:
			for x in infusionset:
				if x in feature:
					actionname = infusionlib.getActionName(feature[x])
					deletestring += f'''!a delete "{actionname}"\n'''
			outputstring = deletestring + outputstring
	else:
		return f'''!embed -title "Replicate" -desc "You do not have {infusion} replicated, you cannot drain it." '''
outputstring += f''' -footer "{ctx.prefix+ctx.alias} | by vaguely_happy" -thumb {image}\n'''
return outputstring
</drac2>
