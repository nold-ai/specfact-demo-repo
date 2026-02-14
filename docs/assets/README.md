# Demo Visual Assets

Place the README animation at:

- `docs/assets/demo-output.gif`

## Capture instructions

1. Run the demo and save a log:
   `make demo | tee artifacts/demo-capture.log`
2. Record terminal session with your preferred tool (examples):
   - `asciinema rec artifacts/demo.cast`
   - `vhs demo.tape` (if VHS is installed)
3. Export to GIF and write to:
   `docs/assets/demo-output.gif`
4. Keep animation short (20-45 seconds) and include:
   - BLOCK result
   - explain output
   - PASS result
