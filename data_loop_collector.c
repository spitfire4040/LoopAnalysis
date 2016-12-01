// HEADER FILES
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdbool.h>

// MAIN FUNCTION
int main(int argc, char *argv[])
{
	// initialize variables
	time_t start, end;
	float elapsed;
	int year, month, day, duration, sleep = 0;
	bool yearflag = false, monthflag = false, dayflag = false;
	char y[4];
	char m[2];
	char d[2];
	char l[2];
	char temp[3];
	char et[11];
	char arkparams[40];
	char mlabparams[40];
	char iplaneparams[40];
	char* zero = "0";
	time_t e_time;

	// outfile pointers
	FILE* outfile1;
	FILE* outfile2;

	// create struct for time
	struct tm t;

	// open log file
	outfile1 = fopen("start_time.txt", "w");


	// prompt for date:
	// year
	while (yearflag == false)
	{
		system("clear");
		printf("Enter desired year as an integer value between 2010 and 2016: ");
		scanf("%d", &year);

		// check for good input
		if((year >= 2010) && (year <= 2016))
		{
			yearflag = true;
		}
	}

	// month
	while(monthflag == false)
	{
		system ("clear");
		printf ("Enter desired month as an integer value between 1 and 12: ");
		scanf ("%d", &month);

		// check for good input
		if((month >= 1) && (month <= 12))
		{
			monthflag = true;
		}
	}

	// day
	while(dayflag == false)
	{
		system("clear");
		printf("Enter desired day as an integer value between 1 and 31: ");
		scanf("%d", &day);

		// check for good input
		if((day >= 1) && (day <= 31))
		{
			dayflag = true;
		}		
	}

	system("clear");
	printf("Enter number of days to collect: ");
	scanf("%d", &duration);

	// convert to unix epoch time
	t.tm_year = (year - 1900);
	t.tm_mon = (month - 1);
	t.tm_mday = day;
	t.tm_hour = 8;
	t.tm_min = 00;
	t.tm_sec = 00;
	t.tm_isdst = 0;
	e_time = mktime (&t);

	// convert year to string
	sprintf(y, "%d", year);

	for(int x = 0; x < duration; x++){

		// correct for 1 digit month
		if(month < 10)
		{
			strcpy(m, zero);
			sprintf(temp, "%d", month);
			strcat(m, temp);
		}

		else
		{
			sprintf(m, "%d", month);
		}

		// correct for 1 digit day
		if(day < 10)
		{
			strcpy(d, zero);
			sprintf(temp, "%d", day);
			strcat(d, temp);
		}

		else
		{
			sprintf(d, "%d", day);
		}

		sprintf(l, "%d", duration);

		// print selected date
		printf("Working: %s/%s/%s\n", m, d, y);
		printf("Duration: %s\n", l);
		printf("Unix epoch time: %ld\n", (long) e_time);

		// write unix time to start_time file for ripe
		fprintf(outfile1, "%ld", e_time);

		// run script syscalls

		// set start time for timer
		start = clock();

		/*

		// call ripe
		printf("Working Ripe...\n");
		system("python ripe.py");

		// get ending time for timer and calculate total time
		end = clock();
		elapsed = (end-start) / CLOCKS_PER_SEC;

		// print time to log file
		fprintf(outfile1, "Elapsed time for Ripe: %f", elapsed);	


		*/

		// call ark
		// set start time for timer
		start = clock();

		// build string for parameter
		strcpy(arkparams, "python3.5 arkloop.py ");
		strcat(arkparams, y);
		strcat(arkparams, " ");
		strcat(arkparams, m);
		strcat(arkparams, " ");
		strcat(arkparams, d);
		strcat(arkparams, " ");
		strcat(arkparams, l);
		printf("Working Ark...\n");
		system(arkparams);

		// get ending time for timer and calculate total time
		end = clock();
		elapsed = (end-start) / CLOCKS_PER_SEC;



		// print time to log file
		fprintf(outfile1, "Elapsed time for Ark: %f\n", elapsed);	

		/*

		// call mlab
		// set start time for timer
		start = clock();

		// build string for parameter
		strcpy(mlabparams, "python mlab.py ");
		strcat(mlabparams, y);
		strcat(mlabparams, " ");
		strcat(mlabparams, m);
		strcat(mlabparams, " ");
		strcat(mlabparams, d);
		printf("Working M-lab...\n");
		system(mlabparams);

		// get ending time for timer and calculate total time
		end = clock();
		elapsed = (end-start) / CLOCKS_PER_SEC;

		// print time to log file
		fprintf(outfile1, "Elapsed time for M-Lab: %f\n", elapsed);
		


		// call iplane
		// set start time for timer
		start = clock();

		// build string for parameter
		strcpy(iplaneparams, "python iplane_trace.py ");
		strcat(iplaneparams, y);
		strcat(iplaneparams, " ");
		strcat(iplaneparams, m);
		strcat(iplaneparams, " ");
		strcat(iplaneparams, d);
		printf("Working iPlane...\n");
		system(iplaneparams);

		// get ending time for timer and calculate total time
		end = clock();
		elapsed = (end-start) / CLOCKS_PER_SEC;

		// print time to log file
		fprintf(outfile1, "Elapsed time for iPlane: %f", elapsed);
	
		*/
		day += 1;
		e_time += 86400;
	}

	// close log file
	fclose(outfile1);

	// end program
	return 0;
}
