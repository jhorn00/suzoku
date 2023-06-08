# suzoku
This is a personal project to solve any (valid) sudoku board with opencv and Python. Name inspired by my aunt Suzanne (Zani).

I hope to learn a lot about Python and Computer Vision through this program.

This readme will be updated when the project reaches a more complete state. As of now I update the project intermittently when I find the time (working full-time and spending the weekends in another city).

## Note
I decided to forego a trained board detection model initially to practice CV basics and write up some simple logic to detect boards with some level of accuracy. As evidenced by the output directory, there is some level of success.

I do plan to train a model eventually, it's just a matter of timing.

## TODO
 - detectCandidates() will return a list with the cropped original image. Later, it may be desireable to move back to returning crops of the prepped image. For development, it would be nicer to leave as-is.
 Needed for future features:
- better method for specifying input and output
- venv and package management for publication
- trained board model for messy images
- most likely want a way to toggle simple board detection using current CV logic and a trained model
- detectBoard function to select detection method and make calls accordingly


## References:

https://www.ams.org/notices/200904/tx090400460p.pdf

https://en.wikipedia.org/wiki/Sudoku_solving_algorithms

https://en.wikipedia.org/wiki/Backtracking

https://www.geeksforgeeks.org/sudoku-backtracking-7/
