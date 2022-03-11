import datetime

from dataclasses import dataclass
from typing import Optional
from ..type import ID
from ..enums import JobResultAction, JobResultActionReason


@dataclass
class JobResult:
    """Represents a download result from a job.

    .. versionadded:: 1.5.0
    """

    id: ID
    action: JobResultAction
    reason: JobResultActionReason
    created_at: datetime.datetime
    redacted_at: Optional[datetime.datetime] = None
