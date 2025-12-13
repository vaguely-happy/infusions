multiline
<drac2>
# Parse arguments and get character information
a = &ARGS&
alev = int(get("ArtificerLevel", 0))
ch = character()
name = ch.name
args = argparse(&ARGS&)
charimage = get("image")
outputstring = ""

# Get spell slot level from arguments, default to 1
slotlist = args.get('l')
slot = int(slotlist[0]) if slotlist else 1
item_input = &ARGS&[0]

ecc="Font Spell Level " + slot

# Character and class setup
ch = character()
cclass = "Artificer"
infusion = item_input

# Load infusion library
using(
    infusionlib="52f4547e-72c5-4d34-a930-14367d4c1db5"
)

# Get all available infusions and setup footer
features = infusionlib.getInfusions()
footer = f'''-thumb "{charimage}" -footer "{ctx.prefix+ctx.alias} charge |  by the1inpink" '''

# Search for matching infusion
feature = []
for x in features:
    if infusion.lower() in x.lower():
        feature = x
        break
    else:
        feature = None


# Check if no matching infusion was found
if feature is None:
    return f"""embed -title "Whoops something is off with your Infusion" -desc "The infusion **{infusion}** does not seem to match an item you replicated." -f " Your current infusions are **{features}** Please check if you entered the name correctly."  {footer} """

# Match the infusion to get full details
infusions = infusionlib.matchInfusion(feature)


# Check if character is at least level 6 Artificer
if alev < 6:
    return f"""embed -title "Whoops! something is off with your Artificer Level" -desc "You need to be at least level 6 Artificer to charge items with spell slots." -f "Please ensure you are the correct class and level before trying again" {footer} """

# Validate the infusion is a valid Replicate Item
if not infusionlib.isInfusion(infusions):
    return f"""embed -title "Oh No! something is off with your Infusion" -desc "The infusion **{infusions}** does not seem to be a valid Replicate Item infusion. Please check if you entered the name correctly, then try again." {footer} """

# Check if custom counter exists for the infusion
if not ch.cc_exists(infusions):
    return f"""embed -title "Oh No! something is off with your Custom Counters" -desc "You don't seem to have a custom counter for the **{infusions}**." -f "You'll want to run the !{ctx.prefix+ctx.alias} alias to create the magic item before charging it with a spell slot. " {footer} """

useslot = True
# Check if character has the required spell slot available
if ch.spellbook.get_slots(slot) <= 0:
    if ch.cc_exists(ecc):
    	if ch.get_cc(ecc) > 0:
    		useslot = False
    if useslot:		
    	return f"""embed -title "Oh No! Insufficient Spell Slots" -desc "You don't have any level {slot} spell slots remaining to charge the **{infusions}**." {footer} """

# Check if infusion is already at maximum charges
if ch.get_cc(infusions) >= ch.get_cc_max(infusions):
    return f"""embed -title "Oh No! Infusion Already at Max Charges" -desc "Your **{infusions}** is already at its maximum charge capacity of {ch.get_cc_max(infusions)} charges." -f "You will need to expended some charges before you try again!" {footer} """

# Process the charging of the infusion
else:
    # Deduct spell slot
    if useslot:
        currslots = ch.spellbook.get_slots(slot)
        newslots = currslots - 1
        ch.spellbook.set_slots(slot, newslots)
    else:
        ch.mod_cc(ecc,-1)
    
    # Get current charge information
    currentcharges = ch.get_cc(infusions)
    maxcharges = ch.get_cc_max(infusions)
    leftcharges = maxcharges - currentcharges
    
 
    # Add charges to the infusion
    ch.mod_cc(infusions, +slot)
    
    # Format output strings
    en = f"{infusions}|{ch.cc_str(infusions) if ch.cc_exists(infusions) else '*None*'} (+{slot})"
    f = f"Level {ch.spellbook.slots_str(slot)} (-1) " if useslot else f'''{ecc} : {ch.cc_str(ecc)} (-1) '''
    
    # Return success message
    return f"""embed -title "Successfully Charged {infusions}!" -desc "You have charged your **{infusions}** with a level {slot} spell slot." -f "**Spell Slots** \n {f}" -f "**Infusion Charge Added** \n {en}" {footer} """

# Debug return (should not reach here)
return f"""embed -title "I captured the following info" -desc "You want to charge a(n) **{infusions}** with a level {slot} spell slot requested by {name} who is level {alev} {cclass}. infused: **{infusions}**" """

</drac2>

