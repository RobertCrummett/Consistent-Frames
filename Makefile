# Build the project
target=figure02.png

$(target): frames.sh
	bash $<

frames.sh: frames.py observation_ce.dat observation_cf.dat observation_ch.dat observation_cl.dat observation_cm.dat
	python3 $<

clean:
	rm -f observation_*
	rm -f $(target)

.PHONY: clean
