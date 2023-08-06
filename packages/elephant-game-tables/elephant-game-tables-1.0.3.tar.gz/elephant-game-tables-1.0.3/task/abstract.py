class AbstractTask:
    __task_name__ = ""

    def __init__(self):
        self.task_steps = []
        self.task_results = []

    def append_task_step(self, name, step_fun):
        self.task_steps.append({
            "name": name,
            "fun": step_fun
        })

    def append_task_steps(self, steps):
        for step_name, step_fun in steps.items():
            self.append_task_step(step_name, step_fun)

    def append_task_result(self, result):
        self.task_results.append(result)

    def run(self):
        self._run_task()
        self._show_results()

    def _run_task(self):
        print(f"============================= task 【{self.__task_name__}】 : begin =============================")
        total_steps = len(self.task_steps)
        for index, step in enumerate(self.task_steps, start=1):
            step_name = step["name"]
            step_fun = step["fun"]
            print(f"------ step [{index}/{total_steps}]: {step_name} : begin ------")
            task_run_ret = self._run_task_step(step_name, step_fun)
            print(f"------ step [{index}/{total_steps}]: {step_name} : end ------")
            if not task_run_ret:
                break
        print(f"============================= run [{self.__task_name__}] : end =============================")

    def _run_task_step(self, step_name, step_fun):
        try:
            return step_fun()
        except Exception as e:
            print(f"run [{self.__task_name__}] of step [{step_name}] error! error=>[{e}]")
            raise e

    def _show_results(self):
        print(f"============================= show run 【{self.__task_name__}】 result : begin =============================")
        result_count = len(self.task_results)
        for index, result in enumerate(self.task_results, start=1):
            print(f"------ result [{index}/{result_count}]: {result}")
        print(f"============================= show run 【{self.__task_name__}】 result : end =============================")
