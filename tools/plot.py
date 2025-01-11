# read train from log and plots metrics
import os, matplotlib.pyplot as plt, numpy as np, sys
if len(sys.argv) == 1: print("You forgot the log path!"); exit()
with open(sys.argv[1]) as f: 
    results = {m:list() for m in ["models", "reasonable", "reasonable_small", "heavy", "all"]}
    lines = f.read().splitlines()
    for i, l in enumerate(lines):
        if "Reasonable" in l:
            sl = l.split()
            results["models"].append(lines[i+1].split()[8])
            results["reasonable"].append(float(sl[5].split("%")[0])/100)
            results["reasonable_small"].append(float(sl[7].split("%")[0])/100)
            results["heavy"].append(float(sl[9].split("%")[0])/100)
            results["all"].append(float(sl[11].split("%")[0])/100)
print(results)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
x_axis, y_axis = "iter", "mr"
# Plot for reasonable
ax1.set_title('reasonable')
ax1.set_xlabel(x_axis)
ax1.set_ylabel(y_axis)
ax1.plot(results["models"], results["reasonable"], "-o")
ax1.set_xticklabels(results["models"], rotation=90)

# Plot for reasonable_small
ax2.set_title('reasonable_small')
ax2.set_xlabel(x_axis)
ax2.set_ylabel(y_axis)
ax2.plot(results["models"], results["reasonable_small"], "-o")
ax2.set_xticklabels(results["models"], rotation=90)

# Plot for heavy
ax3.set_title('heavy')
ax3.set_xlabel(x_axis)
ax3.set_ylabel(y_axis)
ax3.plot(results["models"], results["heavy"], "-o")
ax3.set_xticklabels(results["models"], rotation=90)

# Plot for all
ax4.set_title('all')
ax4.set_xlabel(x_axis)
ax4.set_ylabel(y_axis)
ax4.plot(results["models"], results["all"], "-o")
ax4.set_xticklabels(results["models"], rotation=90)

plt.tight_layout()
plt.savefig('plots.png', bbox_inches='tight')
plt.close()