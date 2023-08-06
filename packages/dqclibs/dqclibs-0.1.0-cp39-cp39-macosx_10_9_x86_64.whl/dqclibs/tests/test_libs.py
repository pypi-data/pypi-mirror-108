import dqclibs

# try loading the libraries
cgto = dqclibs.CGTO()
cint = dqclibs.CINT()
cpbc = dqclibs.CPBC()
csymm = dqclibs.CSYMM()

# test loading the functions
gto1 = getattr(cgto, "GTOval_cart")
gto2 = getattr(cgto, "GTOval_ip_cart")
cint1 = getattr(cint, "int1e_ovlp_sph")
cint2 = getattr(cint, "int1e_rrkin_sph")
