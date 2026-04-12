# RSIM CVPR IMW 2026 Talk — Manim video pipeline
QUALITY   ?= h
SCENES    := S01_Title S02_PhysicsGap S03_Question S04_Pipeline S05_Tiled \
             S06_Leaderboard S07_DINO S08_Protocol S09_Affine S10_Cross \
             S11_Pareto S12_Recipe

.PHONY: build clean

build: final.mp4

# Render all scenes
media/videos/script/1080p60/%.mp4: script.py
	manim render -q$(QUALITY) script.py $*

# Concatenate scenes into final video
final.mp4: $(foreach s,$(SCENES),media/videos/script/1080p60/$(s).mp4) concat.txt
	ffmpeg -y -f concat -safe 0 -i concat.txt -c copy $@

clean:
	rm -rf media __pycache__
