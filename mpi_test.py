from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

done = False

def increment():
	global count
	global done
	count += 1
	print rank, "is at", count
	done = comm.bcast(done, root=1)
	if done: 
		print rank, "exiting with count=", count
		MPI.Finalize()

def main():
	global done
	count = 0
	if rank == 0:
		while count < 1700:
			count += 1
			print rank, "is at", count
			done = comm.bcast(done, root=1)
			if done:
				print rank, "exiting with count=", count
				
			# increment()
	elif rank == 1:
		while count < 1700:
			count += 1
			print rank, "is at", count
			done = comm.bcast(done, root=1)
			if done:
				print rank, "exiting with count=", count
				
			# increment()
		done = True
		done = comm.bcast(done, root=rank)
	else:
		while count < 999:
			count += 1
			print rank, "is at", count
			done = comm.bcast(done, root=1)
			if done:
				print rank, "exiting with count=", count
				
			# increment()
	print rank, "exiting from main. Done =", done, "Count =", count
	MPI.Finalize()

main()