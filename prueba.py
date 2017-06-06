import matplotlib.pyplot as plt

plt.plot(range(10))  # Creates the plot.  No need to save the current figure.
plt.draw()  # Draws, but does not block
raw_input()  # This shows the first figure "separately" (by waiting for "enter").

plt.figure()  # New window, if needed.  No need to save it, as pyplot uses the concept of current figure
plt.plot(range(10, 20))
plt.draw()
# raw_input()  # If you need to wait here too...

# (...)

# Only at the end of your program:
plt.show()  # blocks