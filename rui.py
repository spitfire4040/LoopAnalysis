# Import Header Files
import sys
import os
import os.path
import json
#import urllib
import urllib.request
import string
import time


def trace(start):

	# set end time
	start_time = int(start)
	end_time = start_time + 86400


	# initialize data structures
	uniqueTrace = set()
	uniqueIP = set()
	uniqueEdge = set()
	src_list = set()
	dst_list = set()
	srcdst = []
	allTrace = []
	allIP = []
	nodeList = []

    # initialize edge count
	edgecount = 0

    # open node list
	with open("/home/jay/Desktop/RuiTrace/TestNodeList") as f:
		for line in f:
			for word in line.split():
				nodeList.append(word)

    # iterate through each of 195 nodes
	for node in nodeList:

		#url = "https://atlas.ripe.net/api/v2/measurements/" + node + "/results?start=" + str(start_time) + "&stop=" + str(end_time) + "&format=json", "/home/jay/RuiTrace/ripe-temp/ripe.json"
		#urllib.urlretrieve(url)
		req = urllib.request.Request("https://atlas.ripe.net/api/v2/measurements/" + node + "/results?start=" + str(start_time) + "&stop=" + str(end_time) + "&format=json")
		with urllib.request.urlopen(req) as response:
			the_page = response.read()
		outfile = open("/home/jay/Desktop/RuiTrace/ripe-temp/ripe.json", "wb")
		outfile.write(the_page)
		outfile.close()

		file_input = '/home/jay/Desktop/RuiTrace/ripe-temp/ripe.json'

		file_output = '/home/jay/Desktop/RuiTrace/ripe-temp/out_put.csv'

		fp_out = open(file_output,'w')

		with open(file_input) as temp_json:
		    data = json.load(temp_json)

		# each line is like this: src_addr:dst_name        from,hop1    from,hop2 ...
		temp_count = 0

		for item in data:
		    temp_line = item['src_addr']+':'+item['dst_addr']+'\t'
		    allIP.append(item['src_addr'])
		    allIP.append(item['dst_addr'])
		    uniqueIP.add(item['src_addr'])
		    uniqueIP.add(item['dst_addr'])
		    src_list.add(item['src_addr'])
		    dst_list.add(item['dst_addr'])
		    pair = item['src_addr'] + '\t' + item['dst_addr']
		    srcdst.append(pair)

		    for hop_count in range(len(item['result'])):

		        # check if it is empty
		        if 'result' in item and 'result' in item['result'][hop_count] and len(item['result'][hop_count]['result']) != 0:

		            # only get the first 'from' from each result
		            if 'from' in item['result'][hop_count]['result'][0]:

		                temp_line = temp_line + item['result'][hop_count]['result'][0]['from'] + ',' + str(hop_count + 1) + '\t'

		            else:
		                temp_line = temp_line + '0' + ',' + str(hop_count + 1) +'\t'
		        else:
		            pass

		    temp_count = temp_count + 1
		    fp_out.write(temp_line + '\n')

		fp_out.close()
        

		with open(file_output) as infile:

			# push traces to lists
			for line in infile:
				uniqueTrace.add(line)
				allTrace.append(line)


		# get edges
		#edgeList = set()
		starCounter = 1
		count = 1

		for item in uniqueTrace:

			# set list so it will reset
			trace = []

			# split trace and push to list
			#for item in item.split(): # changed this for Abdullah to make parsing easier
			for item in item.split('\t'):           
				if (':' in item):
					pass
				else:
                    #item = item.split('-') # changed this for Abdullah to make parsing easier
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
				if first == '0':
					first = count
					count += 1
				if second == '0':
					second = count
					count += 1

				#uniqueEdge.add(str(first) + ' ' + str(second)) # changed this for Abdullah to make parsing easier
				uniqueEdge.add(str(first) + '\t' + str(second))
				i += 1

	# all traces
	with open("/home/jay/Desktop/RuiTrace/RipeData/all_trace_" + str(start_time) + ".txt", "w") as f:
		for item in allTrace:
			f.write(item)

	# all ips
	with open("/home/jay/Desktop/RuiTrace/RipeData/all_ip_" + str(start_time) + ".txt", "w") as f:
		for item in allIP:
			f.write(item + '\n')

	# unique traces
	with open("/home/jay/RuiTrace/RipeData/unique_trace_" + str(start_time) + ".txt", "w") as f:
		for item in uniqueTrace:
			f.write(item)

	# unique ip addresses
	with open("/home/jay/RuiTrace/RipeData/unique_ip_" + str(start_time) + ".txt", "w") as f:
		for item in uniqueIP:
			f.write(item + '\n')

	# unique edges (w/o '0's counted)
	with open("/home/jay/RuiTrace/RipeData/unique_edge_" + str(start_time) + ".txt", "w") as f:
		for item in uniqueEdge:
			f.write(item + '\n')
			#item = item.split(' ') # changed this for Abdullah to make parsing easier
			item = item.split('\t')         

			if (('.' in item[0]) and ('.' in item[1])):
				edgecount += 1

	# unique src addresses
	with open("/home/jay/RuiTrace/RipeData/unique_src_" + str(start_time) + ".txt", "w") as f:
		for item in src_list:
			f.write(item + '\n')

	# unique ip addresses
	with open("/home/jay/RuiTrace/RipeData/unique_dst_" + str(start_time) + ".txt", "w") as f:
		for item in dst_list:
			f.write(item + '\n')

	# unique ip addresses
	with open("/home/jay/RuiTrace/RipeData/srcdst_" + str(start_time) + ".txt", "w") as f:
		for item in srcdst:
			f.write(item + '\n')

	# write totals to file
	with open("/home/jay/RuiTrace/RipeData/stats_" + str(start_time) + ".txt", "w") as f:
		f.write("Total IPs: " + str(len(allIP)) + '\n')
		f.write("Total Traces: " + str(len(allTrace)) + '\n')
		f.write("Total Unique IPs: " + str(len(uniqueIP)) + '\n')
		f.write("Total Unique Traces: " + str(len(uniqueTrace)) + '\n')
		f.write("Total Unique Edges: " + str(edgecount) + '\n') 
		f.write("Total Unique Sources: " + str(len(src_list)) + '\n')    
		f.write("Total Unique Destinations: " + str(len(dst_list)) + '\n')
		f.write("Total Source-Destination Pairs: " + str(len(srcdst)) + '\n')


# main function
def main(argv):

	# call trace
	start = sys.argv[1]
	trace(start)

	# trace count
	os.system("./ripe_tracecount " + start)

	# ip count
	os.system("./ripe_ipcount " + start)

# initiate program
if __name__ == '__main__':      
	main(sys.argv)
