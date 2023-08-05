import uvicorn

from stonehenge.application import Application


def runserver(app: Application):
    uvicorn.run(
        app.APP_PATH,
        host=app.HOST,
        port=app.PORT,
        log_level=app.LOG_LEVEL,
        reload=app.RELOAD_RUNSERVER,
    )
