import requests
import os
#import json

class ChunkyCloud:
  def __init__(self, api_key: str):
    self._cc_url = 'https://api.chunkycloud.lemaik.de/jobs/'
    self._api_key = api_key
    self._id_queue: Dict[str, str] = {} # This stores the ids and their corresponding output filepaths
  
  def submit(self, octree: str, emitter_grid: str, scene_file: str, samples: int, output_path: str) -> str:
    """ This will submit a job to CC and return the job ID.
      :param octree:       Path to the octree file
      :param emitter_grid: Path to the emitter grid file
      :param scene_file:   Path to the scene file
      :param samples:   SPP to use
      :param output_path:   path to eventually save the image to
    """
    
    url = 'https://api.chunkycloud.lemaik.de/jobs/'
    payload={'X-Api-Key': self._api_key,
             'chunkyVersion': '2.x',
             'transient': False,
             'targetSpp': samples}
    files=[('scene', (os.path.basename(scene_file), open(scene_file, 'rb')), 'application/json'),
           ('octre', (os.path.basename(octree), open(octree, 'rb')), 'application/octet-stream'),
           ('emittergrid', (os.path.basename(emitter_grid), open(emitter_grid, 'rb')), 'application/octet-stream')
           ]
    headers = {}
    
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    
    new_id = response.json()['_id']
    self._id_queue[new_id] = output_path
    return new_id
 
   
  def fork(self, job_id: str, scene_file: str, samples: int, output_path: str) -> str:
    """ This will fork an existing CC job and return the job ID.
      :param job_id:   Existing Job ID to use as base for fork
      :param scene_file:   Path to the scene file
      :param samples:   SPP to use
      :param output_path:   path to eventually save the image to
    """
    url = 'https://api.chunkycloud.lemaik.de/jobs/' + job_id + '/fork'
    payload={'X-Api-Key': self._api_key,
             'chunkyVersion': '2.x',
             'transient': True,
             'targetSpp': samples}
    files=[('scene', (os.path.basename(scene_file), open(scene_file, 'rb')), 'application/json')]
    headers = {}
        
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
    new_id = response.json()['_id']
    self._id_queue[new_id] = output_path
    return new_id


  def incTargetSpp(self, job_id: str, samples: int):
    """ Increment target SPP by a certain amount for particular job ID.
      :param job_id:   Existing Job ID to increment SPP on
      :param samples:   SPP to increment by
    """
    url = 'https://api.chunkycloud.lemaik.de/jobs/' + job_id
    payload={'X-Api-Key': self._api_key,
             'incTargetSpp': samples}
    headers = {}
    response = requests.request("SET", url, headers=headers, data=payload)
      
      
  def cancel(self, job_id: str):
    """ Cancel job with particular job ID.
      :param job_id:   Existing Job ID to cancel
    """
    url = 'https://api.chunkycloud.lemaik.de/jobs/' + job_id
    payload={'X-Api-Key': self._api_key,
             'cancel': True}
    headers = {}
    response = requests.request("SET", url, headers=headers, data=payload)
      
      
  def cancel_all(self):
    """ [QoL] Cancel all jobs submitted """
    while len(self._id_queue) > 0:
      for job_id, output_path in list(self._id_queue.items()):
        del self._id_queue[job_id] # Remove this item from the queue
        self.cancel(job_id)

      
  def is_complete(self, job_id: str) -> bool:
    """ Check if a particular job ID has reached target SPP.
      :param job_id:   Existing Job ID to check for completion
    """
    response = requests.request("GET", "https://api.chunkycloud.lemaik.de/jobs/" + job_id)
    contents = response.json()
    return contents['spp'] >= contents['targetSpp']


  def download_img(self, job_id: str, output_file: str):
    """ Download the result of the a particular job ID to an output file.
      :param job_id:   Existing Job ID to use download image for
      :param output_path:   path to eventually save the image to
    """
    url = 'https://api.chunkycloud.lemaik.de/jobs/' + job_id + 'latest.png'
    with requests.get(url, stream=True) as r:
        with open(output_file, 'wb') as f:
          shutil.copyfileobj(r.raw, f)
    return output_file # maybe need to return success/fail?


  def wait_and_download_all(self, poll_time: int):
    """ [QoL] Download all images for submitted jobs if complete.
      :param poll_time:   Time to wait before polling the server
    """
    while len(self._id_queue) > 0:
      time.sleep(poll_time)
      for job_id, output_path in list(self._id_queue.items()):
        if self.is_complete(job_id):
          del self._id_queue[job_id] # Remove this item from the queue
          # ^ only if successful at downloading file!!
          self.download_img(job_id, output_path)


