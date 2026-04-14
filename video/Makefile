# GeoAI Talk — Manim video pipeline (2K 60fps, webm output)
# Usage:
#   make -f Makefile build SCENES="S01_CloudNativeStack S07_GeoParquetPushdown"
#   make -f Makefile scene-S12_CloudNativeVsDownload
VIDEO_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
MAKEFILE  := $(abspath $(lastword $(MAKEFILE_LIST)))
SCRIPT    := $(VIDEO_DIR)/geoai_scenes.py
THEME     := $(VIDEO_DIR)/_theme.py
OUTDIR    := $(abspath $(VIDEO_DIR)/../public/videos)
SCENES    ?= S01_CloudNativeStack S02_InferencePipeline S03_TorchGeoSampling S04_EmbeddingRetrieval \
             S05_COGByteRange S06_STACSearchFanout S07_GeoParquetPushdown S08_ContrastiveLearning \
             S09_MAEMaskedModeling S10_PixelVsPatchEmbedding S12_CloudNativeVsDownload \
             S13_ProductionPipeline S14_CNGTimeline S16_Flywheel

.PHONY: build clean

build: $(foreach s,$(SCENES),$(OUTDIR)/$(s).webm)

scene-%:
	$(MAKE) -f $(MAKEFILE) $(OUTDIR)/$*.webm

# All scenes
$(OUTDIR)/%.webm: $(SCRIPT) $(THEME)
	@mkdir -p $(OUTDIR)
	cd $(VIDEO_DIR) && uv run manim render -qh --format webm -o $(abspath $@) $(notdir $(SCRIPT)) $(notdir $(basename $@))

clean:
	rm -rf $(VIDEO_DIR)/media $(VIDEO_DIR)/__pycache__
