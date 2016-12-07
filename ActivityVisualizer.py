import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
plt.ion()

class ActivityVisualizer(object):
	
	def __init__(self, agent_states, time):
		self.agent_record = {}
		self.start_time = time
		self.current_time = time
		self.fig, self.ax = plt.subplots()
		self.lines, = self.ax.plot([],[], 'o')
		self.ticks = []
	
	def init_agent(self,agent,state,t):
		if agent in self.agent_record:
			print("Warning: attempt to duplicate agent in record")
		else:
			agent_num = len(self.agent_record.keys()) + 1
			if (state):
				self.agent_record[agent]={'state':True, 'start_times':[t],'stop_times':[],'agent_num':agent_num}
			else:
				self.agent_record[agent]={'state':False, 'start_times':[],'stop_times':[],'agent_num':agent_num}
			self.ax.add_patch(patches.Rectangle((0, float(self.agent_record[agent]['agent_num']) - 0.4), 0, 0.8))
			self.ticks.append(agent)
			plt.yticks(np.arange(1,len(self.ticks)+1),self.ticks)
			
			
		
	def update(self, agent_states, t):
		for agent in agent_states:
			if agent not in self.agent_record:
				self.init_agent(agent,agent_states[agent],t)
			else:
				if agent_states[agent] != self.agent_record[agent]['state']:
					self.agent_record[agent]['state'] = agent_states[agent]
					if agent_states[agent]:
						self.agent_record[agent]['start_times'].append(t)
					else:
						self.agent_record[agent]['stop_times'].append(t)
						self.ax.add_patch(patches.Rectangle(
							(self.agent_record[agent]['start_times'][-1], float(self.agent_record[agent]['agent_num']) - 0.4), 
							self.agent_record[agent]['stop_times'][-1] - self.agent_record[agent]['start_times'][-1], 
							0.8))
						self.ax.autoscale_view()
						plt.draw()


	def dump(self):
		for agent in self.agent_record:
			print(agent)
			for item in self.agent_record[agent]:
				print '\t' + item + ": ", self.agent_record[agent][item]
	
def test():
	import random as rn
	import time	
	
	agent_states={'transport1':True,'transport2':False, 'drill1':True, 'drill1':False, 'drill2':True, 'press':True}
	t = 0
	
	av = ActivityVisualizer(agent_states,t)
	
	for i in range(t+1,200):
		for agent in agent_states:
			if (rn.random() < 0.07):
				agent_states[agent] = False
			else:
				agent_states[agent] = True
		t = i;
		av.update(agent_states, t)
		time.sleep(.05)
	t += 1
	for agent in agent_states:
		agent_states[agent] = False
	av.update(agent_states, t)
	
	av.dump()
	plt.show(block=True)
				

if __name__ == "__main__":
    test()
