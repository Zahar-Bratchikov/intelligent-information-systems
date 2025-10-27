# IF-THEN CLIPS rules

This folder contains a CLIPS implementation of the IF-THEN rules from `if-then.md`.

Files:

- `if_then.clp` — CLIPS rules and example `deffacts` for testing.

How to run (assuming CLIPS is installed):

1. Start CLIPS:

   clips

2. In the CLIPS prompt, load the file and run:

   (clear)
   (load "lab1/if_then.clp")
   (reset)
   (run)

The file includes an `example-person` deffacts. You can edit or remove it and assert custom `(person ...)` facts instead. Example of asserting a custom person:

   (assert (person (budget 120000) (health-restrictions no) (want-sea no) (want-mountains yes) (want-excursions no) (has-transport no) (season winter) (short-trip yes)))
   (run)

Notes:
- Attributes are represented as slots on the `person` template.
- Derived boolean flags are asserted as `(availability (name ...) (value yes|no))` facts and final recommendations are asserted as `(result <place>)` facts which are printed and retracted by the `print-results` rule.
