
# Survival

### What is "Survival" Analysis?

- branch of statistics focused on analyzing time to an event.
- "Survival": the event of interest does not occur.
- "Survival Duration": time until the event of interest occurs (or the end of the observation).

### What is "Censoring"?

- occurs if a subject has not experienced the event of interest by the end of data collection.
  - loss to follow-up
  - withdrawal
  - no event by end of study period
- "event free" = made it to the end of the trial (false)
- "event before" = patient experienced the event (true)
- "sensored before" = patient dropped out

### What is "Survival" Data?

- consists of a distinct start and end time
  - ie. surgery to death
  - ie. start of treatment to progression
- consists of a status to indicate if the event occurred or was censored.

| Target | Status |
| :----: | :----: |
|   16   |   0    |
|   25   |   1    |

\* "Status == 0" means the event is censored. <br /> \* "Status == 1" means the event was observed.

\*\* What type of split between censor/observed data points are we looking for: at least 50 %

### Plot of Data

```
                  |
                1 | -------------------> o (observed)
                  |
                2 | ----> x (censored)
                  |
(individuals)   3 | --------------------------------------------------| x (censored)
                  |
                4 | ----------> o (observed)
                  |
                5 | -----> x (censored)
                  |
                  |_____________________________________________________
                 t=0                    (time)
```
