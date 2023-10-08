import numpy as np
import math

class TrafficGenerator:
    def __init__(self, max_steps, n_cars_generated):
        self._n_cars_generated = n_cars_generated  # how many cars per episode
        self._max_steps = max_steps
    
    def generate_routefile(self, seed):
        """
        Generation of the route of every car for one episode
        """
        np.random.seed(seed)  # make tests reproducible

        # the generation of cars is distributed according to a weibull distribution
        timings = np.random.weibull(2, self._n_cars_generated)
        timings = np.sort(timings)

        # reshape the distribution to fit the interval 0:max_steps
        car_gen_steps = []
        min_old = math.floor(timings[1])
        max_old = math.ceil(timings[-1])
        min_new = 0
        max_new = self._max_steps
        for value in timings:
            car_gen_steps = np.append(car_gen_steps, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

        car_gen_steps = np.rint(car_gen_steps)  # round every value to int -> effective steps when a car will be generated

        # produce the file for cars generation, one car per line
        with open("C:\TRAFFIC SYSTEM\SUMO222\Deep-QLearning-Agent-for-Traffic-Signal-Control-1\TLCS\intersection\episode_routes.rou.xml", "w") as routes:
            print("""<routes>
            <vType id="bus" length="7.00" minGap="2.50" maxSpeed="15.00" vClass="bus" height="2.40" color="yellow" accel="1.0" decel="4.5" sigma="0.5"/>

            <route id="E_W" edges="E2TL TL2W"/>
            <route id="W_E" edges="W2TL TL2E"/>
            <route id="U_T1" edges="W2TL TL2W"/> 
            <route id="U_T2" edges="W2TL TL2W"/>
            <route id="U_T3" edges="E2TL TL2E"/>
            <route id="U_T4" edges="E2TL TL2E"/>""", file=routes)

            for car_counter, step in enumerate(car_gen_steps):
                straight_or_turn = np.random.uniform()
                if straight_or_turn < 0.75:  # choose direction: straight or turn - 75% of times the car goes straight
                    route_straight = np.random.randint(1, 5)  # choose a random source & destination
                    if route_straight == 1:
                        print('    <vehicle id="bus_E_W_%i" type="bus" route="E_W" depart="%s" departLane="3" departSpeed="10" />' % (car_counter, step), file=routes)
                    else:
                        print('    <vehicle id="bus_W_E_%i" type="bus" route="W_E" depart="%s" departLane="3" departSpeed="10" />' % (car_counter, step), file=routes)
                else:  # car that turn -25% of the time the car turns
                    route_turn = np.random.randint(1, 9)  # choose random source source & destination
                    if route_turn == 1:
                        print('    <vehicle id="car_T1_%i" type="car" route="U_T1" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 2:
                        print('    <vehicle id="car_T2_%i" type="car" route="U_T2" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 3:
                        print('    <vehicle id="car_T3_%i" type="car" route="U_T3" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 4:
                        print('    <vehicle id="car_T4_%i" type="car" route="U_T4" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 5:
                        print('    <vehicle id="motorcycle_T1_%i" type="motorcycle" route="U_T1" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 6:
                        print('    <vehicle id="motorcycle_T2_%i" type="motorcycle" route="U_T2" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 7:
                        print('    <vehicle id="motorcycle_T3_%i" type="motorcycle" route="U_T2" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    elif route_turn == 8:
                        print('    <vehicle id="motorcycle_T4_%i" type="motorcycle" route="U_T3" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)

            print("</routes>", file=routes)
