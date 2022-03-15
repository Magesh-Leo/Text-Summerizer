from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2, duration_pb2
import datetime
import json

def create_task(uid,url,payload):
    # Create a client.
    client = tasks_v2.CloudTasksClient()

    # TODO(developer): Uncomment these lines and replace with your values.
    project = 'demoapp-containerize'      #'my-project-id'
    queue = 'text-summerizer-Q'
    location = 'asia-south1'
    url = url
    payload = {"text" : payload}   #or {'param': 'value'} for application/json
    in_seconds = 180
    task_name = uid
    deadline = 900

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        "http_request": {  # Specify the type of request.
            "http_method": tasks_v2.HttpMethod.POST,
            "url": url,  # The full url path that the task will be sent to.
        }
    }
    if payload is not None:
        if isinstance(payload, dict):
            # Convert dict to JSON string
            payload = json.dumps(payload)
            # specify http content-type to application/json
            task["http_request"]["headers"] = {"Content-type": "application/json"}

        # The API expects a payload of type bytes.
        converted_payload = payload.encode()

        # Add the payload to the request.
        task["http_request"]["body"] = converted_payload

    if in_seconds is not None:
        # Convert "seconds from now" into an rfc3339 datetime string.
        d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

        # Create Timestamp protobuf.
        timestamp = timestamp_pb2.Timestamp()
        timestamp.FromDatetime(d)

        # Add the timestamp to the tasks.
        task["schedule_time"] = timestamp

    if task_name is not None:
        # Add the name to tasks.
        task["name"] = client.task_path(project, location, queue, task_name)

    if deadline is not None:
        # Add dispatch deadline for requests sent to the worker.
        duration = duration_pb2.Duration()
        task["dispatch_deadline"] = duration.FromSeconds(deadline)

    # Use the client to build and send the task.
    response = client.create_task(request={"parent": parent, "task": task})

    print("Created task {}".format(response.name))