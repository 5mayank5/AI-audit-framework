from concurrent.futures import ThreadPoolExecutor

class ParallelExecutor:

    def execute(self, agents):
        results = []
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(agent.run) for agent in agents]
            for future in futures:
                results.append(future.result())
        return results