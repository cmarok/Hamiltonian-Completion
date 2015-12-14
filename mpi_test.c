#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include <math.h>

#define MASTER_TO_SLAVE_TAG 1 //tag for messages sent from master to slaves
#define SLAVE_TO_ANY_TAG 2
#define SLAVE_TO_MASTER_TAG 4 //tag for messages sent from slaves to master

int rank, size;
int count = 0;
int done = 0;

MPI_Request request;
MPI_Status status;

void increment()
{
	count++;
	if (done == 1) {
		MPI_Finalize();
	}
}

void main(int argc, char * argv[])
{
	int ierr = MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &rank); //sets rank
	MPI_Comm_size(MPI_COMM_WORLD, &size); //gets number of processes
	if (rank == 0) {		
		while (done == 0) {
			printf("%d waiting to receive from 1\n", rank);
			MPI_Recv(&done, 1, MPI_INT, 1, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD, &status);
			// printf("%d waiting to receive from 2\n", rank);
			// MPI_Recv(&done, 1, MPI_INT, 2, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD, &status);
			printf("%d waiting to send to 1\n", rank);
			MPI_Send(&done, 1, MPI_INT, 1, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD);
			// printf("%d waiting to send to 2\n", rank);
			// MPI_Send(&done, 1, MPI_INT, 2, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD);
			printf("done is currently %d according to 0\n", done);
		}
		printf("%d exiting main with count = %d\n", rank, count);
	} else if (rank == 1) {		
		while (count < 30) {
			printf("%d waiting to send to root\n", rank);
			MPI_Send(&done, 1, MPI_INT, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
			printf("%d on iteration %d and done = %d\n", rank, count, done);
			increment();
			printf("%d waiting to receive from root\n", rank);
			MPI_Recv(&done, 1, MPI_INT, 0, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &status);
		}
		done = 1;
		printf("%d sending %d to root\n", rank, done);
		MPI_Send(&done, 1, MPI_INT, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
		printf("%d exiting main with count = %d\n", rank, count);
	} else {
		while (count < 40) {
			printf("%d waiting to send to root\n", rank);
			MPI_Send(&done, 1, MPI_INT, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
			printf("%d on iteration %d and done = %d\n", rank, count, done);
			increment();
			printf("%d waiting to receive from root\n", rank);
			MPI_Recv(&done, 1, MPI_INT, 0, MASTER_TO_SLAVE_TAG, MPI_COMM_WORLD, &status);
		}
		done = 1;
		printf("%d sending %d to root\n", rank, done);
		MPI_Send(&done, 1, MPI_INT, 0, SLAVE_TO_MASTER_TAG, MPI_COMM_WORLD);
		printf("%d exiting main with count = %d\n", rank, count);
	}
	MPI_Finalize();
	return;
}