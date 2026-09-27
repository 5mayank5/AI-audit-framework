from core.model_loader import load_config, load_model
from core.orchestrator import AuditOrchestrator
from core.experiment_logger import ExperimentLogger
from reports.json_exporter import JSONExporter
from reports.csv_exporter import CSVExporter
from reports.report_generator import HTMLReportGenerator


def main():

    config = load_config()
    logger = ExperimentLogger()

    env = logger.collect_environment()
    logger.save(env)

    # 🔹 Run ONLY one model per execution
    model_name = config["baseline_models"][0]

    print(f"\nRunning audit for: {model_name}")

    model = load_model(model_name)
    orchestrator = AuditOrchestrator(model, config)
    result = orchestrator.run_audit()

    JSONExporter().export(result)
    CSVExporter().export(result)
    HTMLReportGenerator().generate(result)

    print("Score:", result["total_score"])
    print("Severity:", result["severity"])


if __name__ == "__main__":
    main()