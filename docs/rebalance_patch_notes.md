# Gen 3+ Move/Breeding Rebalance Patch Notes

This note records engine approximations used for the combined move import and breeding-first rebalance patch.

## Imported move behavior approximations

The 84 imported moves are fully defined as move IDs, battle data, names, descriptions, and animation-table entries. Where the vanilla Emerald battle engine lacks a native later-generation mechanic, the move uses the closest stable Gen 3 effect available:

- Pivot attacks (`U-turn`, `Volt Switch`) currently deal damage but do not force a post-hit switch.
- Berry-eating attacks (`Bug Bite`, `Pluck`) use the Gen 3 `Thief`-style steal hook as their closest stable item interaction.
- Ability suppression (`Gastro Acid`) is imported as a harmless hit/status placeholder because Gen 3 has no ability-nullification volatile.
- Entry hazards beyond Spikes (`Toxic Spikes`, `Stealth Rock`) use the existing Spikes battle effect pending a dedicated hazard system.
- Variable-power attacks (`Gyro Ball`, `Electro Ball`, `Heavy Slam`, `Acrobatics`, `Hex`, `Venoshock`) use their listed base/import role as fixed-damage approximations until custom damage callbacks are added.
- Grounding and gravity-like effects (`Magnet Rise`, `Smack Down`) are imported as stable placeholders because Gen 3 has no Ground-immunity volatile toggle for these roles.
- `Clear Smog` uses Haze-style stat clearing.
- `Freeze Shock` and `Ice Burn` use the existing two-turn Sky Attack-style flow without their exact secondary statuses.
- `Wide Guard` uses Protect-style guarding rather than full team super-effective damage halving.
- `Sky Drop` is implemented as the reworked one-turn Flying attack that lowers Speed, matching the move rework sheet's intended simplification.

## Repurposed utility approximations

The reworked utility moves are data-repointed toward stable Gen 3 effects:

- `Mud Sport`: status Ground utility that lowers Speed using the existing Speed-down script.
- `Water Sport`: self-support burn/status relief approximation via Refresh.
- `Camouflage`: Defense-up utility approximation.
- `Imprison`: Taunt-style status lockdown approximation.
- `Grudge`: Curse-style punishment approximation.
- `Flatter`: confusion-first Dark disruption; the Special Defense drop is deferred until a combined confuse + stat-drop script exists.
- `Snatch`: priority Speed-up anti-support placeholder.
- `Torment` and `Assist`: retain their stable Gen 3 scripts and updated PP/type metadata.

## Learnset distribution notes

Egg move additions from the breeding-first learnset sheet were imported into existing egg-move family blocks when the target species has a Gen 3 egg-move entry. Level-up support additions were added as level-1 bridge moves for specified species so they are legal and accessible without bloating natural level progressions. TM/HM slots were not expanded in this patch; existing TM/HM/tutor access remains intact.

## Breeding structure notes

`EGG_GROUP_WATER` is the canonical Water group. The legacy Water 1/2/3 constants alias to it, and species data now uses `EGG_GROUP_WATER`, so all old Water subgroups match behaviorally while Ditto and Undiscovered remain unchanged.
