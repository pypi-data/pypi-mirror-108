
# %%
import os,sys,time,random,uuid,json,copy
from typing import SupportsRound
from dpdispatcher.JobStatus import JobStatus
from dpdispatcher import dlog
from hashlib import sha1
# from dpdispatcher.slurm import SlurmResources
#%%
default_strategy = dict(if_cuda_multi_devices=False)

class Submission(object):
    """submission represents the whole workplace, all the tasks to be calculated
    Parameters
    ----------
    work_base : str
        path-like, the base directory of the local tasks
    resources : Resources
        the machine resources (cpu or gpu) used to generate the slurm/pbs script
    forward_common_files: list
        the common files to be uploaded to other computers before the jobs begin
    backward_common_files: list
        the common files to be downloaded from other computers after the jobs finish
    machine : machine
        machine class object (for example, PBS, Slurm, Shell) to execute the jobs.
        The machine can still be bound after the instantiation with the bind_submission method.
    """
    def __init__(self,
                work_base,
                machine=None,
                resources=None,
                forward_common_files=[],
                backward_common_files=[],
                *,
                task_list=[]):
        # self.submission_list = submission_list
        self.work_base = work_base
        self.resources = resources
        self.forward_common_files= forward_common_files
        self.backward_common_files = backward_common_files

        self.submission_hash = None
        # print('Submission.__init__:task_list', task_list)
        # print('empty_list:', [])
        # warning: can not remote .copy() or there will be bugs
        # self.belonging_tasks = task_list
        self.belonging_tasks = task_list.copy()
        self.belonging_jobs = list()

        self.bind_machine(machine)

    def __repr__(self):
        return json.dumps(self.serialize(), indent=4)

    def __eq__(self, other):
        """When check whether the two submission are equal,
        we disregard the runtime infomation(job_state, job_id, fail_count) of the submission.belonging_jobs.
        """
        # print('submission.__eq__()  self', self.serialize(if_static=True))
        # print('submission.__eq__() other', other.serialize(if_static=True))
        return self.serialize(if_static=True) == other.serialize(if_static=True)

    @classmethod
    def deserialize(cls, submission_dict, machine=None):
        """convert the submission_dict to a Submission class object

        Parameters
        ----------
        submission_dict : dict
            path-like, the base directory of the local tasks

        Returns
        -------
        submission : Submission
            the Submission class instance converted from the submission_dict
        """
        submission = cls(work_base=submission_dict['work_base'],
            resources=Resources.deserialize(resources_dict=submission_dict['resources']),
            forward_common_files=submission_dict['forward_common_files'],
            backward_common_files=submission_dict['backward_common_files'])
        submission.belonging_jobs = [Job.deserialize(job_dict=job_dict) for job_dict in submission_dict['belonging_jobs']]
        submission.submission_hash = submission.get_hash()
        submission.bind_machine(machine=machine)
        return submission

    def serialize(self, if_static=False):
        """convert the Submission class instance to a dictionary.

        Parameters
        ----------
        if_static : bool
            whether dump the job runtime infomation (like job_id, job_state, fail_count) to the dictionary.

        Returns
        -------
        submission_dict : dict
            the dictionary converted from the Submission class instance
        """
        submission_dict = {}
        submission_dict['work_base'] = self.work_base
        submission_dict['resources'] = self.resources.serialize()
        submission_dict['forward_common_files'] = self.forward_common_files
        submission_dict['backward_common_files'] = self.backward_common_files
        submission_dict['belonging_jobs'] = [ job.serialize(if_static=if_static) for job in self.belonging_jobs]
        # print('&&&&&&&&', submission_dict['belonging_jobs'] )
        return submission_dict

    def register_task(self, task):
        if self.belonging_jobs:
            raise RuntimeError("Not allowed to register tasks after generating jobs."
                    "submission hash error {self}".format(self))
        self.belonging_tasks.append(task)
        # self.belonging_tasks = task

    def register_task_list(self, task_list):
        if self.belonging_jobs:
            raise RuntimeError("Not allowed to register tasks after generating jobs."
                    "submission hash error {self}".format(self))
        self.belonging_tasks.extend(task_list)
    def get_hash(self):
        return sha1(str(self.serialize(if_static=True)).encode('utf-8')).hexdigest()

    def bind_machine(self, machine):
        """bind this submission to a machine. update the machine's context remote_root and local_root.

        Parameters
        ----------
        machine : Machine
            the machine to bind with
        """
        self.submission_hash = self.get_hash()
        self.machine = machine
        for job in self.belonging_jobs:
            job.machine = machine
        if machine is not None:
            self.machine.context.bind_submission(self)
        return self

    def run_submission(self, *, exit_on_submit=False, clean=True):
        """main method to execute the submission.
        First, check whether old Submission exists on the remote machine, and try to recover from it.
        Second, upload the local files to the remote machine where the tasks to be executed.
        Third, run the submission defined previously.
        Forth, wait until the tasks in the submission finished and download the result file to local directory.
        if exit_on_submit is True, submission will exit.
        """
        if not self.belonging_jobs:
            self.generate_jobs()
        self.try_recover_from_json()
        if self.check_all_finished():
            print('debug:check_all_finished: True')
            pass
        else:
            print('debug:check_all_finished: False')
            self.upload_jobs()
            self.handle_unexpected_submission_state()
            self.submission_to_json()
        time.sleep(1)
        while not self.check_all_finished():
            if exit_on_submit is True:
                print('<<<<<<dpdispatcher<<<<<<SuccessSubmit<<<<<<exit 0<<<<<<')
                print(f"submission succeeded: {self.submission_hash}")
                print(f"at {self.machine.context.remote_root}")
                print("exit_on_submit")
                print('>>>>>>dpdispatcher>>>>>>SuccessSubmit>>>>>>exit 0>>>>>>')
                return self.serialize()
            try:
                time.sleep(40)
            except KeyboardInterrupt as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<KeyboardInterrupt<<<<<<exit 1<<<<<<')
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>KeyboardInterrupt>>>>>>exit 1>>>>>>')
                exit(1)
            except SystemExit as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<SystemExit<<<<<<exit 2<<<<<<')
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>SystemExit>>>>>>exit 2>>>>>>')
                exit(2)
            except Exception as e:
                self.submission_to_json()
                print('<<<<<<dpdispatcher<<<<<<{e}<<<<<<exit 3<<<<<<'.format(e=e))
                print('submission: ', self.submission_hash)
                print(self.serialize())
                print('>>>>>>dpdispatcher>>>>>>{e}>>>>>>exit 3>>>>>>'.format(e=e))
                exit(3)
            else:
                self.handle_unexpected_submission_state()
            finally:
                pass
        self.handle_unexpected_submission_state()
        self.submission_to_json()
        self.download_jobs()
        if clean:
            self.clean_jobs()
        return self.serialize()

    def get_submission_state(self):
        """check whether all the jobs in the submission.

        Notes
        -----
        this method will not handle unexpected (like resubmit terminated) job state in the submission.
        """
        for job in self.belonging_jobs:
            job.get_job_state()
            print('debug:get_submission_state: job: ', job.job_hash, job.job_id, job.job_state)
        # self.submission_to_json()

    def handle_unexpected_submission_state(self):
        """handle unexpected job state of the submission.
        If the job state is unsubmitted, submit the job.
        If the job state is terminated (killed unexpectly), resubmit the job.
        If the job state is unknown, raise an error.
        """
        for job in self.belonging_jobs:
            job.handle_unexpected_job_state()

    def submit_submission(self):
        """submit the job belonging to the submission.
        """
        for job in self.belonging_jobs:
            job.submit_job()
        self.get_submission_state()

    def check_all_finished(self):
        """check whether all the jobs in the submission.

        Notes
        -----
        This method will not handle unexpected job state in the submission.
        """
        self.get_submission_state()
        # print('debug:***', [job.job_state for job in self.belonging_jobs])
        # print('debug:***', [job for job in self.belonging_jobs])
        if any( (job.job_state in  [JobStatus.terminated, JobStatus.unknown] ) for job in self.belonging_jobs):
            self.submission_to_json()
        if any( (job.job_state in  [JobStatus.running,
            JobStatus.waiting,
            JobStatus.unsubmitted,
            JobStatus.completing,
            JobStatus.terminated,
            JobStatus.unknown]) for job in self.belonging_jobs):
            return False
        else:
            return True

    def generate_jobs(self):
        """After tasks register to the self.belonging_tasks,
        This method generate the jobs and add these jobs to self.belonging_jobs.
        The jobs are generated by the tasks randomly, and there are self.resources.group_size tasks in a task.
        Why we randomly shuffle the tasks is under the consideration of load balance.
        The random seed is a constant (to be concrete, 42). And this insures that the jobs are equal when we re-run the program.
        """
        if self.belonging_jobs:
            raise RuntimeError(f'Can not generate jobs when submission.belonging_jobs is not empty. debug:{self}')
        group_size = self.resources.group_size
        if ( group_size < 1 ) or ( type(group_size) is not int ):
            raise RuntimeError('group_size must be a positive number')
        task_num = len(self.belonging_tasks)
        if task_num == 0:
            raise RuntimeError("submission must have at least 1 task")
        random.seed(42)
        random_task_index = list(range(task_num))
        random.shuffle(random_task_index)
        random_task_index_ll = [random_task_index[ii:ii+group_size] for ii in range(0,task_num,group_size)]

        for ii in random_task_index_ll:
            job_task_list = [ self.belonging_tasks[jj] for jj in ii ]
            job = Job(job_task_list=job_task_list, machine=self.machine, resources=copy.deepcopy(self.resources))
            # print('generate_jobs', ii, job)
            self.belonging_jobs.append(job)

        if self.machine is not None:
            self.bind_machine(self.machine)

        self.submission_hash = self.get_hash()

    def upload_jobs(self):
        self.machine.context.upload(self)

    def download_jobs(self):
        self.machine.context.download(self)
        # for job in self.belonging_jobs:
        #     job.tag_finished()
        # self.machine.context.write_file(self.machine.finish_tag_name, write_str="")

    def clean_jobs(self):
        self.machine.context.clean()

    def submission_to_json(self):
        # print('~~~~,~~~', self.serialize())
        self.get_submission_state()
        write_str = json.dumps(self.serialize(), indent=4, default=str)
        submission_file_name = "{submission_hash}.json".format(submission_hash=self.submission_hash)
        self.machine.context.write_file(submission_file_name, write_str=write_str)

    @classmethod
    def submission_from_json(cls, json_file_name='submission.json'):
        with open(json_file_name, 'r') as f:
            submission_dict = json.load(f)
        # submission_dict = machine.context.read_file(json_file_name)
        submission = cls.deserialize(submission_dict=submission_dict, machine=None)
        return submission

    # def check_if_recover()

    def try_recover_from_json(self):
        submission_file_name = "{submission_hash}.json".format(submission_hash=self.submission_hash)
        if_recover = self.machine.context.check_file_exists(submission_file_name)
        submission = None
        submission_dict = {}
        if if_recover :
            submission_dict_str = self.machine.context.read_file(fname=submission_file_name)
            submission_dict = json.loads(submission_dict_str)
            submission = Submission.deserialize(submission_dict=submission_dict)
            if self == submission:
                self.belonging_jobs = submission.belonging_jobs
                self.bind_machine(machine=self.machine)
                self = submission.bind_machine(machine=self.machine)
            else:
                print(self.serialize())
                print(submission.serialize())
                raise RuntimeError("Recover failed.")

class Task(object):
    """a task is a sequential command to be executed, as well as its files to transmit forward and backward.

    Parameters
    ----------
    command : str
        the command to be executed.
    task_work_path : path-like
        the directory of each file where the files are dependent on.
    forward_files : list of path-like
        the files to be transmitted to other location before the calculation begins
    backward_files : list of path-like
        the files to be transmitted from other location after the calculation finished
    log : str
        the files to be transmitted from other location after the calculation finished
    err : str
        the files to be transmitted from other location after the calculation finished
    """
    def __init__(self,
                command,
                task_work_path,
                forward_files=[],
                backward_files=[],
                outlog='log',
                errlog='err',
                ):

        self.command = command
        self.task_work_path = task_work_path
        self.forward_files = forward_files
        self.backward_files = backward_files
        self.outlog = outlog
        self.errlog = errlog

        # self.task_need_resources = task_need_resources

        self.task_hash = self.get_hash()
        # self.task_need_resources="<to be completed in the future>"
        # self.uuid =

    def __repr__(self):
        return str(self.serialize())

    def __eq__(self, other):
        return self.serialize() == other.serialize()


    def get_hash(self):
        return sha1(str(self.serialize()).encode('utf-8')).hexdigest()

    @classmethod
    def deserialize(cls, task_dict):
        """convert the task_dict to a Task class object

        Parameters
        ----------
        task_dict : dict
            the dictionary which contains the task information
        Returns
        -------
        Task : task
            the Task class instance converted from the task_dict
        """
        task=cls(**task_dict)
        return task

    def serialize(self):
        task_dict={}
        task_dict['command'] = self.command
        task_dict['task_work_path'] = self.task_work_path
        task_dict['forward_files'] = self.forward_files
        task_dict['backward_files'] = self.backward_files
        task_dict['outlog'] = self.outlog
        task_dict['errlog'] = self.errlog
        # task_dict['task_need_resources'] = self.task_need_resources
        return task_dict

class Job(object):
    """Job is generated by Submission represnting a collection of task.
    Each Job can generate a Shell, PBS, or a Slurm script to be submitted the job scheduler system or executed locally.

    Parameters
    ----------
    job_task_liste : list of Task
        the tasks belong to the job
    resources : Resources
        the machine resources. Passed from Submission when instantiating.
    machine : machine
        machine object to execute the job. Passed from Submission when instantiating.
    """
    def __init__(self,
                job_task_list,
                *,
                resources,
                machine=None,
                ):
        self.job_task_list = job_task_list
        # self.job_work_base = job_work_base
        self.resources = resources
        self.machine = machine

        self.job_state = None # JobStatus.unsubmitted
        self.job_id = ""
        self.fail_count = 0
        self.job_uuid = uuid.uuid4()

        # self.job_hash = self.get_hash()
        self.job_hash = self.get_hash()
        self.script_file_name = self.job_hash+ '.sub'


    def __repr__(self):
        return str(self.serialize())

    def __eq__(self, other):
        """When check whether the two jobs are equal,
        we disregard the runtime infomation(job_state, job_id, fail_count) of the jobs.
        """
        return self.serialize(if_static=True) == other.serialize(if_static=True)

    @classmethod
    def deserialize(cls, job_dict, machine=None):
        """convert the  job_dict to a Submission class object

        Parameters
        ----------
        submission_dict : dict
            path-like, the base directory of the local tasks

        Returns
        -------
        submission : Job
            the Job class instance converted from the job_dict
        """
        if len(job_dict.keys()) != 1:
            raise RuntimeError("json file may be broken, len(job_dict.keys()) must be 1. {job_dict}".format(job_dict=job_dict))
        job_hash = list(job_dict.keys())[0]

        job_task_list = [Task.deserialize(task_dict) for task_dict in job_dict[job_hash]['job_task_list']]
        job = Job(job_task_list=job_task_list,
            resources=Resources.deserialize(resources_dict=job_dict[job_hash]['resources']),
            machine=machine)

        # job.job_runtime_info=job_dict[job_hash]['job_runtime_info']
        job.job_state = job_dict[job_hash]['job_state']
        job.job_id = job_dict[job_hash]['job_id']
        job.fail_count = job_dict[job_hash]['fail_count']
        # job.job_uuid = job_dict[job_hash]['job_uuid']
        return job

    def get_job_state(self):
        """get the jobs. Usually, this method will query the database of slurm or pbs job scheduler system and get the results.

        Notes
        -----
        this method will not submit or resubmit the jobs if the job is unsubmitted.
        """
        print('debug:self.machine',self.machine)
        job_state = self.machine.check_status(self)
        self.job_state = job_state

    def handle_unexpected_job_state(self):
        job_state = self.job_state

        if job_state == JobStatus.unknown:
            raise RuntimeError("job_state for job {job} is unknown".format(job=self))

        if job_state == JobStatus.terminated:
            print("job: {job_hash} terminated; restarting job".format(job_hash=self.job_hash))
            if self.fail_count > 3:
                raise RuntimeError("job:job {job} failed 3 times".format(job=self))
            # self.fail_count += 1
            self.submit_job()
            self.get_job_state()

        if job_state == JobStatus.unsubmitted:
            if self.fail_count > 3:
                raise RuntimeError("job:job {job} failed 3 times".format(job=self))
            # self.fail_count += 1
            self.submit_job()
            print("job: {job_hash} submit; job_id is {job_id}".format(job_hash=self.job_hash, job_id=self.job_id))
            # self.get_job_state()

    def get_hash(self):
        return str(list(self.serialize(if_static=True).keys())[0])

    def serialize(self, if_static=False):
        """convert the Task class instance to a dictionary.

        Parameters
        ----------
        if_static : bool
            whether dump the job runtime infomation (job_id, job_state, fail_count, job_uuid) to the dictionary.

        Returns
        -------
        task_dict : dict
            the dictionary converted from the Task class instance
        """
        job_content_dict = {}
        # for task in self.job_task_list:
        job_content_dict['job_task_list'] = [ task.serialize() for task in self.job_task_list ]
        job_content_dict['resources'] = self.resources.serialize()
        # job_content_dict['job_work_base'] = self.job_work_base
        job_hash = sha1(str(job_content_dict).encode('utf-8')).hexdigest()
        if not if_static:
            job_content_dict['job_state'] = self.job_state
            job_content_dict['job_id'] = self.job_id
            job_content_dict['fail_count'] = self.fail_count
            # job_content_dict['job_uuid'] = self.job_uuid
        return {job_hash: job_content_dict}

    def register_job_id(self, job_id):
        self.job_id = job_id

    def submit_job(self):
        job_id = self.machine.do_submit(self)
        self.register_job_id(job_id)
        self.job_state = JobStatus.waiting

    def job_to_json(self):
        # print('~~~~,~~~', self.serialize())
        write_str = json.dumps(self.serialize(), indent=2, default=str)
        self.machine.context.write_file(self.job_hash + '_job.json', write_str=write_str)


class Resources(object):
    """Resources is used to describe the machine resources we need to do calculations.

    Parameters
    ----------
    number_node : int
        the number of node we need to do the calculation.
    cpu_per_node : int
        cpu numbers of each node.
    gpu_per_node : int
        gpu numbers of each node.
    queue_name : str
        the job queue name of slurm or pbs job scheduler system.
    group_size : int
        the number of tasks in a job submitting script.
    strategy['if_cuda_multi_devices'] : bool
        experimentally, if there are multiple nvidia GPUS on the target computer, we want to compute the jobs to different GPUS.
        With this option, dpdispatcher will manually allocate environment variable CUDA_VISIBLE_DEVICES to different task.
        Usually, this option will be used with Task.task_need_resources variable simultaneously.
    para_deg : int
        Decide how many tasks will be run in parallel.
    """
    def __init__(self,
                number_node,
                cpu_per_node,
                gpu_per_node,
                queue_name,
                group_size,
                *,
                custom_flags=[],
                strategy=default_strategy,
                para_deg=1,
                source_list=[],
                **kwargs):
        self.number_node = number_node
        self.cpu_per_node = cpu_per_node
        self.gpu_per_node = gpu_per_node
        self.queue_name = queue_name
        self.group_size = group_size

        # self.extra_specification = extra_specification
        self.custom_flags = custom_flags
        self.strategy = strategy
        self.para_deg = para_deg
        self.source_list = source_list
        # self.if_cuda_multi_devices = if_cuda_multi_devices

        self.kwargs = kwargs

        self.gpu_in_use = 0
        self.task_in_para = 0
        # self. = 0
        # if self.gpu_per_node > 1:
        # self.in_para_task_num = 0

        if self.strategy['if_cuda_multi_devices'] is True:
            if gpu_per_node < 1:
                raise RuntimeError("gpu_per_node can not be smaller than 1 when if_cuda_multi_devices is True")
            if number_node != 1:
                raise RuntimeError("number_node must be 1 when if_cuda_multi_devices is True")

    def __eq__(self, other):
        return self.serialize() == other.serialize()

    def serialize(self):
        resources_dict = {}
        resources_dict['number_node'] = self.number_node
        resources_dict['cpu_per_node'] = self.cpu_per_node
        resources_dict['gpu_per_node'] = self.gpu_per_node
        resources_dict['queue_name'] = self.queue_name
        resources_dict['group_size'] = self.group_size

        resources_dict['custom_flags'] = self.custom_flags
        resources_dict['strategy'] = self.strategy
        resources_dict['para_deg'] = self.para_deg
        resources_dict['source_list'] = self.source_list
        resources_dict['kwargs'] = self.kwargs
        return resources_dict

    @classmethod
    def deserialize(cls, resources_dict):
        resources = cls(number_node=resources_dict['number_node'],
                        cpu_per_node=resources_dict['cpu_per_node'],
                        gpu_per_node=resources_dict['gpu_per_node'],
                        queue_name=resources_dict['queue_name'],
                        group_size=resources_dict['group_size'],

                        custom_flags=resources_dict['custom_flags'],
                        strategy=resources_dict['strategy'],
                        para_deg=resources_dict['para_deg'],
                        source_list=resources_dict['source_list'],
                        **resources_dict['kwargs'])
        return resources

    @classmethod
    def load_from_json(cls, json_file):
        with open(json_file, 'r') as f:
            resources_dict = json.load(f)
        resources = cls.deserialize(resources_dict=resources_dict)
        return resources

    @classmethod
    def load_from_dict(cls, resource_dict):
        return cls(**resource_dict)

# %%
