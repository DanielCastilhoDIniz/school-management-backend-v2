from datetime import date

from django.utils.translation import gettext_lazy as _

from core.domain.errors import ...

class MemberShip(id, user_id, role, status, start_date, end_date):

    """
    para consultar durante a construção
        ACTIVE = 'active', _('Active')
        INACTIVE = 'inactive', _('Inactive')
        SUSPENDED = 'suspended', _('Suspended')
        COMPLETED = 'completed', _('Completed')

    """

def activate(self):
    if self.status == MembershipStatus.ACTIVE:
        raise MembershipAlreadyActiveError()
    self.status = MembershipStatus.ACTIVE














