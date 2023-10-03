import greenstalk


class Beanstalk:
    def __init__(self, host='localhost', port=11300):
        self.host = host
        self.port = port
        self.client = self.connect()

    def connect(self):
        return greenstalk.Client((self.host, self.port))

    def push(self, platform, body, priority=1, ttr=3600, tube='test_push'):
        try:
            self.client.use(tube)
            self.client.put(body=body, priority=priority, ttr=ttr)
            print("success insert job {} {}".format(platform, body))
        except:
            print("failed insert job {}".format(body))

    def consume(self, tube='test_consume'):
        try:
            self.client.watch(tube)
            return self.client.reserve(10)
        except:
            print("failed consume tube {}".format(tube))

    def delete_job(self, tube, job):
        try:
            self.client.watch(tube)
            self.client.delete(job)
            print("success delete job {}".format(job.id))
        except:
            print("failed delete job `{}` in tube `{}".format(job, tube))

    def close(self):
        self.client.close()
