This Program Simulates Admissions Office Applications For a Given Academic Cycle.
---

Table of Contents

* [Run It Yourself](#run-it-yourself)
* [What This Program Simulates](#what-this-program-simulates)
* [What Analysis Can I Do?](#what-analysis-can-i-do)


### Run It Yourself
1. Download this repository
2. Open it in an IDE (like VScode)
3. Run "Application.py"

By default, it will run with the following important parameters:
```
"simulation_name": "2015-2016 Admissions Cycle"
"uni_location": "New Mexico"
"num_applications": 4340
```

If you want to simulate a different year, a different home state location, the number 
of applications, or any other parameters, just open a file called "Config.json" and 
edit the values. <i>Just make sure any name that ends in "_distribution" adds up to 1</i>.


<br>

### What This Program Simulates
We keep track of the follow parameters. Internally, <strong>we apply a ±10% variation to all 
distributions</strong> to produce "randomness". 
```
{
  "simulation_name": "2015-2016 Admissions Cycle",
  "application_start": "2014-08-01",
  "application_end": "2015-03-15",
  "uni_location": "New Mexico",
  "application_distribution": {
    "admitted": 0.64,
    "rejected": 0.36,
    "enrolled": 0.65,
    "lost": 0.30,
    "withdrawn": 0.02,
    "under_review": 0.05
  },
  "age_distribution": {
    "<18": 0.10,
    "18-21": 0.64,
    "22-25": 0.16,
    "26-30": 0.07,
    "30+": 0.03
  },
  "nationality_distribution": {
    "usa": 0.67,
    "foreign": 0.33
  },
  "state_distribution": {
    "in-state": 0.55,
    "out-of-state": 0.45
  },
  "program_distribution": {
    "undecided": 0.08,
    "associates": 0.07,
    "bachelors": 0.43,
    "masters": 0.17,
    "mba": 0.15,
    "phd": 0.10
  },
  "under_scholarship_distribution": {
    "yes": 0.32,
    "no": 0.68
  },
  "first_gen_distribution": {
    "yes": 0.41,
    "no": 0.59
  },
  "days_to_apply_distribution": {
    "min": 3,
    "median": 48,
    "max": 160
  },
  "num_applications": 4340
}
```

### What Analysis Can I Do?
I compiled a few examples that you can make with this simulation under "Documentation>[Data Analysis Objectives.md](https://github.com/FerminRamos/Admissions-Office-Simulation/blob/main/Documentation/Data%20Analysis%20Objectives.md)"

Here is a snippet of that document:
```
* What proportion of applicants choose to enroll after being offered admission?
* What are the top intakes and programs and what is their impact on the total enrollment?
* How fast are we able to recruit students?
```

---
Quick links:
<br>GitHub Emojis: https://www.markdownguide.org/cheat-sheet/
<br>Progress Bars: https://github.com/gepser/markdown-progress
