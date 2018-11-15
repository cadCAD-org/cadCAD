# from pathos.multiprocessing import ProcessingPool as Pool
#
# class Multiproc(object):
#
#     def __init__(self, fs, states_list, configs, env_processes, Ts, Ns):
#         self.fs = fs
#         self.states_list = states_list
#         self.configs = configs
#         self.env_processes = env_processes
#         self.Ts = Ts
#         self.Ns = Ns
#
#     def parallelize_simulations(self):
#         l = list(zip(self.fs, self.states_list, self.configs, self.env_processes, self.Ts, self.Ns))
#         with Pool(len(self.configs)) as p:
#             results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5]), l)
#
#         return results