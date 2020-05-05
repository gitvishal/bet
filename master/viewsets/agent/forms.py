from master.forms import UserCreationForm as BaseUserCreationForm
from master.utils.queryset import get_instance_or_none
import sys

class UserCreationForm(BaseUserCreationForm):

	def save_relational_model(self, parent, child_payload):
		parent_agent = child_payload['parent_agent']
		agent = get_instance_or_none(getattr(sys.modules[child_payload['module']], child_payload['model']),  pk=parent_agent['pk'])
		child_payload.update({parent_agent['agent_parent_param']:agent})
		return super().save_relational_model(parent, child_payload)