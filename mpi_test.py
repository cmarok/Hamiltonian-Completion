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
	done = comm.recv(source=0)
	print rank, "got past recv"
	if done: 
		print rank, "exiting with count=", count
		MPI.Finalize()

def main():
	global done
	global count
	Py_buffer buf
	if rank == 0:
<<<<<<< Updated upstream
		while count < 1001:
			# print rank, "started iteration"
			increment()
			# print rank, "finished iteration"
=======
		while not done:
			done = comm.Irecv(buf, MPI.ANY_SOURCE)
			for i in range(1, comm.Get_size()):
				comm.send(done, dest=i)
>>>>>>> Stashed changes
	elif rank == 1:
<<<<<<< Updated upstream
		while count < 50:
			print rank, "started iteration"
=======
		while count < 1501:
			# print rank, "started iteration"
>>>>>>> Stashed changes
			increment()
			# print rank, "finished iteration"
		done = True
		comm.send(done, dest=0)
	else:
<<<<<<< Updated upstream
		while count < 1000:
			print rank, "started iteration"
=======
		while count < 499:
			# print rank, "started iteration"
>>>>>>> Stashed changes
			increment()
			# print rank, "finished iteration"
	print rank, "exiting from main. Done =", done, "Count =", count
	MPI.Finalize()

main()