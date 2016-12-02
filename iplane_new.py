# import headers
import sys
import os
import gzip
import time

node_dict = {}


def load_dict():
	with open("/home/jay/Desktop/Final_Copies/iPlane/vp_ips", "r") as f:
		for line in f:
			test = line.split('\t')
			node_dict[test[0]] = test[1]


def parse(year, month, day):

	# initialize variables
	hop = 1
	flag = False
	src = ''
	dst = ''
	count = 1
	edgecount = 0

	# initialize variables
	trace = []
	all_trace = []
	all_ip = []
	unique_trace = set()
	unique_ip = set()
	edgelist = set()
	unique_src = set()
	unique_dst = set()
	srcdst = []

	# open nodelist
	for filename in os.listdir("/home/jay/Desktop/Final_Copies/iPlane/DataFiles/traces_" + year + "_" + month + "_" + day):
		# get file name
		node = filename[10:]

		try:
			# get ip from dictionary
			src_ip = node_dict[node]
		except:
			# if its empty...
			src_ip = '0'

		# strip end line
		src_ip = src_ip.strip('\n')
		
		# add to list
		unique_src.add(src_ip)

		# assemble string for system call
		command = "./iplane /home/jay/Desktop/Final_Copies/iPlane/DataFiles/traces_" + year + "_" + month + "_" + day + "/" + filename + " > /home/jay/Desktop/Final_Copies/iPlane/iplane-temp/temp.txt"

		# system call
		os.system(command)

		# open file to read
		with open("/home/jay/Desktop/Final_Copies/iPlane/iplane-temp/temp.txt", "r") as f:

			# iterate through each line
			for line in f:

				# split line into pieces
				line = line.split()

				# if 'destination', write and reset 
				if (line[0] == "destination:"):

					# get dst
					dst = line[1]
					dst = dst.strip('\n')

					# add to ip lists
					all_ip.append(dst)
					unique_ip.add(dst)
					unique_dst.add(dst)

					# get rid of empty line
					if trace != None:

						# remove trailing '0' addresses
						tf = True
						last = ''.join(trace[-1:])

						while(tf == True):

							last = last.split(',')
							#print(last[0])

							if(last[0] == '0'):
								del trace[-1]
								last = ''.join(trace[-1:])
							else:
								tf = False

						# push trace to lists
						all_trace.append(''.join(trace))
						unique_trace.add(''.join(trace))

					# reset lists and flag
					trace = []
					flag = False

				else:
					# collect hop and address
					hop = line[0]

					# clip : from hop
					hop = hop[:-1]
					new_hop = int(hop) + 1
					addr = line[1]

					# change 0.0.0.0 to 0
					if(addr == '0.0.0.0'):
						addr = '0'
					
					# push address, hop to list
					unique_ip.add(addr)
					all_ip.append(addr)

					# on first pass start with header
					if (flag == False):
						trace.append(src_ip + ':' + dst + '\t')
						trace.append(addr + ',' + str(new_hop) + '\t')
						srcdst.append(src_ip + '\t' + dst)

						# use flag for first pass
						flag = True

					else:
						# on not first pass, append address
						trace.append(addr + ',' + str(new_hop) + '\t')

						# add to ip lists
						all_ip.append(addr)
						unique_ip.add(addr)
		


		# find edges...
		# iterate through unique traces
		for item in unique_trace:

			# set list so it will reset
			trace = []

			# split trace and push to list
			for item in item.split():
				if (':' in item):
					pass
				else:
					item = item.split(',')
					trace.append(item[0])

			# find length of list
			length = len(trace)

			# set iterator variable so it will reset
			i = 0

			# iterate through trace list for pairs
			while i < length - 1:
				first = trace[i]
				second = trace[i+1]

				# set incrementing value for 0's
				if first == '0' and second == '0':
					# don't count 0 - 0
					pass

				else:

					if first == '0':
						first = count
						count += 1

					if second == '0':
						second = count
						count += 1

				# add to edgeList set (unique values only)
				edgelist.add(str(first) + '\t' + str(second))
				i += 1

	# open all_trace file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/all_trace_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in all_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open all_ip file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/all_ip_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in all_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_trace file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/unique_trace_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_trace:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_ip file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/unique_ip_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_ip:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_ip file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/unique_src_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_src:
			if not item:
				pass
			else:
				f.write(item + '\n')

	# open unique_ip file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/unique_dst_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in unique_dst:
			if not item:
				pass
			else:
				f.write(item + '\n')

	# open unique_ip file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/srcdst_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in srcdst:
			if not item:
				pass
			else:
				f.write(item + '\n')


	# open unique_edge file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/unique_edge_" + month + '_' + day + '_' + year + ".txt", "w") as f:

		# write list to file
		for item in edgelist:
			if not item:
				pass
			else:
				f.write(item + '\n')

			item = item.split('\t')			

			if (('.' in item[0]) and ('.' in item[1])):
				edgecount += 1

	# open stats file
	with open("/home/jay/Desktop/Final_Copies/iPlane/iPlaneData/stats_" + month + '_' + day + '_' + year + ".txt", "w") as f:
		# write stats
		f.write("Total IP: " + str(len(all_ip)) + '\n')
		f.write("Unique IP: " + str(len(unique_ip)) + '\n')
		f.write("Total Trace: " + str(len(all_trace)) + '\n')
		f.write("Unique Trace: " + str(edgecount) + '\n')
		f.write("Unique Edge: " + str(edgecount) + '\n')
		f.write("Unique Source: " + str(len(unique_src)) + '\n')
		f.write("Unique Destination: " + str(len(unique_dst)) + '\n')
		f.write("Source-Destinatioin pairs: " + str(len(srcdst)) + '\n')



def main(argv):

	# get day from command line args
	year = sys.argv[1]
	month = sys.argv[2]
	day = sys.argv[3]

	# for log file
	start = time.time()

	# load node dictionary
	load_dict()

	# run parse
	parse(year, month, day)

	# trace count
	#os.system("./iplane_tracecount " + year + ' ' + month + ' ' + day)

	# ip count
	#os.system("./iplane_ipcount " + year + ' ' + month + ' ' + day)

	# for log file
	end = time.time()

	with open("log.txt", "a") as f:
		f.write("iPlane:" + '\t' + "Start-Time-" + month + '_' + day + '_' + year + '\t' + "Runtime (minutes)-" + str((end - start)/60) + '\n')


if __name__ == '__main__':
  main(sys.argv)
