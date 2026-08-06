from helios.worker import MockWorker


class SingleWorkerPolicy:
    def __init__(self, worker: MockWorker) -> None:
        self.worker = worker

    def select_worker(self) -> MockWorker:
        return self.worker
