# repodanta

## role

you are working on repodanta.

repodanta is a local-first tool for understanding codebases.

your job is to help keep the project small, correct, and easy to change.

## what matters

1. keep behavior stable
2. make the smallest useful change
3. prefer plain code over clever code
4. write tests for anything that can break
5. keep the repo easy to explain

## how to think

start with the code that exists.

read before changing.

do not jump to design unless the current code shows it is needed.

when unsure, check the repo and the tests first.

## product direction

repodanta is for:

- understanding repository structure
- tracing dependencies
- finding risk in changes
- showing execution flow
- helping people build a mental model of a codebase

repodanta is not:

- a generic chatbot
- an autocomplete tool
- a code generator
- an autonomous coding agent

## working rules

- make one task small enough to review in one pass
- do not change files that are not needed
- do not add abstractions unless they remove real duplication or real coupling
- keep public behavior the same unless the task says otherwise
- if a change affects behavior, add or update a test
- if a change touches architecture, explain the tradeoff in simple words

## order of work

for any non-trivial task, do this order:

1. inspect the relevant files
2. explain what is there now
3. point out the smallest safe change
4. implement the change
5. run tests or show how to verify it
6. summarize the diff

## analysis style

use three buckets when useful:

- known: directly from the code
- inferred: reasonable conclusion from the code
- unknown: needs proof

do not blur these together.

## code style

prefer:

- short functions
- clear names
- simple data flow
- explicit imports
- boring config
- direct tests

avoid:

- hidden magic
- premature abstraction
- large refactors in the same task
- buzzwords in comments or docs

## repo-specific priorities

for repodanta, these are the current priorities:

- fix bugs first
- centralize config only when it removes real drift
- keep the analysis pipeline easy to trace
- keep retrieval logic understandable
- do not turn the project into an agent framework

## change discipline

before any refactor, ask:

- what problem is this solving?
- what breaks if we do nothing?
- what gets simpler?
- what gets harder?
- can this be smaller?

if the answer is weak, do not do the change.

## docs to keep in sync

when a change touches product direction, update:

- vision.md
- roadmap.md
- backlog.md
- personas.md

when a change touches technical structure, update:

- architecture_decisions.md
- claude_workflow.md

## output format

be direct.

keep explanations short.

do not oversell the work.

do not call things revolutionary, elegant, or intelligent unless the code really is.

## current stance

repodanta should help a developer answer:

- what is this codebase?
- how does it fit together?
- what breaks if i change this?
- what should i fix first?
- what should stay stable?

that is the product.
