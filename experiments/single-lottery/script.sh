../../reservation_generator.py -m "CP7:50,CP9:65,CP10:80,C11:110,CP12:200" -g "marconi:0" -l 20160 reservations.json > results.txt
../../scheduler.py -g "marconi" -a "lottery" -l 20160 reservations.json schedule.json >> results.txt
../../analysis.py schedule.json chart.html >> results.txt
