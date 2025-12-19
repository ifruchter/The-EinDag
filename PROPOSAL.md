# The EinDag — Final Project Pitch

**The EinDag** is a lightweight web dashboard for **aquaculture farm operators** that turns messy **tank CSV exports** into fast, clear insights.

### The problem
Operators routinely:
- Export CSVs from sensor platforms / spreadsheets
- Manually clean columns, filter by tank, and rebuild charts in Excel
- Miss early warnings (e.g., low dissolved oxygen, high ammonia) because analysis is slow and inconsistent

### The solution
The EinDag provides a simple flow:
1. **Log in**
2. **Drag & drop a CSV**
3. Automatically:
   - Previews the data
   - Computes summary statistics
   - Generates charts (line, pie, bar)
   - Writes shareable output files (JSON + CSV)

### Why it’s different
Instead of a “bird’s eye view” management dashboard, The EinDag focuses on the operator’s reality:
- CSV-first workflow (works with the files they already have)
- Fast, visual “tank-by-tank” inspection

### Future build-on ideas
- Per-tank “health alerts” and thresholds
- Multi-file projects + trend comparison across weeks
- Role-based views for operators vs. managers
- Real authentication + database storage
