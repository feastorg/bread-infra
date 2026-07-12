# KiBot targets for a BREAD board. Copy to hardware/Makefile and set PRJ_*.
#
# CAUTION: KiBot's -s/--skip-pre SKIPS the named preflight. So the ERC target
# must skip *drc*, and the DRC target must skip *erc*. The fleet shipped these
# inverted for months: every `erc` target ran DRC and every `drc` target ran ERC.
# Both checks still executed, so nothing was missed -- but every violation was
# reported under the wrong job name, which is exactly what made a broken DRC
# look like a passing one.
#
# -i/--invert-sel with no outputs named means "preflights only, no outputs".

KIBOT?=kibot
DEBUG?=
OUT_DIR=Generated
EXTRA_OPS=--banner -1 --log $(OUT_DIR)/kibot.log $(DEBUG)
PRJ_SCH=BREAD_Slice.kicad_sch
PRJ_PCB=BREAD_Slice.kicad_pcb

.PHONY: erc drc sch_fab pcb_fab erc_and_fab drc_and_fab

# Run ERC only: skip the DRC preflight.
erc:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) -s drc -i

# Run DRC only: skip the ERC preflight.
drc:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) -s erc -i

sch_fab:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) \
		print_sch interactive_bom bom_html bom_csv

pcb_fab:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) \
		print_pcb gerbers excellon_drill gerber_drills position \
		board_top_png board_bottom_png

erc_and_fab:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) \
		print_sch interactive_bom bom_html bom_csv

drc_and_fab:
	$(KIBOT) $(EXTRA_OPS) -e $(PRJ_SCH) -b $(PRJ_PCB) -d $(OUT_DIR) \
		print_pcb gerbers excellon_drill gerber_drills position
