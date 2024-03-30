from .route_auth import bp_auth
from .route_logs import bp_logs
from .route_task import bp_task

all_blueprints = (
    (bp_task, '/api/tasks'),
    (bp_logs, '/api/logs'),
    (bp_auth, '/api/auth'),
)