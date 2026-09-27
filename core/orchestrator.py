from core.scoring_engine import ScoringEngine
from core.datastore import AuditDataStore

from agents.red_team_agent import RedTeamAgent
from agents.bias_agent import BiasAgent
from agents.safety_agent import SafetyAgent
from agents.robustness_agent import RobustnessAgent
from agents.toxicity_agent import ToxicityAgent

from agents.dataset_toxicity_agent import DatasetToxicityAgent
from agents.dataset_bias_agent import DatasetBiasAgent
from agents.injection_agent import InjectionAgent
from agents.adversarial_agent import AdversarialAgent


class AuditOrchestrator:

    def __init__(self, model_bundle, config):
        self.model = model_bundle
        self.config = config

    def run_audit(self):

        agents = []

        if self.config["agents"]["red_team"]:
            agents.append(RedTeamAgent(self.model, self.config))

        if self.config["agents"]["bias"]:
            agents.append(BiasAgent(self.model, self.config))

        if self.config["agents"]["safety"]:
            agents.append(SafetyAgent(self.model, self.config))

        if self.config["agents"]["robustness"]:
            agents.append(RobustnessAgent(self.model, self.config))

        if self.config["agents"]["toxicity"]:
            agents.append(ToxicityAgent(self.model, self.config))

        agent_results = []
        for agent in agents:
            agent_results.append(agent.run())

        toxicity_metrics = {}
        bias_metrics = {}

        if self.config["agents"]["dataset_mode"]:

            toxicity_dataset_agent = DatasetToxicityAgent(
                self.model,
                self.config,
                "datasets/toxicity_dataset.json"
            )
            toxicity_metrics = toxicity_dataset_agent.run()

            bias_dataset_agent = DatasetBiasAgent(
                self.model,
                self.config,
                "datasets/bias_dataset.json"
            )
            bias_metrics = bias_dataset_agent.run()

        injection_agent = InjectionAgent(self.model, self.config)
        injection_metrics = injection_agent.run()

        adversarial_agent = AdversarialAgent(self.model, self.config)
        adversarial_metrics = adversarial_agent.run()

        scoring = ScoringEngine()

        scored_results = scoring.score(
            agent_results,
            toxicity_metrics,
            bias_metrics,
            injection_metrics,
            adversarial_metrics
        )

        scored_results["dataset_toxicity_metrics"] = toxicity_metrics
        scored_results["dataset_bias_metrics"] = bias_metrics
        scored_results["injection_metrics"] = injection_metrics
        scored_results["adversarial_metrics"] = adversarial_metrics

        datastore = AuditDataStore()
        datastore.save(scored_results)

        return scored_results