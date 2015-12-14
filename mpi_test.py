from mpi4py import MPI
import pdb

# pdb.set_trace()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

done = False
count = 0

def increment():
	global count
	global done
	count += 1
	print rank, "is at", count
	done = comm.bcast(done, root=MPI.ANY_SOURCE)
	print rank, "got past bcast"
	if done: 
		print rank, "exiting with count=", count
		MPI.Finalize()

def main():
	global done
	global count
	if rank == 0:
		while count < 501:
			print rank, "started iteration"
			increment()
			print rank, "finished iteration"
	elif rank == 1:
		while count < 50:
			print rank, "started iteration"
			increment()
			print rank, "finished iteration"
		done = True
		done = comm.bcast(done, root=rank)
	else:
		while count < 1000:
			print rank, "started iteration"
			increment()
			print rank, "finished iteration"
	print rank, "exiting from main. Done =", done, "Count =", count
	MPI.Finalize()

main()