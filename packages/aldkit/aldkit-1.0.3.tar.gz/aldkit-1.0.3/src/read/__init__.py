class ALD:  
    
    def __init__(self, 
                 outdir = './'
                 ):
        
        from ase import Atoms
        from ase.io.trajectory import Trajectory
        import numpy as np
        import re
        
        self.outdir = outdir
    
        def load_data(filename, head=0):
            f = open(filename, 'r')
            lines = [i.split() for i in f.readlines()[head:]]
            f.close()

            for n, i in enumerate(lines):
                for o, j in enumerate(i):
                    try:
                        lines[n][o] = float(j)
                    except:
                        lines[n][o] = j

            length = max(map(len, lines))
            y=np.array([xi+[None]*(length-len(xi)) for xi in lines])

            return y
        
        
        
        self.primcell = load_data(f'{self.outdir}/cell_primitive.dat',head=1)
        self.harmprop = load_data(f"{self.outdir}/harmonic_properties.dat", head=1)
        self.eigdata = load_data(f'{self.outdir}/eigenVector.dat', head=1)        
        self.natoms = len(self.get_positions())
        self.nqpts = int((len(self.eigdata))/int(3*self.natoms))
        

    def get_cell(self):
        return self.primcell[0:3, 0:3]

    def get_direct_qpts(self):
        
        qpts = []
        for i in self.harmprop:
            if i[0] != len(qpts)-1 or len(qpts) == 0:
                qpts.append(i[2:5])

        return qpts
    
    def get_cartesian_qpts(self):
        
        qpts = []
        for i in self.harmprop:
            if i[0] != len(qpts)-1 or len(qpts) == 0:
                qpts.append(i[5:8])

        return qpts

    def get_elements(self):
        return self.primcell[3:,1]

    def get_positions(self):
        return self.primcell[3:, 2:5]
    
    def get_eigvecs(self):
        
        import re
        def flatten(list_of_lists):
            
            if len(list_of_lists) == 0:
                return list_of_lists
            if isinstance(list_of_lists[0], list):
                return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
            return list_of_lists[:1] + flatten(list_of_lists[1:])
        
        eigvecs = []
        eigvecdata1 = self.eigdata
        eigvecdata2 = np.array([flatten([re.findall(r"[-+]?\d*\.\d+|\d+", str(s)) for s in s1]) for s1 in eigvecdata1], dtype=float)
        
        real = np.array([[[0]*self.natoms*3]*self.natoms*3]*self.nqpts, dtype=float)
        imaginary = np.array([[[0]*self.natoms*3]*self.natoms*3]*self.nqpts, dtype=float)
        
        for i in eigvecdata2:
            qid = int(float(i[0]))
            print('qpt:',qid)
            modeid = int(float(i[1]))
            print('mode: ',modeid)
            r = [i[j] for j in range(3, len(i)) if j%2 == 1]
            im = [i[j] for j in range(3, len(i)) if j%2 == 0]
            real[qid][modeid] = r
            print(real[0][0])
            imaginary[qid][modeid] = im    
        
        return real, imaginary
    
    def get_frequencies(self):
        return self.harmprop[:,8]
    
    def get_heat_capacities(self):
        return self.harmprop[:,9]
    
    def get_group_velocities(self):
        return self.harmprop[:,10:13]
    
    def get_gruneissen_parameters(self):
        return self.harmprop[:,14:]
    
    def get_mean_free_paths(self):
        import numpy as np
        self.rta = load_data(f'{self.outdir}/phonon_RTA.dat', head=1)
        return np.array([np.sqrt(np.sum(i**2)) for i in self.harmprop[:,10:13]])*self.rta[:,-1]
                             
    def get_life_times(self, index=-1):
        self.rta = load_data(f'{self.outdir}/phonon_RTA.dat', head=1)
        return self.rta[:,index]   
    
    def get_band_structure(self):
        
        data = load_data(f'{self.outdir}/directional_harmonic_properties.dat', head=1)
        distances = data[:, 8]
        bands =[[]]*3*self.natoms
        
        for i in self.harmprop:
            bands[int(float(i[1]))].append(i[9])
        
        return distances, bands
