# Chunky Cloud Python API

This is a Python API which aims to make interacting with Chunky Cloud much easier by predefining all requests.

## Usage

Below is an example usage.

	import CCpythonAPI
	...
	api_key = ""
	cc = ChunkyCloud(api_key)

	scenedir = r"C:\Users\jackj\.chunky\scenes\default_2021-10-02_17-54-30"
	octree = os.path.join(scenedir, "default_2021-10-02_17-54-30.octree2")
	emittergrid = os.path.join(scenedir, "default_2021-10-02_17-54-30.emittergrid")
	json = os.path.join(scenedir, "default_2021-10-02_17-54-30.json")

	job_id = cc.submit(octree, emittergrid, json, 64, "frame.png")
	print(job_id)
	cc.wait_and_download_all(15)
	if os.path.isfile("frame.png"):
		print("Download completed")
	
## Core and QoL methods

This API has been built with a few QoL methods (cancel_all(), wait_and_download_all()) which make a few bulk tasks easier by having all the code already done. You can achieve the same features by using the Core methods (submit(), fork(), incTargetSpp(), cancel(), is_complete()) but you need to be more hands on for these.

