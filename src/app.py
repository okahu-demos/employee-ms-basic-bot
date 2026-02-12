"""
Agent Framework Entry Point - using Azure OpenAI Assistants API
"""
# Enable Monocle Tracing
from monocle_apptrace import setup_monocle_telemetry
setup_monocle_telemetry(workflow_name = 'employee-ms-basic-bot', monocle_exporters_list = 'file,okahu')

from http import HTTPStatus
import logging

from aiohttp import web
from botbuilder.core.integration import aiohttp_error_middleware

from bot import bot_app

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

routes = web.RouteTableDef()

@routes.post("/api/messages")
async def on_messages(req: web.Request) -> web.Response:
    logger.debug("Received a POST to /api/messages")
    res = None
    import os
    print("[env] BOT_ID=", os.environ.get("BOT_ID"))
    print("[env] BOT_TYPE=", os.environ.get("BOT_TYPE"))
    print("[env] BOT_TENANT_ID=", os.environ.get("BOT_TENANT_ID"))
    print("[env] BOT_PASSWORD set?=", bool(os.environ.get("BOT_PASSWORD")))
    try:
        logging.debug("Received a message from Teams")
        res = await bot_app.process(req)
        logger.debug("bot_app.process returned: %s", res)
    except Exception as e:
        logger.exception("Error processing message")

    if res is not None:
        return res

    return web.Response(status=HTTPStatus.OK)

@routes.get("/")
async def on_ping(req: web.Request) -> web.Response:
    return web.Response(status=HTTPStatus.OK)


app = web.Application(middlewares=[aiohttp_error_middleware])
app.add_routes(routes)

from config import Config

# Cleanup on shutdown
async def on_shutdown(app):
    await bot_app.cleanup()

app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=Config.PORT)
