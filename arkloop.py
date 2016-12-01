# import files
import sys
import os
import os.path
import urllib
import gzip
from requests.auth import HTTPBasicAuth
import requests
import time


# get day from command line args
year = sys.argv[1]
month = sys.argv[2]
day = sys.argv[3]

print ('year: ', year)
print ('month: ', month)
print ('day: ', day)

count = 0

# initialize node list
nodelist = []


def parse():
	global count

	# initialize global variables
	global day, month, year

	# open nodelist file
	f = open("/home/jay/LoopAnalysis/ark_nodes.txt", "r")

	# read nodes into list
	for item in f:
		nodelist.append(item)
	f.close()

	# re-initialize variables each time (clear)
	trace = []

	all_trace = []
	unique_trace = set()

	src = ''
	dst = ''
	hop = ''
	ip = ''
	addr = ''
	rtt = ''

	# check for directories and create if necessary
	if not os.path.exists("/home/jay/LoopAnalysis/ArkData"):
		os.makedirs("/home/jay/LoopAnalysis/ArkData")

	if not os.path.exists("/home/jay/LoopAnalysis/Processing"):
		os.makedirs("/home/jay/LoopAnalysis/Processing")

	# open files for write
	out1 = open("/home/jay/LoopAnalysis/ArkData/loop-traces.txt", "w")
	out2 = open("/home/jay/LoopAnalysis/ArkData/stats.txt", "w")

	# iterate through each team
	for x in range(1, 4):
		print("Team-" + str(x))

		for y in range(4770, 4844):
			print("Cycle-" + str(y))

			# cycle through each file for team/day
			for item in nodelist:
				print("Node-" + item)

				# remove carriage return
				item = item.strip('\n')

				# retrieve file			
				filename = "https://topo-data.caida.org/team-probing/list-7.allpref24/team-" + str(x) + "/daily/" + year + "/cycle-" + year + month + day + "/daily.l7.t1.c" + str(y) + "." + year + month + day + "." + item + ".warts.gz"

				# fetch file with requests
				r = requests.get(filename, auth=("jthom@cse.unr.edu", "sherdnig3544"))

				# open file for write
				f = open("/home/jay/LoopAnalysis/Processing/temp.gz", "wb")
				for chunk in r.iter_content(chunk_size=512 * 1024):
					if chunk:
						f.write(chunk)
				f.close()

				# use scamper to convert to text file
				os.system("zcat /home/jay/LoopAnalysis/Processing/temp.gz | sc_warts2text > /home/jay/LoopAnalysis/Processing/warts.txt")

				# open textfile for read
				f = open("/home/jay/LoopAnalysis/Processing/warts.txt", "r")

				try:
					# iterate through each line
					for line in f:

						# split line into pieces
						line = line.split()

						# build trace string (line not traceroute)
						if line[0] != 'traceroute':
							hop = line[0]
							ip = line[1]
							rtt = line[2]
							addr = ip + ',' + hop + ',' + rtt + ' '
							trace.append(addr)

						# reset and append running list each time line == traceroute
						if line[0] == 'traceroute':

							# count total traces processed
							count += 1

							# get values for src, dst
							src = line[2]
							dst = line[4]

							# check for empty list and append if good
							if not trace:
								pass
							else:

								# eliminate trailing '*'s
								while '*' in trace[-1]:
									del(trace[-1])

								# convert list to string
								trace = ''.join(trace)

								# append string to running lists
								unique_trace.add(trace)
								all_trace.append(trace)

							# reset trace
							trace = []

							# append src, dst to new trace
							trace.append(src + ':' + dst + ' ')

				except:
					pass

				# once more at end to catch last trace
				try:
					# eliminate trailing '*'s
					while '*' in trace[-1]:
						del(trace[-1])

					# convert list to string
					trace = ''.join(trace)

					# append string to running lists
					unique_trace.add(trace)
					all_trace.append(trace)
					count += 1

				except:
					pass

				f.close()

				#except:
					#print ("url does not exist")

				# write unique_trace to file
				for item in unique_trace:
					out1.write(item)
					out1.write('\n')

	# write stats
	out2.write("Unique Trace: " + str(len(unique_trace)) + '\n')
	out2.write("All Trace: " + str(len(all_trace)) + '\n')
	out2.write("Total Traces Processed: " + str(count) + '\n')

	# close files
	out1.close()
	out2.close()

def main(argv):
	# run parse
	parse()


if __name__ == '__main__':
  main(sys.argv)