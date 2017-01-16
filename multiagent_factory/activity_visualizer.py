import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random as rn
import time
import os

plt.ion()

class ActivityVisualizer(object):
    
    def __init__(self, factory):
        self._factory = factory
        self.agent_record = {}
        self.fig, self.ax = plt.subplots()
        self.fig.set_size_inches(19.2, 10.8)
        self.ax.set_title("Agent Activity")
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Agents')
        self.ticks = [""]
        self.start_time = time.strftime("%Y%m%d-%H%M%S")
        self.img_iter = 0
    
    def init_agent(self,agent,state,t):
        if agent in self.agent_record:
            print("Warning: attempt to duplicate agent in record")
        else:
            agent_num = len(self.agent_record.keys()) + 1
            agent_color = (0.0,rn.random()*0.9,rn.random()*0.9)
            self.agent_record[agent]={'stop_times':[],'agent_num':agent_num,'color':agent_color}
            if (state):
                self.agent_record[agent]['state']=True
                self.agent_record[agent]['start_times']=np.array([t],dtype=float)
            else:
                self.agent_record[agent]['state']=False
                self.agent_record[agent]['start_times']=np.array([],dtype=float)
            self.ax.add_patch(patches.Rectangle((0.0, float(self.agent_record[agent]['agent_num']) - 0.4), 0.0, 0.8))
            self.ticks.append(agent)
            self.ax.set_yticklabels(self.ticks)

            
        
    def update(self, agent_states):
        for agent in agent_states:
            if agent not in self.agent_record:
                self.init_agent(agent,agent_states[agent],self._factory.time)
            else:
                if agent_states[agent] != self.agent_record[agent]['state']:
                    self.agent_record[agent]['state'] = agent_states[agent]
                    if agent_states[agent]:
                        self.agent_record[agent]['start_times'] = np.append(self.agent_record[agent]['start_times'],self._factory.time)
                    else:
                        self.agent_record[agent]['stop_times'] = np.append(self.agent_record[agent]['stop_times'] , self._factory.time)
                        self.ax.add_patch(patches.Rectangle(
                            (self.agent_record[agent]['start_times'][-1], float(self.agent_record[agent]['agent_num']) - 0.4), 
                            self.agent_record[agent]['stop_times'][-1] - self.agent_record[agent]['start_times'][-1], 
                                0.8,color=self.agent_record[agent]['color']))
                        self.ax.autoscale_view()
                        self.ticks[self.agent_record[agent]['agent_num']] = agent + ": " + str(int(100.0*float(sum(self.agent_record[agent]['stop_times']-self.agent_record[agent]['start_times'])/float(self._factory.time)))) + "%"
                        self.ax.set_yticklabels(self.ticks)
                        
                        #uncomment block for gif creation
                        self.make_gif()
                        
                        
                        plt.draw()
        plt.yticks(np.arange(0, len(self.agent_record)+1, 1))
        #plt.yticks()
        plt.tick_params(axis='both', which='both', right='off', left='off')
        plt.ylim([0, len(self.agent_record)+1])


    def dump(self):
        for agent in self.agent_record:
            print(agent)
            for item in self.agent_record[agent]:
                print '\t' + item + ": ", self.agent_record[agent][item]
                
    def save(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        plt.tight_layout()
        #plt.savefig('img/activity-vis_' + timestr + '.png',dpi=100)
								
    def make_gif(self):
        if not os.path.exists('img/'+self.start_time):
            os.makedirs('img/'+self.start_time)															
        plt.tight_layout()
        #plt.savefig('img/' + self.start_time + '/' + str(self.img_iter).zfill(4) + '.png',dpi=100)
        self.img_iter += 1
        
   
def test():
    import time    
    
    agent_states={'trans_1':None,'trans_2':None, 'drill_1':None, 'drill_3':None, 'drill_2':None, 'press_1':None}
    t = 0
    
    av = ActivityVisualizer()
    
    for i in range(t,200):
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
