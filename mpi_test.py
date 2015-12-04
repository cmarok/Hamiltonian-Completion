from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
	data = [1, 2, 3]
	comm.send(data, dest=1, tag=11)
else:
	data = comm.recv(source=0, tag=11)

print "Hi I'm process", rank, "and data is", type(data)