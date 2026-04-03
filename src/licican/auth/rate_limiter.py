from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass
class _AttemptStore:
    attempts: dict[str, deque[datetime]] = field(default_factory=lambda: defaultdict(deque))


class LoginRateLimiter:
    def __init__(self, max_attempts: int = 5, window_minutes: int = 5) -> None:
        self.max_attempts = max_attempts
        self.window = timedelta(minutes=window_minutes)
        self._store = _AttemptStore()

    def is_limited(self, client_ip: str, now: datetime | None = None) -> bool:
        current = now or datetime.now(UTC)
        attempts = self._prune(client_ip, current)
        return len(attempts) >= self.max_attempts

    def register_failure(self, client_ip: str, now: datetime | None = None) -> None:
        current = now or datetime.now(UTC)
        attempts = self._prune(client_ip, current)
        attempts.append(current)

    def reset(self, client_ip: str) -> None:
        self._store.attempts.pop(client_ip, None)

    def _prune(self, client_ip: str, current: datetime) -> deque[datetime]:
        attempts = self._store.attempts[client_ip]
        lower_bound = current - self.window
        while attempts and attempts[0] < lower_bound:
            attempts.popleft()
        if not attempts:
            self._store.attempts.pop(client_ip, None)
            return self._store.attempts[client_ip]
        return attempts


rate_limiter = LoginRateLimiter()
