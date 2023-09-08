import openai
import os 
import ray
from ray import serve
from ray.serve.gradio_integrations import GradioIngress
import gradio as gr
import asyncio

api_key_env = os.getenv('ANYSCALE_API_KEY')
api_base_env = "https://api.endpoints.anyscale.com/v1"
model_13b = "meta-llama/Llama-2-13b-chat-hf"
model_7b = "meta-llama/Llama-2-7b-chat-hf"
system_content = """
You are a smart assistant trying to figure out why a Ray job has failed. Given a log, Generate a valid JSON object of most relevant error. The response should ALWAYS BE A VALID JSON format and it should be parsed in its ENTIRETY.
Object should contain the following properties:

1. relevantError: This SHOULD be up to 10 words max, a verbatim of the log line that is relevant to the error. If the error has a python exception name, then ALWAYS retain that exception name in output.
2. message: Explain in details why the error might have happened.
"""

sample_log = """
Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/tuner.py", line 364, in fit
    return self._local_tuner.fit()
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/impl/tuner_internal.py", line 613, in fit
    analysis = self._fit_internal(trainable, param_space)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/impl/tuner_internal.py", line 729, in _fit_internal
    analysis = run(
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/tune.py", line 1106, in run
    runner.step()
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 852, in step
    if not self._actor_manager.next(timeout=0.1):
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/air/execution/_internal/actor_manager.py", line 224, in next
    self._actor_task_events.resolve_future(future)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/air/execution/_internal/event_manager.py", line 118, in resolve_future
    on_result(result)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/air/execution/_internal/actor_manager.py", line 765, in on_result
    self._actor_task_resolved(
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/air/execution/_internal/actor_manager.py", line 300, in _actor_task_resolved
    tracked_actor_task._on_result(tracked_actor, result)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1404, in _on_result
    raise TuneError(traceback.format_exc())
ray.tune.error.TuneError: Traceback (most recent call last):
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1395, in _on_result
    on_result(trial, *args, **kwargs)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1709, in _on_training_result
    self._process_trial_results(trial, result)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1722, in _process_trial_results
    decision = self._process_trial_result(trial, result)
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1765, in _process_trial_result
    decision = self._scheduler_alg.on_trial_result(
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/schedulers/pbt.py", line 548, in on_trial_result
    self._checkpoint_or_exploit(
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/schedulers/pbt.py", line 637, in _checkpoint_or_exploit
    state.last_checkpoint = tune_controller._schedule_trial_save(
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/execution/tune_controller.py", line 1895, in _schedule_trial_save
    assert (
AssertionError: Memory checkpoints are no longer supported in the new persistence mode.


The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "horovod/workloads/horovod_tune_test.py", line 201, in <module>
    result_grid = tuner.fit()
  File "/home/ray/anaconda3/lib/python3.8/site-packages/ray/tune/tuner.py", line 366, in fit
    raise TuneError(
ray.tune.error.TuneError: The Ray Tune run failed. Please inspect the previous error messages for a cause. After fixing the issue, you can restart the run from scratch or continue this run. To continue this run, you can use `tuner = Tuner.restore("/home/ray/ray_results/HorovodTrainer_2023-08-19_02-50-12", trainable=...)`.
[2m[36m(RayTrainWorker pid=4797, ip=10.0.6.130)[0m Copying checkpoint files to storage path:[32m [repeated 3x across cluster][0m
[2m[36m(RayTrainWorker pid=4797, ip=10.0.6.130)[0m (<pyarrow._fs.LocalFileSystem object at 0x7f97d8071f30>, /tmp/tmp694xe2sx) -> (<pyarrow._fs.LocalFileSystem object at 0x7f97e1562cb0>, /mnt/cluster_storage/HorovodTrainer_2023-08-19_02-50-12/HorovodTrainer_ca911_00003_3_lr=0.4000_2023-08-19_02-50-14/checkpoint_000001)[32m [repeated 2x across cluster][0m
[2m[36m(RayTrainWorker pid=4797, ip=10.0.6.130)[0m Checkpoint successfully created at: Checkpoint(filesystem=<pyarrow._fs.LocalFileSystem object at 0x7f97e1562cb0>, path=/mnt/cluster_storage/HorovodTrainer_2023-08-19_02-50-12/HorovodTrainer_ca911_00003_3_lr=0.4000_2023-08-19_02-50-14/checkpoint_000001)[32m [repeated 3x across cluster][0m
Subprocess return code: 1
[INFO 2023-08-19 02:53:30,075] anyscale_job_wrapper.py: 190  Process 4500 exited with return code 1.
[INFO 2023-08-19 02:53:30,075] anyscale_job_wrapper.py: 292  Finished with return code 1. Time taken: 215.31985806400002
Completed 112 Bytes/112 Bytes (1.2 KiB/s) with 1 file(s) remaining
upload: ../../../../../release_test_out.json to s3://ray-release-automation-results/working_dirs/long_running_horovod_tune_test.aws/tblrpqqbiw/tmp/release_test_out.json
Completed 374 Bytes/374 Bytes (1.9 KiB/s) with 1 file(s) remaining
upload: ../../../../../metrics_test_out.json to s3://ray-release-automation-results/working_dirs/long_running_horovod_tune_test.aws/tblrpqqbiw/tmp/metrics_test_out.json
Completed 261 Bytes/261 Bytes (2.5 KiB/s) with 1 file(s) remaining
upload: ./output.json to s3://ray-release-automation-results/working_dirs/long_running_horovod_tune_test.aws/tblrpqqbiw/tmp/output.json
[INFO 2023-08-19 02:54:18,137] anyscale_job_wrapper.py: 345  ### Finished ###
[INFO 2023-08-19 02:54:18,137] anyscale_job_wrapper.py: 348  ### JSON |{"colle

"""

@serve.deployment
class TextGenerationModel:
    def __init__(self, model_name):
        self.model = model_name

    def __call__(self, api_base, api_key, text):
        
        try:
            response = openai.ChatCompletion.create(
                    api_base=api_base,
                    api_key=api_key,
                    model=self.model,
                    messages=[{"role": "system", "content": system_content},
                    {"role": "user", "content": text}],
                    temperature=0.9,
                    max_tokens=4000
                )
            choice = response["choices"][0]
            message = choice["message"]
            content = message["content"]
            return content
        except Exception as e:
            return e.message
        # return api_base + " \n " + api_key + " \n " + text
 
@serve.deployment
class MyGradioServer(GradioIngress):
    def __init__(self, downstream_1, downstream_2):
        self._d1 = downstream_1
        self._d2 = downstream_2
        super().__init__(lambda: gr.Interface(
            self.summarize, 
            inputs=[
                gr.Textbox(value=api_base_env, label="API URL"),
                gr.Textbox(value=api_key_env, label="API KEY"),
                gr.Textbox(value=sample_log, label="Input prompt")
                ],
            outputs=[gr.Textbox(label="Base 7b output"), gr.Textbox(label="Finetuned Model output")]
            )
        )

    async def summarize(self, api_base, api_key, text):
        refs = await asyncio.gather(self._d1.remote(api_base, api_key, text), self._d2.remote(api_base, api_key, text))
        [res1, res2] = ray.get(refs)
        return (
            f"[Generated text version 1]\n{res1}\n\n",
            f"[Generated text version 1]\n{res2}\n\n"
        )

app1 = TextGenerationModel.bind(model_7b)
app2 = TextGenerationModel.bind(model_13b)
app = MyGradioServer.bind(app1, app2)

# serve run demo:app