import time
from retrying import retry

from src.excepthread import ExcThread
from src.server import local_serve
from src.onedrive_call import call_onedrive_thread
from src.util.log import Log


@retry(stop_max_attempt_number=100, wait_fixed=60000)
def start_child_thread():
  """
    说明:
        因为网络原因可能执行失败，所以设定程序异常时
        最大尝试次数 100
        两次调用时间间隔 60000 ms
    feature:将所有子线程添加到线程列表中
    :return:
    """
  thread_task_list = []
  onedrive_thread = ExcThread(target=call_onedrive_thread,
                              name="call_onedrive_thread")
  onedrive_thread.start()

  # serve_thread = ExcThread(target=local_serve.run, name="server_thread")
  # serve_thread.start()

  # thread_task_list.append(serve_thread)
  thread_task_list.append(onedrive_thread)
  return thread_task_list


if __name__ == '__main__':
  """
    feature: 轮询各个子线程的状态，如果有子线程失败就结束主线程 
    从而有一个子线程异常时，主线程结束，导致所有子线程(已经全部设置为守护线程)退出
    """
  thread_list = start_child_thread()
  while True:
    for task in thread_list:
      if not task.is_alive():
        log_content = (str(task.exception) + "split_symb" + task.exc_traceback)
        Log.save_log(content=log_content)
        raise task.exception
    time.sleep(1)
