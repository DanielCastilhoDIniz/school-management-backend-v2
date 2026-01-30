from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum


class MembershipState(Enum):
    """
    Possible states of a membership.
    """

    ACTIVE = 'active'
    INACTIVE = 'inactive'
    SUSPENDED = 'suspended'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    EXPIRED = 'expired'


@dataclass(frozen=True)
class MembershipStatus:
    """
    Value Object que representa o estado atual de um vínculo/membership.
    Só responde perguntas (é imutável e sem side-effects).
    """
    state: MembershipState
    start_date: date
    end_date = date | None

    def __post_init__(self):
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be earlier than start date.")

    def is_active_on(self, when: date | datetime) -> bool:

        when_date = when.date() if isinstance(when, datetime) else when

        if self.state in {
            MembershipState.CANCELED,
            MembershipState.SUSPENDED,
            MembershipState.COMPLETED,
            MembershipState.EXPIRED,
            MembershipState.INACTIVE,
        }:
            return False

        if when_date < self.start_date:
            return False

        if self.end_date and when_date > self.end_date:
            return False

        if when_date <= self.end_date:
            return True

    def is_active_now(self) -> bool:
        return self.is_active_on(datetime.now())

    def days_until_expiration(self,
                              reference: date | None = None) -> int | None:
        ref = reference or date.today()

        if self.end_date is None:
            return None

        delta = (self.end_date - ref).days

        if delta < 0:
            return None

        return delta

    def requires_attention(self) -> bool:

        if self.state != MembershipState.ACTIVE:
            return True

        days_left = self.days_until_expiration()
        if days_left is None:
            return False








