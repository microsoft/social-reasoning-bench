We want to test and isolate the effect of the malicious strategies on duty of care in our dataset

# step 1: construct data

Go to 2-25-split-whimsical/strategies/duty_of_care, and select strategy:

- 7,8,1,5,6. these were shown the have the most effect on duty of care

Then apply each of these to the small dataset in data/calendar-scheduling/final/small.yaml

See /home/willepperson/workspaces/sage/data/calendar-scheduling/final/small-malicious-whimsical-duty-of-care.yaml for how the prompt should be formatted. The strategy must appear in the requestor instruction message with a similar format. For a dataset variant, the same strategy is inserted into each request.

This will give us 5 new datasets. I want them stored in data/calendar-scheduling/final/malicious-whim-variants/small-malicious-whimsical-duty-of-care-strat-{i}.yaml

# step 2: set up experiment

I now want to run an experiment on this data. The setup will be similar to:

/home/willepperson/workspaces/sage/experiments/2-26-full-sweep/experiment_full_sweep.py

- data: We will use each of these new 5 datasets, along with the 5 variants of small we already have for 10 datasets in total.
- requestor: gpt-4.1
- assistants: gemini, gpt 4.1, and gpt-5.2
- prompt: default
- prefs: run with both hidden and exposed

# step 3: plot results

I want a graph that is essentially a grid. 3 subplots stacked on top of each other, one for each assistant model. Then within each a row for hidden prefs and exposed prefs.
The columns should be aligned for each of the 10 datasets.

In total, I think this will be 60 unique experiment variants that are plotted.

The entire plot should be a heatmap with a green color scale plotting duty of care. higher is better so should be darker green with lower as light green (0 to 100 scale.)
