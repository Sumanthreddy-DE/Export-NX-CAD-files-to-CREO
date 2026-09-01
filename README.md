# Exporting NX parts to STEP for Creo

An NX Open journal that exports a Siemens NX part to STEP AP214, the neutral format PTC Creo
reads. Written while working as a research assistant at the Chair of Engineering Design (KTmfk),
Friedrich-Alexander-Universität Erlangen-Nürnberg, where parts modelled in NX had to be handed
over to a Creo workflow.

## What an NX Open journal is

NX Open is the scripting interface into Siemens NX. A journal is a Python file that NX runs
inside its own session, so it can drive the same operations a user would reach through the menus.
Recording `File > Export > STEP` produces a working but literal script; extending that recording
into something that can be run unattended is what this repository holds.

## What the script does

`Export_CAD_NX_to_CREO.py` opens a part, reports how many bodies it found, configures a STEP
exporter and writes the file:

- Exports as AP214
- Includes solids and surfaces, excludes curves
- Sets the selection scope to the entire assembly, so components come across rather than only
  the displayed body
- Preserves colours and layers
- Verifies afterwards that the output file exists and reports its size, and if it is missing,
  lists any STEP files in the target directory to show where the export actually landed
- Closes the part and disposes of the exporter in a `finally` block, so a failed export does not
  leave a part open in the session

Progress is written to the NX listing window rather than to stdout, since that is where output
is visible when NX runs the journal.

`journal_test.py` is the raw recorded journal the script grew out of, kept for reference.

## Running it

The input and output paths are set at the top of `main()` and are currently hardcoded to the
machine the script was written on:

```python
input_part  = r"Z:\Creo\Nov_6\prt_files\DIN_471_6X0D7.prt"
output_step = r"Z:\Creo\Nov_6\STEP_files\DIN_471_6X0D7.stp"
```

Edit both to your own paths before running. Then, in NX:

```
Tools > Journal > Play
```

and select `Export_CAD_NX_to_CREO.py`. Open the listing window to follow the output.

Requires a Siemens NX installation with NX Open Python. It was written against NX 2306. There
are no external dependencies beyond NX itself.

## Scope

This handles one part per run. Converting a directory means wrapping the export in a loop over
the input folder, which is the obvious next step and is not implemented here.
