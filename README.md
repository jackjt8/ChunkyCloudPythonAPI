# Chunky Cloud Python API

This is a Python API which aims to make interacting with Chunky Cloud much easier by predefining all requests.

## Usage

Below is an example usage.

	import CCpythonAPI
	...
	cc = ChunkyCloud(api_key)
	job_id = cc.sumbit("scene.octree2", "scene.emittergrid", "scene.json", 64, "frame.png")
	cc.wait_and_download_all(60)
	
## Core and QoL methods

This API has been built with a few QoL methods (cancel_all(), wait_and_download_all()) which make a few bulk tasks easier by having all the code already done. You can achieve the same features by using the Core methods (submit(), fork(), incTargetSpp(), cancel(), is_complete()) but you need to be more hands on for these.

