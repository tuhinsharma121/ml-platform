import uvicorn
from fastapi import FastAPI

from kronos_platform.deployment.scheduler.routers import container, heartbeat
from kronos_platform.deployment.scheduler.routers import forecast_engine, cluster_status

# Initialize FastAPI application
app = FastAPI(title="Kronos Scheduler",
              description="Apis for {app_name}".format(app_name="Kronos Scheduler"),
              docs_url="/hxdocs",
              redoc_url=None,
              version="1.0",
              openapi_url="/api/{app_version}/schemas/openapi.json".format(
                  app_version="1.0"))

# Initialize app modules - Any persistent modules
# app.snowflake_data_store = SnowflakeDataStore()
# app.redshift_data_store = PostgresDataStore()
# app.rds_data_store = MySQLDataStore()

# Include engine routers
app.include_router(heartbeat.router)
app.include_router(container.router)
app.include_router(forecast_engine.router)
app.include_router(cluster_status.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9009)
