# Pokémon Emerald Mod — Master Implementation Plan

## Purpose

This file is the top-level implementation authority for the current Pokémon Emerald mod build.

It tells Codex or any developer how to use the project documents, what to implement first, what to avoid, and how to translate the current design into safe repo edits.

This file is intentionally practical:
- it defines scope,
- it sets the implementation order,
- it separates low-risk data work from higher-risk scripting work,
- and it reduces the chance of accidental overreach.

---

## Source Hierarchy

Use the following authority order when there is ambiguity:

1. `POKEMON_GEN1_3_FULL_DETAILED_CHANGE_LOG.txt`
   - authoritative for species edits already decided
   - includes type changes, stat changes, level-up changes, egg move changes, TM changes, pre-evolution move changes, and tutor adjustments where applicable

2. `POKEBALL_REBALANCE_PLAN.txt`
   - authoritative for capture item roles, ball effects, slot replacement intent, and early-game distribution goals

3. `EMERALD_BREEDING_TASK_MATRIX_v1.txt`
   - authoritative for breeding implementation phase order and species priority
   - this is a planning-and-scope file, not permission to invent unsupported mechanics

4. This file: `MASTER_IMPLEMENTATION_PLAN.md`
   - authoritative for execution order, guardrails, and rollout strategy

If the repo structure cannot cleanly support a requested feature, prefer the smallest safe implementation that preserves design intent.

---

## Core Project Goals

The mod should achieve the following:

- make more Pokémon viable without flattening identity
- make retypes feel supported by stats and learnsets
- make Poké Balls matter more during actual play
- make breeding feel rewarding without becoming bloated or unreadable
- reduce dead or wasteful stat distributions
- preserve maintainability of the Emerald decomp
- avoid large speculative rewrites when clean table edits are enough

---

## Design Rules

### Global rules
- Do not make unrelated balance changes.
- Do not invent new mechanics unless required by the design files.
- Prefer table/data edits over custom logic when both can achieve the same result.
- Preserve existing code style and project conventions.
- Avoid broad formatting churn in unrelated files.
- Keep diffs modular and reviewable.

### Species rules
- Use the detailed change log as the authority for already-approved Pokémon changes.
- Do not add extra species edits beyond that file.
- Do not revert existing repo work unless it clearly conflicts with the approved change set.

### Breeding rules
- Breeding should refine a role, not replace a species identity.
- No flat BST rewards for bred offspring.
- Hatch rewards should stay curated, limited, and readable.
- Start with data-backed, low-risk species first.

### Poké Ball rules
- Specialist balls should matter because of encounter context, not because they are universally best.
- Great, Quick, Timer, and Heal Balls should appear early enough to shape player behavior.
- Ultra Balls should still preserve later progression value.

---

## Required Implementation Buckets

Implementation should be split into the following buckets.

### 1. Species data changes
Apply the already-approved changes from the detailed change log:
- types
- base stats
- level-up learnsets
- egg moves
- pre-evolution moves
- TM/HM compatibility changes
- move tutor changes where listed

This is the highest-priority bucket.

### 2. Poké Ball system
Implement the final active ball system and its identities:
- Poké Ball
- Great Ball
- Ultra Ball
- Master Ball
- Quick Ball
- Timer Ball
- Repeat Ball
- Level Ball
- Lure Ball
- Heal Ball

Also implement the intended slot replacement logic where needed and preserve clean item identity.

### 3. Shop / distribution edits
Implement early-game and progression-based availability for:
- Poké Ball
- Great Ball
- Heal Ball
- Quick Ball
- Timer Ball

Then phase in:
- Repeat Ball
- Level Ball
- Lure Ball
- Ultra Ball later as common premium stock

### 4. Egg hatch-time reduction
Reduce egg hatch time significantly, but do it in a controlled way that:
- preserves the value of breeding,
- reduces grind,
- does not trivialize the process completely

### 5. Breeding phase work
Implement breeding changes in the phase order defined by the breeding matrix:
- Phase 1 first
- then Phase 2
- then Phase 3
- then Phase 4

Prioritize easier and cleaner species/tasks before high-risk scripting.

---

## Detailed Implementation Order

## Phase A — Repo Audit and Mapping
Before editing anything:

1. Identify the exact repo files controlling:
   - species stats and types
   - level-up learnsets
   - egg moves
   - TM/HM compatibility
   - tutor data
   - item behavior / catch modifiers
   - marts / shop inventory
   - breeding behavior
   - egg hatch cycles / hatch timing

2. Produce a short mapping of:
   - requested feature
   - target file(s)
   - implementation type:
     - data edit
     - constant edit
     - scripting edit
     - custom logic edit

3. Flag any requested feature that is not obviously supported by current repo structure.

No speculative edits should happen before this step is complete.

---

## Phase B — Species Change Log Implementation
Implement the detailed change log first.

### Why this comes first
- it is the clearest approved content
- it is mostly deterministic
- it is the backbone for later breeding and balance work
- it reduces the chance that later systems are built on outdated species data

### Deliverables
- all approved type edits applied
- all approved stat edits applied
- all approved learnset and compatibility edits applied
- successful build or validation pass

### Risk level
Low to medium, mostly data-driven.

---

## Phase C — Poké Ball Rebalance
Implement the capture system after species edits.

### Required mechanics
- **Poké Ball**: 1.0× catch rate
- **Great Ball**: 1.5× catch rate
- **Ultra Ball**: 2.0× catch rate
- **Master Ball**: guaranteed catch
- **Quick Ball**: 4.0× on turn 1, 1.0× after
- **Timer Ball**: scales from 1.0× upward, capping at 4.0× around turn 10–12
- **Repeat Ball**: 3.5× if species already caught, 1.0× otherwise
- **Level Ball**:
  - 2.0× if player level is higher than target
  - 3.5× if at least double
  - 5.0× if at least quadruple
- **Lure Ball**: 4.0× when encountered by fishing, 1.0× otherwise
- **Heal Ball**: 1.5× catch rate and fully heals the caught Pokémon

### Slot / identity notes
If the repo structure requires repurposing weaker or lower-priority balls, follow the rebalance plan.

### Risk level
Medium.
Some mechanics may be simple data changes; others may require conditional logic.

---

## Phase D — Early-Game Poké Ball Distribution
After ball behavior works, implement progression and shop access.

### Recommended rollout
**Early unlimited or near-unlimited**
- Poké Ball
- Great Ball
- Heal Ball

**Early limited**
- Quick Ball
- Timer Ball

**Midgame**
- Repeat Ball
- Level Ball
- Lure Ball

**Later common stock**
- Ultra Ball

### Balance levers
Use one or more of:
- price
- limited stock
- NPC gift quantities
- badge-gated shop expansion
- field pickups

### Risk level
Low to medium depending on mart structure.

---

## Phase E — Hatch-Time Reduction
Reduce egg hatch time after core capture progression is stable.

### Implementation goal
Make breeding substantially less grind-heavy while preserving its role as a project/investment system.

### Guardrails
- do not reduce hatch time so far that breeding becomes trivial
- use a clean constant or cycle edit if possible
- avoid invasive rewrites unless the repo requires them

### Risk level
Usually low if hatch cycles are table/constant controlled.

---

## Phase F — Breeding Implementation by Matrix Phase

Use `EMERALD_BREEDING_TASK_MATRIX_v1.txt` as the phase guide.

### Phase 1 — Core Showcase Batch
- Delcatty
- Mawile
- Banette
- Castform
- Luvdisc
- Girafarig
- Plusle
- Minun
- Kecleon
- Swalot

### Phase 2 — Rewrite Batch
- Sunflora
- Farfetch'd
- Ariados
- Pinsir

### Phase 3 — Stable Expansion Batch
- Mightyena
- Tropius
- Corsola
- Absol
- Seviper
- Zangoose
- Spinda
- Chimecho
- Goldeen / Seaking
- Delibird

### Phase 4 — Light Finishing Batch
- Wigglytuff
- Noctowl

### Breeding implementation rule
For each species or line:
1. confirm the current v11 identity already exists in species data
2. identify whether the breeding reward can be implemented with existing egg move / learnset tools
3. prefer curated hatch rewards over new systemic complexity
4. only use custom logic where the design clearly requires it and the payoff justifies the risk

### Species to treat carefully
The matrix already marks some species as harder to implement cleanly:
- Castform
- Luvdisc
- Girafarig
- Kecleon
- Spinda

These should be flagged before custom scripting work begins.

---

## Safe vs Risky Work

## Usually safe
- stats
- types
- level-up learnsets
- TM/HM compatibility
- egg move table edits
- hatch-cycle constants
- mart inventories
- item prices
- simple catch multiplier edits

## Usually medium risk
- turn-based conditional catch logic
- encounter-method conditional logic
- species-caught checks for Repeat Ball if not already supported cleanly
- curated breeding packages that need rule checks

## Usually high risk
- custom breeding trigger systems
- branching offspring reward logic beyond the repo’s natural structures
- scripting that rewrites core item/breeding flow
- anything that touches broad battle or save-state logic

High-risk work should always be isolated, justified, and reported before implementation.

---

## Required Validation After Each Major Bucket

After each major bucket, run the strongest available validation supported by the repo.

### Minimum checks
- build compiles successfully
- changed files parse cleanly
- no broken references
- no obvious data table misalignment
- no unintended species regressions in edited files

### Recommended targeted checks
- sample species from the change log verify correctly in data
- Poké Ball modifiers behave as intended
- mart inventories match progression plan
- egg hatch timing is visibly reduced
- breeding phase species do not gain unintended rewards

---

## Suggested Commit / Patch Grouping

Keep changes grouped logically.

### Group 1
Species change log implementation

### Group 2
Poké Ball behavior changes

### Group 3
Shop and distribution changes

### Group 4
Egg hatch-time reduction

### Group 5
Breeding Phase 1

### Group 6
Breeding Phase 2

### Group 7
Breeding Phase 3

### Group 8
Breeding Phase 4 / cleanup

This makes rollback and debugging much easier.

---

## Expected Final Reporting Format

At the end of work, report:

1. files changed
2. changes completed
3. checks/build steps run
4. anything uncertain
5. anything skipped
6. blockers or repo limitations
7. what still needs manual review or playtesting

Be explicit when a requested feature was approximated rather than matched exactly.

---

## Final Guardrail

The goal is not to make the repo match the wording of the documents at any cost.

The goal is to implement the approved design cleanly, safely, and maintainably inside the actual Emerald decomp structure.

When there is a conflict between:
- exact prose wording,
- repo reality,
- and implementation safety,

prefer:
1. verified repo structure,
2. approved design intent,
3. smallest safe implementation path.
