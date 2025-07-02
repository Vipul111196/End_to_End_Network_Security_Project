.PHONY: install run train docker-up docker-down monitoring-up clean

install:
	pip install -r requirements.txt

run:
	python app.py

train:
	python main.py

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

monitoring-up:
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "MLflow: http://localhost:5000"
	@echo "API: http://localhost:8080/docs"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; true
	rm -rf Artifacts/ final_model/ mlruns/ logs/ prediction_output/
