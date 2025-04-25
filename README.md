EXPERIMENT 11

Code :

#include<stdio.h>

int main()
{
int queue[20], n, head, i, j, k, seek=0, max, diff;
float avg;

printf("Enter the max range of disk : \n");
scanf("%d", &max);

printf("Enter the size of queue request : \n");
scanf("%d", &n);

printf("Enter the queue of disk positions to be read : ");
for(i=1;i<=n;i++)
scanf("%d", &queue[i]);

printf("Enter the initial head position : \n");
scanf("%d", &head);

queue[0]=head;
for(j=0;j<=n-1;j++)
{
diff=abs(queue[j+1]-queue[j]);
seek+=diff;
printf("Disk head moves from %d to %d with seek %d\n", queue[j], queue[j+1], diff);
}

printf("Total seek time is %d\n", seek);
avg=seek/(float)n;
printf("Average seek time is %f\n", avg);
return 0;
}


EXPERIMENT 10

Code :

#include<stdio.h>

int main()
{
int i, j, n, a[50], frame[10], no, k, avail, count=0;

printf("\n ENTER THE NUMBER OF PAGES : ");
scanf("%d", &n);

printf("\n ENTER THE PAGE NUMBER : \n");
for(i=1;i<=n;i++)
scanf("%d", &a[i]);

printf("\n ENTER THE NUMBER OF FRAMES : ");
scanf("%d", &no);

for(i=0;i<no;i++)
frame[i]= -1;

j=0;
printf("REFERENCE STRING \t PAGE FRAMES\n");
for(i=1;i<=n;i++)
{
printf("%d\t\t",a[i]);
avail=0;
for(k=0;k<no;k++)
if(frame[k]==a[i])
avail=1;
if (avail==0)
{
frame[j]=a[i];
j=(j+1)%no;
count++;
for(k=0;k<no;k++)
printf("%d\t", frame[k]);
}
printf("\n");
}

printf("\n PAGE FAULT :%d", count);
return 0;
}



EXPERIMENT 09

Code : 

#include<stdio.h>
void main()
{
int bsize[10], psize[10], bno, pno, flags[10], allocation[10], i, j; 
for(i=0;i<10;i++)
{
flags[i]=0;
allocation[i]=-1;
}
printf("\n\n Enter no. of blocks : ");
scanf("%d", &bno);
printf("\n Enter size of each block : \n");
for(i=0;i<bno;i++)
scanf("%d", &bsize[i]);
printf("\n Enter no. of processes : ");
scanf("%d", &pno);
printf("\n Enter size of each process :\n");
for(i=0;i<pno;i++)
scanf("%d", &psize[i]);
for(i=0;i<pno;i++)
for(j=0;j<bno;j++)
if(flags[j]==0 && bsize[j]>=psize[i])
{
allocation[j] = i; 
flags[j] = 1;
break;
}
printf("\n BLOCK NO.\tSIZE\t\tPROCESS NO.\t\tSIZE"); 
for(i=0;i<bno;i++)
{
printf("\n%d\t\t%d\t\t", i+1, bsize[i]);
if(flags[i] == 1)
    printf("%d\t\t\t%d", allocation[i]+1, psize[allocation[i]]);
else
    printf("Not allocated !!");
}
}




EXPERIMENT 08

AIM : Write a C program to demonstrate the concept of deadlock avoidance through Banker’s algorithm.

RESOURCE REQUIRED : Online C compiler or Turbo C

THEORY : Mention some basic theory from notes
(You may include definition, algorithm, advantages, disadvantages)

CONCLUSION : Hence,  the concept of deadlock avoidance using Banker’s algorithm was successfully implemented.

------------------------------------------------------------------------------

Code : 

#include <stdio.h>
#include <stdbool.h>

// Number of processes
#define P 5

// Number of resources
#define R 3

// Function to find the need of each process
void calculateNeed(int need[P][R], int max[P][R], int allot[P][R])
{
    for (int i = 0; i < P; i++)
        for (int j = 0; j < R; j++)
            need[i][j] = max[i][j] - allot[i][j];
}

// Function to check if the system is in a safe state or not
bool isSafe(int processes[], int avail[], int max[][R], int allot[][R])
{
    int need[P][R];
    calculateNeed(need, max, allot);
  
    bool finish[P] = {0};
    int safeSeq[P];
  
    int work[R];
    for (int i = 0; i < R; i++)
        work[i] = avail[i];
  
    int count = 0;
    while (count < P)
    {
        bool found = false;
        for (int p = 0; p < P; p++)
        {
            if (!finish[p])
            {
                int j;
                for (j = 0; j < R; j++)
                    if (need[p][j] > work[j])
                        break;
  
                if (j == R)
                {
                    for (int k = 0 ; k < R ; k++)
                        work[k] += allot[p][k];
  
                    safeSeq[count++] = p;
  
                    finish[p] = 1;
  
                    found = true;
                }
            }
        }
  
        if (found == false)
        {
            printf("System is not in a safe state");
            return false;
        }
    }
  
    printf("System is in a safe state.\nSafe sequence is: ");
    for (int i = 0; i < P ; i++)
        printf("%d ",safeSeq[i]);
  
    return true;
}

int main()
{
    int processes[] = {0, 1, 2, 3, 4};
  
    // Available instances of resources
    int avail[] = {3, 3, 2};
  
    // Maximum R that can be allocated to processes
    int max[][R] = {{7, 5, 3},
                    {3, 2, 2},
                    {9, 0, 2},
                    {2, 2, 2},
                    {4, 3, 3}};
  
    // Resources allocated to processes
    int allot[][R] = {{0, 1, 0},
                      {2, 0, 0},
                      {3, 0, 2},
                      {2, 1, 1},
                      {0, 0, 2}};
  
    // Check if the system is in a safe state or not
    isSafe(processes, avail, max, allot);
  
    return 0;
}



EXPERIMENT : 07

Aim - Write a program to implement solution of Producer Consumer Problem through Semaphore.

Theory -
Mention some basic theory from notes
(You may include definition, algorithm, advantages, disadvantages)

Code -
from threading import*
import time

BUFFER_SIZE = 5
BUFFER = [0]*BUFFER_SIZE

Mutex = Semaphore(1)
Empty = Semaphore(BUFFER_SIZE)
Full = Semaphore(0)

class Producer(Thread):
    def run(self):
        global BUFFER
        for i in range(5):
            Empty.acquire()
            Mutex.acquire()
            BUFFER[i % BUFFER_SIZE] = i
            print(f"Produced item {i}")
            Mutex.release()
            Full.release()
            time.sleep(1)

class Consumer(Thread):
    def run(self):
        global BUFFER
        for i in range(5):
            Full.acquire()
            Mutex.acquire()
            item = BUFFER[i % BUFFER_SIZE]
            BUFFER[i % BUFFER_SIZE] = 0
            print(f"Consumed Item {item}")
            Mutex.release()
            Empty.release()
            time.sleep(1)

P = Producer()
C = Consumer()

P.start()
P.join()
C.start()
C.join()

Output -
Take printout

Conclusion -
Hence, the solution for producer-consumer problem using semaphores is successfully implemented.




EXPERIMENT 06
Write-up as it is.

Code :
#include <stdio.h>
struct Process
{
    int WT, AT, BT, TAT;
};
struct Process a[10];
void main()
{
    int i, n, count, t, temp[10], short_P;
    count = 0;
    t = 0;
    float Total_WT, Total_TAT, Avg_WT, Avg_TAT;
    printf("Enter the number of processes : ");
    scanf("%d", &n);
    printf("Enter the arrival time and burst time : \n");
    printf("AT  BT\n");
    for(i=0;i<n;i++)
    {
        scanf("%d %d", &a[i].AT, &a[i].BT);
        temp[i]=a[i].BT;
    }
    a[9].BT=10000;
    for(t=0;count!=n;t++)
    {
        short_P=9;
        for(i=0;i<n;i++)
        {
            if(a[i].BT<a[short_P].BT && (a[i].AT<=t && a[i].BT>0))
            {
                short_P=i;
            }
        }
        a[short_P].BT = a[short_P].BT-1;
        if(a[short_P].BT==0)
        {
            count++;
            a[short_P].WT = t+1-a[short_P].AT-temp[short_P];
            a[short_P].TAT = t+1-a[short_P].AT;
            Total_WT = Total_WT+a[short_P].WT;
            Total_TAT = Total_TAT+a[short_P].TAT;
        }
    }
    Avg_WT = Total_WT/n;
    Avg_TAT = Total_TAT/n;
    printf("WT\tTAT\n");
    for(i=0;i<n;i++)
    {
        printf("%d\t%d\n", i+1, a[i].WT, a[i].TAT);
    }
    printf("THE AVERAGE WAITING TIME IS : %f\n",Avg_WT);
    printf("THE AVERAGE TURN AROUND TIME IS : %f\n",Avg_TAT);
    getch();
}



EXPERIMENT 05
Write-up as it is.

Code :
#include<stdio.h>
#include<conio.h>
void main()
{
    int pr, i, t, avg;
    t=0;
    avg=0;
    printf("Enter the number of processes : \n");
    scanf("%d",&pr);
    char P[10];
    int Burst_Time[10], Wait_Time[10];
    Burst_Time[0]=0;
    Wait_Time[0]=0;
    for(i=0;i<pr;i++)
    {
        printf("Enter the name of process : \n");
        scanf("%s",&P[i]);
        printf("Enter the burst time of the process : \n");
        scanf("%d",&Burst_Time[i]);
    }
    t=Wait_Time[0];
    for(i=1;i<pr;i++)
    {
        Wait_Time[i]=Wait_Time[i-1]+Burst_Time[i-1];
        t=t+Wait_Time[i];
    }
    printf("\nPROCESS\tBURST TIME\tWAITING TIME\n");
    for(i=0;i<pr;i++)
    {
        printf("P%d\t%d\t%d\t\n",i+1,Burst_Time[i],Wait_Time[i]);
    }
    avg=t/pr;
    printf("Total waiting time : %d\n",t);
    printf("Average waiting time : %d\n",avg);
    getch();
}


