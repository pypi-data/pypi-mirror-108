from sovereign.modifiers.lib import Modifier
from sovereign.context import template_context
from sovereign.utils import eds, templates


class Test(Modifier):
    def match(self) -> bool:
        return True

    def apply(self) -> None:
        assert template_context
        assert eds
        assert templates
