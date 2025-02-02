from fastapi import APIRouter, Depends

from fermentation_station.models.action_logger import ActionLogger

router = APIRouter()


def get_action_logger() -> ActionLogger:
    return ActionLogger()


@router.get("/last_action")
async def get_last_action(action_logger: ActionLogger = Depends(get_action_logger)):
    return action_logger.get_last_known_action()
