import streamlit as st
import pandas as pd
import numpy as np
import time  # <- We'll need this later as well
from wf_sim import Population

st.title('Simple Wright-Fisher Simulation of Genetic Drift')

population_size = st.slider("Population Size: ", 10,10000)
init_frequency = st.slider("Frequency: ", 0.00, 1.00)
genetarion = st.slider("Generation: ", 1, 10000)

# Create a new Population
# As a reminder these are the default values for population size (N)
# and initial derived allele frequency (f).
#   N=10, f=0.2
p = Population(population_size, init_frequency)

# Initialize the chart with the initial allele frequency of the derived
# allele. `line_chart` expects a list, so we must wrap `p.f` in square
# brackets to pass a list
chart = st.line_chart([p.f])

# Initially we'll run a loop 50 times
freq = np.sum(p.pop)/len(p.pop)


status_text = st.empty() 
status_text.markdown(f"""
	**Population Size: {population_size}**

	**Initial Frequency: {init_frequency}**

	**Generation Number: {genetarion}**

	""")


progress_text = "Operation in progress. Please wait."
complete_text = "Operation completed."
percent_complete = 0
my_bar = st.progress(percent_complete, text = progress_text)

for i in range(1, genetarion):

    status_text = st.empty() 
    # Step 1 wf generation
    p.step(ngens=1)
    # Calculate the current derived allele frequency
    freq = np.sum(p.pop)/len(p.pop)
    # Update the chart to add the current allele frequency
    chart.add_rows([freq])

    status_text.markdown(f"""

    	**Generation {i}: Frequency {freq}**

    	""")

    percent = round((i/genetarion)*100)
    my_bar.progress(percent_complete + percent, text=progress_text)

    if p.isMonomorphic() == True:

    	my_bar.progress(100, text = complete_text)
    	break
    # sleep for a small amount of time so you can watch the animation
    time.sleep(0.05)




# Add a button to rerun the simulation
st.button("Rerun")